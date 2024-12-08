import json

"""
This is a helper class to build the search query for the PropertySync API.
"""

class Search:
    def __init__(self):
        self.recording_infos = []
        self.addresses = []
        self.parties = []
        self.subdivisions = []
        self.acreages = []
        self.marketsources = []
        self.parcels = []
        self.legals = []

        self.tags = []
        self.limit = None
        self.exclude_related_documents = True

    # search by tag
    def add_tag(self, tag):
        self.tags.append(tag)

    # add recording info
    def add_recording_info(self, instrument_type=None, instrument_page=None,instrument_number=None, book_type=None, book_number=None, book_page=None, case_number=None, file_number=None, start_date=None, end_date=None):
        recording_info = {}
        if instrument_type:
            recording_info["instrumentType"] = instrument_type
        if instrument_number:
            recording_info["instrumentNumber"] = instrument_number
        if instrument_page:
            recording_info["instrumentPage"] = instrument_page
        if book_type:
            recording_info["bookType"] = book_type
        if book_number:
            recording_info["book"] = book_number
        if book_page:
            recording_info["page"] = book_page
        if case_number:
            recording_info["caseNumber"] = case_number
        if file_number:
            recording_info["fileNumber"] = file_number
        if start_date:
            recording_info["dateFrom"] = start_date
        if end_date:
            recording_info["dateTo"] = end_date

        self.recording_infos.append(recording_info)

    # add parties
    def add_party(self, party_name=None,grantor_name=None, grantee_name=None, soundex=False, proximity=False):
        party = {}
        if grantor_name:
            party["grantorName"] = grantor_name
        if grantee_name:
            party["granteeName"] = grantee_name
        if party_name:
            party["partyName"] = party_name
        if soundex:
            party["soundexSearch"] = 1
        if proximity:
            party["proximitySearch"] = 1

        self.parties.append(party)

    # add subdivision
    def add_subdivision(self, addition=None, lot=None, block=None, unit=None, claim=None, mining_survey=None, arb=None, comment=None):
        subdivision = {}
        if addition:
            subdivision["addition"] = addition
        if lot:
            subdivision["lot"] = lot
        if block:
            subdivision["block"] = block
        if unit:
            subdivision["unit"] = unit
        if claim:
            subdivision["claim"] = claim
        if mining_survey:
            subdivision["miningSurvey"] = mining_survey
        if arb:
            subdivision["arb"] = arb
        if comment:
            subdivision["subdivisionComment"] = comment


        self.subdivisions.append(subdivision)

    # add parcel
    def add_parcel(self, number=None):
        parcel = {}
        if number:
            parcel["parcelNumber"] = number

        self.parcels.append(parcel)

    # add legal
    def add_legal(self, full_text_legal=None, parcel=None):
        legal = {}
        if full_text_legal:
            legal["fullTextLegal"] = full_text_legal
        self.legals.append(legal)

    # add acreage
    def add_acreage(self, section=None, township=None, range=None, quarter=None, arb=None, govlot=None, comment=None):
        acreage = {}
        if township:
            acreage["township"] = township
        if range:
            acreage["range"] = range
        if section:
            acreage["section"] = section
        if quarter:
            acreage["quarter"] = quarter
        if arb:
            acreage["arb"] = arb
        if govlot:
            acreage["govLot"] = govlot
        if comment:
            acreage["acreageComment"] = comment
        

        self.acreages.append(acreage)
  
    # add address
    def add_address(self, address=None, city=None, state=None, zip=None):
        addressRecord = {}
        if address:
            addressRecord["address"] = address
        if city:
            addressRecord["city"] = city
        if state:
            addressRecord["state"] = state
        if zip:
            addressRecord["zip"] = zip

        self.addresses.append(addressRecord)

    # limit the number of results
    def add_limit(self, limit):
        self.limit = limit

    # return the query
    def get_query(self):
        query = {
            "queryParams": {}
        }

        # add exclude related documents
        if self.exclude_related_documents:
            query["queryParams"]["excludeRelatedDocuments"] = 1

        # add tags
        if len(self.tags) > 0:
            query["queryParams"]["tags"] = self.tags
        
        # add record limit
        if self.limit:
            query["customLimit"] = self.limit

        # add recording info
        if len(self.recording_infos) > 0:
            query["queryParams"]["recordingInfos"] = self.recording_infos

        # add addresses
        if len(self.addresses) > 0:
            query["queryParams"]["addresses"] = self.addresses

        # add parties
        if len(self.parties) > 0:
            query["queryParams"]["parties"] = self.parties

        # add subdivision
        if len(self.subdivisions) > 0:
            query["queryParams"]["subdivisions"] = self.subdivisions

        # add acreage
        if len(self.acreages) > 0:
            query["queryParams"]["acreages"] = self.acreages

        # add parcels
        if len(self.parcels) > 0:
            query["queryParams"]["parcels"] = self.parcels

        # add legals
        if len(self.legals) > 0:
            query["queryParams"]["legals"] = self.legals

        return query
