import json
from .titlesearch_batch import TitleSearchBatch
from .document import Document
from .document import BaseJsonElement

from jsonpath_ng import jsonpath
from jsonpath_ng.ext import parse

"""
This is a helper class for working with PropertySync batches.
"""

class Batch(BaseJsonElement):
    def __init__(self, json_string=None):
        # first, initialize all of the properties
        super().__init__(json_string)
        # now save a copy of our _json dictionary
        self._json = json.loads(json_string)
        
    def __len__(self):
        return len(self.documents)

    # documents
    @property
    def documents(self):
        # if there is a documents key in the dictionary, convert it to a list of Document objects
        if "documents" in self._json:
            return [Document(x) for x in self._json["documents"]]
        else:
            return []
        
    @documents.setter
    def documents(self, value):
        # value should be a list of Document objects
        self._json["documents"] = [x.to_json() for x in value]

    # update my json from documents
    def _update_json(self):
        self._json["documents"] = [x.to_json() for x in self.documents]

    # # dump to json
    # def to_json(self):
    #     # first, loop through the documents and convert them to json to reset our _json["documents"] value
    #     doc_json = []
    #     for doc in self.documents:
    #         doc_json.append(doc.to_json())

    #     # now, set our _json["documents"] value to the json we just created
    #     self._json["documents"] = doc_json

    #     # dump the dictionary to json, hiding any private variables
    #     return json.dumps({k: v for k, v in self.__dict__.items() if not k.startswith("_")})

    # add_document
    def add_document(self, document):
        # document should be a Document object
        self.documents.append(document.to_json())

    def documents_with_tags(self, tags):
        return [doc for doc in self.documents if set(tags).issubset(set(doc.tags))]
    
    def documents_without_tags(self, tags):
        return [doc for doc in self.documents if not set(tags).issubset(set(doc.tags))]
    
    # get documents with a specific instrumentType value
    def documents_with_instrument_type(self, instrument_type):
        return [doc for doc in self.documents if doc.instrumentType == instrument_type]
    
    # load a batch from a titlesearch batch file
    def load_from_titlesearch_batch(self, titlesearch_batch_file):
        ts_batch = TitleSearchBatch(titlesearch_batch_file)
        self.load(ts_batch.get_json())
    
    # get all of the instrumentNumbers for a given instrumentType, or all instrumentNumbers if no instrumentType is specified
    def instrument_numbers(self, instrument_type_filter = None):
        if instrument_type_filter:
            return [doc.instrumentNumber for doc in self.documents if doc.instrumentType == instrument_type_filter]
        else:
            return [doc.instrumentNumber for doc in self.documents]

    # find all documents in the batch that have a specific value in a specific json node
    def find_documents(self, json_path, where_value):
        # for each document, check to see if the value matches
        return [doc for doc in self.documents if doc.find(json_path)[0].value == where_value]

    # replace  with "value" in "json_path" for all documents in this batch json
    def replace_in_documents(self, json_path, value, where_json_path=None, where_value=None):
        # if where_json_path and where_value are specified, only replace in documents where the where_json_path value matches the where_value
        if where_json_path and where_value:
            # for each document, check to see if the value matches
            for doc in self.documents:
                if doc.find(where_json_path)[0].value == where_value:
                    doc.replace(json_path, value)
        else:
            # for each document, check to see if the value matches
            for doc in self.documents:
                doc.replace(json_path, value)
                            
    # find all nodes in the batch json that have a specific value
    def find(self, json_path):
        # before we work with json directly, make sure our json is current
        self._update_json()

        jsonpath_expr = parse(json_path)
        matches = jsonpath_expr.find(self._json)
        if len(matches) > 0:
            return matches
            
        return False