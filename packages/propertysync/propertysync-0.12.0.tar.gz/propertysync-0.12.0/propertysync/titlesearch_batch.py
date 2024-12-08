import json, csv, os
from datetime import datetime

# This is a helper that will convert from a titlesearch batch to a PropertySync batch

class TitleSearchBatch:

    def __init__(self, titlesearch_batch_file=None):
        self._json = {}

        self.batch_fields = (
            "recordId", "documentNumber", "bookType", "bookNumber", "pageNumber", "filedDate", "filedTime", "instrumentDate",
            "instrumentType", "consideration", "generalComment", "marketSource", "companyName", "caseNumber", "uccNumber",
            "microFilmNumber", "loanNumber", "grantor", "grantee", "arbitraryNumber", "unit", "lot", "block", "addition",
            "subdivision",
            "platType", "platBookNumber", "platPageNumber", "landComment", "quarters", "section", "township", "range",
            "abstractNumber", "abstractName", "parcelNumber", "propertyIdentificationNumber", "previousParcelNumber",
            "previousArbitraryNumber", "relatedDocumentNumber", "relatedBookType", "relatedBookNumber", "relatedPageNumber",
            "relatedInstrumentType", "imageNumber", "imagePath", "imageName", "propertyStreetNumber", "propertyStreetDirection",
            "propertyStreetName", "propertyStreetType", "propertyUnitType", "propertyUnitNumber", "propertyCity",
            "propertyState",
            "propertyZip", "returnStreetNumber", "returnStreetDirection", "returnStreetName", "returnStreetType",
            "returnUnitType", "returnUnitNumber", "returnAddressCity", "returnAddressState", "returnAddressZip",
            "userField1", "userField2", "userField3", "userField4", "userField5",
        )

        self.related_fields = (
            "relatedDocumentNumber", "relatedBookType", "relatedBookNumber", "relatedPageNumber", "relatedInstrumentType",
        )

        self.legal_fields = (
            "arbitraryNumber", "unit", "lot", "block", "addition", "subdivision", "platType", "platBookNumber",
            "platPageNumber",
            "landComment", "quarters", "section", "township", "range", "abstractNumber", "abstractName", "parcelNumber",
        )

        # if the file exists, then convert it to a PropertySync batch
        if os.path.exists(titlesearch_batch_file):
            self._json = self.convert_batch(titlesearch_batch_file)

    def get_json(self):
        return self._json

    def has_field(self, row, fields):
        for field in fields:
            if row[field]:
                return True
        return False

    def parse_date(self, value):
        if value:
            # try to convert value to a date, if this throws an exception, then just return the value
            try:
                time = datetime.strptime(value, '%m%d%Y')
                return time.strftime('%Y-%m-%d')
            except:
                return value
        return value

    def parse_party_name(self, value):
        split_name = {
            'name_last': None,
            'name_first': None,
            'name_middle': None,
        }

        if ',' in value:
            name_parts = value.split(',')

            if len(name_parts) == 2:
                split_name['name_last'] = name_parts[0].strip()

                first_middle = name_parts[1].strip().split(' ')
                split_name['name_first'] = first_middle[0].strip()

                first_middle.remove(first_middle[0])
                split_name['name_middle'] = ' '.join(x for x in first_middle)
                if not split_name['name_middle']:
                    split_name['name_middle'] = None
            else:
                split_name['name_last'] = value.strip()
        else:
            split_name['name_last'] = value.strip()

        return split_name


    def parse_legal(self, record, row, append=False):
        if not self.has_field(row, self.legal_fields):
            return

        subdivision = False
        if row['addition']:
            subdivision = True

        if subdivision:
            self.parse_subdivision_legal(record, row, append)
        else:
            self.parse_acreage_legal(record, row, append)

    def parse_subdivision_legal(self, record, row, append):
        record_info = {
            'abstractName': row['abstractName'] or None,
            'abstractNumber': row['abstractNumber'] or None,
            'action': None,
            'addition': row['addition'] or None,
            'arb': [],
            'block': [],
            'bookNumber': row['bookNumber'] or None,
            'bookType': row['bookType'] or None,
            'comment': row['landComment'] or None,
            'landFlags': None,
            'landType': None,
            'lot': [],
            'mineral': False,
            'pageNumber': row['pageNumber'] or None,
            'parcel': row['parcelNumber'] or None,
            'pid': row['propertyIdentificationNumber'] or None,
            'previousArb': row['previousArbitraryNumber'] or None,
            'previousParcel': row['previousParcelNumber'] or None,
            'range': row['range'] or None,
            'recDate': None,
            'township': row['township'] or None,
            'unit': [],
        }
        if append:
            if row['arbitraryNumber']:
                record_info['arb'].append(
                    {"rangeAction": None, "rangeMax": row['arbitraryNumber'], "rangeMin": row['arbitraryNumber'],
                    "rangePrecision": None})

            if row['block']:
                record_info['block'].append(
                    {"rangeAction": None, "rangeMax": row['block'], "rangeMin": row['block'], "rangePrecision": None})

            if row['lot']:
                record_info['lot'].append(
                    {"rangeAction": None, "rangeMax": row['lot'], "rangeMin": row['lot'], "rangePrecision": None})

            if row['unit']:
                record_info['unit'].append(
                    {"rangeAction": None, "rangeMax": row['unit'], "rangeMin": row['unit'], "rangePrecision": None})
        else:
            if row['arbitraryNumber']:
                record_info['arb'] = [
                    {"rangeAction": None, "rangeMax": row['arbitraryNumber'], "rangeMin": row['arbitraryNumber'],
                    "rangePrecision": None}
                ]

            if row['block']:
                record_info['block'] = [
                    {"rangeAction": None, "rangeMax": row['block'], "rangeMin": row['block'], "rangePrecision": None}
                ]

            if row['lot']:
                record_info['lot'] = [
                    {"rangeAction": None, "rangeMax": row['lot'], "rangeMin": row['lot'], "rangePrecision": None}
                ]

            if row['unit']:
                record_info['unit'] = [
                    {"rangeAction": None, "rangeMax": row['unit'], "rangeMin": row['unit'], "rangePrecision": None}
                ]

        record['subdivisionLegal'].append(record_info)


    def parse_acreage_legal(self,record, row, append):
        record_info = {
            'abstractName': row['abstractName'] or None,
            'abstractNumber': row['abstractNumber'] or None,
            'action': None,
            'addition': None,
            'arb': None,
            'block': None,
            'bookNumber': None,
            'bookType': row['bookType'] or None,
            'comment': row['landComment'] or None,
            'landFlags': None,
            'landType': None,
            'govLot': [],
            'mineral': False,
            'pageNumber': None,
            'parcel': row['parcelNumber'] or None,
            'pid': row['propertyIdentificationNumber'] or None,
            'previousArb': row['previousArbitraryNumber'] or None,
            'previousParcel': row['previousParcelNumber'] or None,
            'quarters': row["quarters"] or None,
            'range': row['range'] or None,
            'recDate': None,
            'section': row['section'] or None,
            'township': row['township'] or None,
            'unit': None,
        }
        if append:
            if row['lot']:
                record_info['govLot'].append(
                    {"rangeAction": None, "rangeMax": row['lot'], "rangeMin": row['lot'], "rangePrecision": None})
        else:
            if row['lot']:
                record_info['govLot'] = [
                    {"rangeAction": None, "rangeMax": row['lot'], "rangeMin": row['lot'], "rangePrecision": None}
                ]

        record['acreageLegal'].append(record_info)


    def convert_batch(self, batchFilePath, batchName = None):
        records = []

        # if batchName is not provided, use the filename without the extension
        if not batchName:
            batchName = os.path.splitext(os.path.basename(batchFilePath))[0]

        csv.register_dialect('piper', delimiter='|', quoting=csv.QUOTE_NONE)

        # read batch file
        with open(batchFilePath) as csvf:
            batchReader = csv.DictReader(csvf, fieldnames=self.batch_fields, dialect='piper')
            prev_id = None
            curr_id = None

            # add each row to our table
            for row in batchReader:
                if curr_id:
                    prev_id = int(curr_id)
                curr_id = int(row["recordId"])

                if curr_id != prev_id:
                    record = {
                        "indexingRecordId": None,
                        "instrumentNumber": row["documentNumber"] or None,
                        "bookType": row['bookType'] or None,
                        "bookNumber": row['bookNumber'] or None,
                        "pageNumber": row['pageNumber'] or None,
                        "filedDate": self.parse_date(row['filedDate']) or None,
                        "filedTime": row['filedTime'] or None,
                        "instrumentDate": self.parse_date(row['instrumentDate']) or None,
                        "instrumentType": row["instrumentType"] or None,
                        "consideration": row['consideration'] or None,
                        "comment": row['generalComment'] or None,
                        "marketSource": row['marketSource'] or None,
                        "company": row['companyName'] or None,
                        "caseNumber": row['caseNumber'] or None,
                        "uccNumber": row['uccNumber'] or None,
                        "microFilmNumber": row['microFilmNumber'] or None,
                        "loanNumber": row['loanNumber'] or None,
                        "propertyStreetNumber": row['propertyStreetNumber'] or None,
                        "propertyStreetDirection": row['propertyStreetDirection'] or None,
                        "propertyStreetName": row['propertyStreetName'] or None,
                        "propertyStreetType": row['propertyStreetType'] or None,
                        "propertyUnitType": row['propertyUnitType'] or None,
                        "propertyUnitNumber": row['propertyUnitNumber'] or None,
                        "propertyCity": row['propertyCity'] or None,
                        "propertyState": row['propertyState'] or None,
                        "propertyZip": row['propertyZip'] or None,
                        "returnStreetNumber": row['returnStreetNumber'] or None,
                        "returnStreetDirection": row['returnStreetDirection'] or None,
                        "returnStreetName": row['returnStreetName'] or None,
                        "returnStreetType": row['returnStreetType'] or None,
                        "returnUnitType": row['returnUnitType'] or None,
                        "returnUnitNumber": row['returnUnitNumber'] or None,
                        "returnCity": row['returnAddressCity'] or None,
                        "returnState": row['returnAddressState'] or None,
                        "returnZip": row['returnAddressZip'] or None,
                        "userField1": row['userField1'] or None,
                        "userField2": row['userField2'] or None,
                        "userField3": row['userField3'] or None,
                        "userField4": row['userField4'] or None,
                        "userField5": row['userField5'] or None,
                        "status": None,
                        "checkedOutBy": None,
                        "flags": None,
                        "imageId": None,
                        "acreageLegal": [],
                        "subdivisionLegal": [],
                        "grantors": [],
                        "grantees": [],
                        "related": [],
                        "images": [],
                        "tags": row['userField5'] or None,
                    }

                    if row['grantor']:
                        split_name = self.parse_party_name(row["grantor"])
                        record['grantors'] = [
                            {"nameFirst": split_name['name_first'], "nameLast": split_name['name_last'],
                            "nameMiddle": split_name['name_middle'], "nameType": None}
                        ]

                    if row['grantee']:
                        split_name = self.parse_party_name(row['grantee'])
                        record['grantees'] = [
                            {"nameFirst": split_name['name_first'], "nameLast": split_name['name_last'],
                            "nameMiddle": split_name['name_middle'], "nameType": None}
                        ]

                    if self.has_field(row, self.related_fields):
                        record['related'] = [
                            {
                                "bookNumber": row['relatedBookNumber'] or None,
                                "bookType": row['relatedBookType'] or None,
                                "instrumentType": row['relatedInstrumentType'] or None,
                                "instrumentNumber": row['relatedDocumentNumber'] or None,
                                "pageNumber": row['relatedPageNumber'] or None
                            }
                        ]

                    self.parse_legal(record, row)
                    records.append(record)
                else:
                    record = records[len(records) - 1]
                    if row['grantor']:
                        split_name = self.parse_party_name(row["grantor"])
                        record["grantors"].append(
                            {"nameFirst": split_name['name_first'], "nameLast": split_name['name_last'],
                            "nameMiddle": split_name['name_middle'], "nameType": None})

                    if row['grantee']:
                        split_name = self.parse_party_name(row['grantee'])
                        record["grantees"].append(
                            {"nameFirst": split_name['name_first'], "nameLast": split_name['name_last'],
                            "nameMiddle": split_name['name_middle'], "nameType": None})

                    if self.has_field(row, self.related_fields):
                        record["related"].append(
                            {
                                "bookNumber": row['relatedBookNumber'] or None,
                                "bookType": row['relatedBookType'] or None,
                                "instrumentType": row['relatedInstrumentType'] or None,
                                "instrumentNumber": row['relatedDocumentNumber'] or None,
                                "pageNumber": row['relatedPageNumber'] or None
                            }
                        )

                    self.parse_legal(record, row, append=True)

        batchStructure = []
        for document in records:
            batchStructure.append({'json': document})

        # dump documents here to sort it only, sorting is not required but makes reading the json structure easier
        return { 'name': batchName, 'documents': json.loads(json.dumps(batchStructure, indent=2, sort_keys=True)) }

