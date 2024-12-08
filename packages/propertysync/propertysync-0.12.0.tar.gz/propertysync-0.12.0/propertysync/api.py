import requests, os, time, tempfile, datetime

requests.packages.urllib3.disable_warnings() #disable warnings for unverified HTTPS requests

"""
This is a helper for interacting with the PropertySync API
"""

# TODO: Follow styleguide: https://google.github.io/styleguide/pyguide.html#316-naming

class ApiClient:
    def __init__(self, email=None, password=None, document_group_id=None, company_id=None):
        self.search_url = "https://api.propertysync.com/v1/search"
        self.login_url = "https://api.propertysync.com/v1/login"
        self.indexing_url = "https://api.propertysync.com/v1/indexing"
        self.trailing_slash = "" #this should get set if we change the URLs above
        self.user_agent = "PropertySync API Python Client"
        self.email = email
        self.password = password
        self.token = None
        self.company_id = company_id
        self.document_group_id = document_group_id
        self.document_group_info = None

        self.login()

    def get_document_group_name(self):
        if self.document_group_info is None:
            self.document_group_info = self.get_info()
        return self.document_group_info["name"]
    
    def get_document_group_county(self):
        if self.document_group_info is None:
            self.document_group_info = self.get_info()
        return self.document_group_info["county"]
    
    def get_document_group_state(self):
        if self.document_group_info is None:
            self.document_group_info = self.get_info()
        return self.document_group_info["state"]

    def get_plant_effective_date(self):
        if self.document_group_info is None:
            self.document_group_info = self.get_info()
        return self.document_group_info["plantEffectiveDate"]
    
    # requires admin access
    def set_plant_effective_date(self, plant_effective_date):

        try:
            datetime.date.fromisoformat(plant_effective_date)
        except ValueError:
            raise ValueError("Incorrect effective date format, should be YYYY-MM-DD")

        # set the date in local copy of info
        self.document_group_info["plantEffectiveDate"] = plant_effective_date

        url = f"{self.indexing_url}/document-groups/{self.document_group_id}"
        return self.api_call("PATCH", url, params={"plantEffectiveDate":plant_effective_date})
    
    def set_document_group_id(self, document_group_id):
        # reset the document group info
        self.document_group_info = None
        self.document_group_id = document_group_id
    
    def set_company_id(self, company_id):
        self.company_id = company_id

    def get_token(self):
        return self.token
    
    def get_company_id(self):
        return self.company_id  
    
    def get_document_group_id(self):
        return self.document_group_id

    # login function
    def login(self):
        # if email is not set, check for environment variables
        if self.email is None:
            if os.environ.get("PROPERTYSYNC_API_EMAIL") is None:
                raise Exception("Email is not set")
            else:
                self.email = os.environ.get("PROPERTYSYNC_API_EMAIL")

        # if password is not set, check for environment variables
        if self.password is None:
            if os.environ.get("PROPERTYSYNC_API_PASSWORD") is None:
                raise Exception("Password is not set")
            else:
                self.password = os.environ.get("PROPERTYSYNC_API_PASSWORD")

        credentials = {"email":self.email,"password":self.password}
        
        headers = {
            "User-Agent": self.user_agent,
            "Content-Type": "application/json"
            }
        
        login_request = requests.post(self.login_url,json=credentials, headers=headers, verify=False)

        if login_request.status_code != 200:
            raise Exception("Login failed: "+login_request.text)

        self.token = login_request.json()["token"]

    # make a call to the API
    def api_call(self, method, url, params=None, body=None, tries=1):
        # create a header with the token
        headers = {
            "User-Agent": self.user_agent,
            "Authorization": "Bearer "+self.token, 
            "Content-Type": "application/json"
        }

        # append our trailing slash if it is not already there and must be set
        if self.trailing_slash != "" and url[-1] != self.trailing_slash:
            url += self.trailing_slash

        if (method == "GET"):
            request = requests.get(url,params=params,headers=headers, json=body, verify=False)
        elif (method == "POST"):
            request = requests.post(url,params=params,headers=headers, json=body, verify=False)
        elif (method == "DELETE"):
            request = requests.delete(url,params=params,headers=headers, json=body, verify=False)    
        elif (method == "PATCH"):
            request = requests.patch(url,params=params,headers=headers, json=body, verify=False)             
        else:
            raise Exception("Invalid method: "+method)

        # determine if the request was successful
        if request.status_code == 200:
            # if we are requesting a PDF, return the raw content
            if "pdf" in request.headers["Content-Type"]:
                return request.content
            else:
                return request.json()
        elif request.status_code == 401:
            # if the token is invalid, try to login again, if we receive a failure again, raise an exception
            if (tries < 2):
                tries += 1
                self.login()
                return self.api_call(method=method, url=url, params=params, tries=tries)
            else:
                raise Exception("Unauthorized : "+request.text)
        elif request.status_code == 403:
            raise Exception("Forbidden: You do not have access to this resource")
        elif request.status_code == 404:
            raise Exception("Not Found: "+request.text)
        elif request.status_code == 500:
            raise Exception("Server Error: "+request.text)
        else:
            raise Exception("Unknown Error: "+request.text)

    # get info about the document group
    def get_info(self):
        if self.document_group_info is not None:
            return self.document_group_info
        
        url = f"{self.indexing_url}/document-groups/{self.document_group_id}"
        return self.api_call("GET", url, None)

    # get a list of batches
    def get_batches(self):
        url = f"{self.indexing_url}/document-groups/{self.document_group_id}/batches"
        return self.api_call("GET", url, None)

    # create a batch
    def create_batch(self, batch_name, search_id=None):
        url = f"{self.indexing_url}/document-groups/{self.document_group_id}/batches"
        params = {"name":batch_name}
        if search_id is not None:
            params["searchId"] = search_id
        return self.api_call("POST", url, params)
    
    # create batch from json, optionally save to search
    def create_batch_from_json(self, json, save_to_search=False, wait_time=2):
        url = f"{self.indexing_url}/document-groups/{self.document_group_id}/batches"

        #if they want to save to search, we need to count the number of documents in the batch
        if save_to_search:
            num_documents = len(json["documents"])

            # create the batch
            batch = self.api_call("POST", url, body=json)

            # check the status of the batch until numOfDocs is equal to the number of documents in the batch
            while batch["numOfDocs"] != num_documents:
                time.sleep(wait_time)
                batch = self.get_batch_info(batch["id"])

            # update the batch to save to search
            self.save_batch_to_search(batch["id"])

            return batch
        else:
            return self.api_call("POST", url, body=json)
    
    # update batch from json
    def update_batch_from_json(self, json, batch_id=None):
        # if batch_id is none, we need to determine from the json
        if batch_id is None:
            if "id" in json:
                batch_id = json["id"]
       
        # if we still don't have a batch_id, raise an exception
        if batch_id is None:
            raise Exception("Batch ID is not set")

        url = f"{self.indexing_url}/document-groups/{self.document_group_id}/batches/{batch_id}"
        return self.api_call("PATCH", url, body=json)
    
    # create batch from file at URL
    def create_batch_from_url(self, file_url):
        url = f"{self.indexing_url}/document-groups/{self.document_group_id}/batches"
        body = {
            "name":"Python CLI Batch", 
            "fileUrl":file_url
            }

        return self.api_call("POST", url, body=body)

    # delete a batch
    def delete_batch(self, batch_id):
        url = f"{self.indexing_url}/document-groups/{self.document_group_id}/batches/{batch_id}"
        return self.api_call("DELETE", url)
    
    # get batch info
    def get_batch_info(self, batch_id):
        url = f"{self.indexing_url}/document-groups/{self.document_group_id}/batches/{batch_id}"
        return self.api_call("GET", url)
    
    # get batch documents
    def get_batch(self, batch_id, filter=None):
        # filter can be "complete" or "incomplete" to filter by status
        url = f"{self.indexing_url}/document-groups/{self.document_group_id}/batches/{batch_id}"
        params = {
            "include-documents":1
        }
        if filter is not None:
            params["filter[completedFilter]"] = filter
        return self.api_call("GET", url, params=params)
    
    # save batch to search
    def save_batch_to_search(self, batch_id):
        url = f"{self.indexing_url}/document-groups/{self.document_group_id}/queue-process-documents"
        params = {
            "exportTo":"propertySync",
            "batchId":batch_id
        }
        return self.api_call("GET", url, params=params)
    
    # get autocompletes
    def get_autocompletes(self, type=None, search=None):
        url = f"{self.indexing_url}/document-groups/{self.document_group_id}/auto-completes"
        params = {}

        if type is not None:
            params["type"] = type
        if search is not None:
            params["search"] = search

        return self.api_call("GET", url, params=params)
    
    # delete an autocomplete
    def delete_autocomplete(self, autocomplete_id):
        url = f"{self.indexing_url}/document-groups/{self.document_group_id}/auto-completes/{autocomplete_id}"
        return self.api_call("DELETE", url)
    
    # add an autocomplete
    def add_autocomplete(self, type, value):
        url = f"{self.indexing_url}/document-groups/{self.document_group_id}/auto-completes"
        body = {
            "type":type,
            "value":value
        }
        return self.api_call("POST", url, body=body)
    
    # get landvalidations
    def get_landvalidations(self, type=None, pageSize=10000, page=None):
        url = f"{self.indexing_url}/document-groups/{self.document_group_id}/land-validations"
        params = {}

        if type is not None:
            params["type"] = type

        # always get the compact version
        params["compact"] = 1

        # default to 10000
        params["size"] = pageSize

        # if page is not set, assume they want them all. Get the first page to determine the total number of pages
        if page is None:
            page = 1
            params["page"] = page
            
            # get the first page, this will tell us how many pages there are
            validationsPage = self.api_call("GET", url, params=params)
            validations = validationsPage["data"]

            total = validationsPage["total"]
            totalPages = total // pageSize

            # if there is a remainder, add one to the total pages
            if total % pageSize > 0:
                totalPages += 1

            # if there is more than one page, get the rest of the pages
            if totalPages > 1:
                # loop through the rest of the pages
                for page in range(2,totalPages+1):
                    params["page"] = page

                    validationsPage = self.api_call("GET", url, params=params)

                    validations += validationsPage["data"]

        else:
            # they only want a single page
            params["page"] = page
            validationsPage = self.api_call("GET", url, params=params)
            validations = validationsPage["data"]

        return validations

    # add a landvalidation
    def add_landvalidation(self, validation_data):
        """
        Add a new land validation to the document group
        
        Args:
            validation_data (dict): Dictionary containing the validation data. 
                This can be any valid land validation structure - the method will 
                preserve the structure as provided.
                
                Example of a plat validation structure:
                {
                    "addition": "PIPPINPOST SUB LTS 1 - 50",
                    "platDate": "1989-10-25",
                    "bookNumber": "H",
                    "pageNumber": "9",
                    "platValidation": [{...}],
                    "instrumentNumber": null
                }
                
                But other validation structures are also valid depending on the 
                type of land validation being added.
            
        Returns:
            dict: The response from the API
        """
        url = f"{self.indexing_url}/document-groups/{self.document_group_id}/land-validations"
        
        # Simply wrap the provided validation data in a json key
        # This preserves whatever structure is provided
        body = {
            "json": validation_data
        }
        
        return self.api_call("POST", url, body=body)
    
    # get document IDs from a search ID
    def get_document_ids_from_search(self, search_id):
        url = f"{self.search_url}/document-groups/{self.document_group_id}/searches/{search_id}/document-ids"
        return self.api_call("GET", url)
    
    # get JSON from a document ID
    def get_json_from_document_id(self, document_id):
        url = f"{self.indexing_url}/document-groups/{self.document_group_id}/documents/{document_id}"
        return self.api_call("GET", url)
    
    # get assets from a document ID
    def get_document_assets(self, document_id):
        url = f"{self.indexing_url}/document-groups/{self.document_group_id}/documents/{document_id}/assets"
        return self.api_call("GET", url)
    
    # get asset from a document ID
    def get_document_asset(self, document_id, asset_id):
        url = f"{self.indexing_url}/document-groups/{self.document_group_id}/documents/{document_id}/assets/{asset_id}"
        return self.api_call("GET", url)
    
    # get pdf from assets
    def get_document_pdf(self, document_id):
        # first, get all assets for this document
        assets = self.get_document_assets(document_id)
        if(len(assets) == 0):
            raise Exception("No assets found for document ID "+document_id)
        
        # find the PDF asset
        if "pdf" not in assets:
            raise Exception("No PDF found for document ID "+document_id)
        
        # get the PDF asset
        pdf_asset = self.get_document_asset(document_id, assets["pdf"]["id"])

        # create a temp file name for the pdf on this os
        temp_file_name = tempfile.NamedTemporaryFile(suffix=".pdf").name

        # download the PDF to the temp file
        with open(temp_file_name, 'wb') as f:
            f.write(pdf_asset)

        # return the temp file name
        return temp_file_name
    
    # get versions from a document ID
    def get_document_versions(self, document_id):
        url = f"{self.indexing_url}/document-groups/{self.document_group_id}/documents/{document_id}/versions"
        return self.api_call("GET", url)

    # get orders (requires a company ID)
    def get_orders(self):
        if self.company_id is None:
            raise Exception("You must set a company ID to use this method")
        url = f"{self.search_url}/document-groups/{self.document_group_id}/companies/{self.company_id}/orders"
        return self.api_call("GET", url)

    # close an order
    def close_order(self, order_id):
        if self.company_id is None:
            raise Exception("You must set a company ID to use this method")
        url = f"{self.search_url}/document-groups/{self.document_group_id}/companies/{self.company_id}/orders/{order_id}/close"
        return self.api_call("POST", url)

    # reopen an order
    def reopen_order(self, order_id):
        if self.company_id is None:
            raise Exception("You must set a company ID to use this method")
        url = f"{self.search_url}/document-groups/{self.document_group_id}/companies/{self.company_id}/orders/{order_id}/re-open"
        return self.api_call("POST", url)
    
    # get document group meta data
    def get_document_group_metadata(self):
        url = f"{self.indexing_url}/document-groups/{self.document_group_id}/plant-info"
        return self.api_call("GET", url)
    
    # run a report
    def run_report(self, report_id, params=None):
        url = f"{self.search_url}/reports/{report_id}/run"
        return self.api_call("GET", url, params=params)
    
    # run a search
    def run_search(self, search_query):
        url = f"{self.search_url}/document-groups/{self.document_group_id}/searches"
        return self.api_call("POST", url, body=search_query)
    
    # run a document action on a batch
    def run_document_action(self, batch_id, action_id, document_ids=None):
        url = f"{self.indexing_url}/document-groups/{self.document_group_id}/document-actions/{action_id}/execute"
        # if document_ids is set and has a count of more than 0, add it to the params
        params = {
            "batchId":batch_id
        }
        if document_ids is not None and len(document_ids) > 0:
            params["documentIds"] = document_ids

        return self.api_call("POST", url, body=params)
    
    # validate a document
    def validate_document(self, document_json):
        url = f"{self.indexing_url}/document-groups/{self.document_group_id}/documents/validate"

        # if document_json contains an "id" key and no "json" key, it will validate the stored copy of the document
        # if document_json contains a "json" key and no "id" key, it will validate the json
        # if document_json contains a "json" key and no "id" key and the "json" contains a "indexingRecordId" key, it will validate the stored copy of the document

        # if they are passing in "json", assume they want that validated, create a copy of the json and remove the "id" and "indexingRecordId" keys

        # create a copy of the json so that we don't modify the original document
        new_json = None
        if "json" in document_json:
            new_json = {"json": document_json["json"]}
            if "indexingRecordId" in new_json["json"]:
                del new_json["json"]["indexingRecordId"]
        elif "id" in document_json:
            new_json = {"id": document_json["id"]}


        # if they are not passing in "json", assume they want the stored copy validated and ensure they have passed an ID
        if "json" not in new_json and "id" not in new_json:
            raise Exception("You must pass either an ID or JSON to validate a document")

        return self.api_call("POST", url, body=new_json)
        
        
    # run a search, then create a batch and wait for the batch to fully hydrate, then retrieve the batch and optionally delete it
    def run_search_and_create_batch(self, search_query, minimum_results=1,wait_time=2,batch_name='python-api-client temp batch', delete_batch=True):
        search = self.run_search(search_query)
        search_id = search["id"]

        # if we don't have enough results in the search, throw an exception
        if search["count"] < minimum_results:
            raise Exception(f"Search returned {search['count']} results, but we need at least {minimum_results} to create a batch")

        batch_id = self.create_batch(batch_name,search_id)["id"]
        batch_info = self.get_batch_info(batch_id)
        while batch_info["numOfDocs"] < search["count"]:
            time.sleep(wait_time)
            batch_info = self.get_batch_info(batch_id)

        ## once here, we should be complete
        batch = self.get_batch(batch_id)

        # optionally delete the batch
        if delete_batch:
            self.delete_batch(batch_id)

        return batch

    # run the user-activity report
    def run_user_activity_report(self, start_date, end_date, format="json"):
        params = {
            "companyId":self.company_id,
            "plantId":self.document_group_id,
            "responseType":format,
            "startDate":start_date,
            "endDate":end_date
        }
        return self.run_report("user-activity", params=params)
