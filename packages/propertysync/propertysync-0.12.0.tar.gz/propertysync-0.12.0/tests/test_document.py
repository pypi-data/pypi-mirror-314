from propertysync.document import Document
from propertysync.document import SubdivisionLegal
from propertysync.document import AcreageLegal
from propertysync.document import Grantor
from propertysync.document import Grantee
from propertysync.document import BaseJsonElement

import json

def test_document():

    document_json = {
        "id": "074ed20e-5251-11ed-97c8-024203b4b07a",
        "json":
        {
            "tags":
            [
                "tag1",
                "tag2"
            ],
            "flags": None,
            "images":
            [],
            "status": None,
            "address":
            [],
            "comment": None,
            "company": None,
            "imageId": None,
            "related":
            [],
            "bookType": None,
            "grantees":
            [
                {
                    "nameLast": "MARTINSON",
                    "nameType": None,
                    "nameFirst": "ROBERT",
                    "nameMiddle": None
                },
                {
                    "nameLast": "SMITH",
                    "nameType": None,
                    "nameFirst": "JAMES",
                    "nameMiddle": None
                }
            ],
            "grantors":
            [
                {
                    "nameLast": "CRAWFORD",
                    "nameType": None,
                    "nameFirst": "STACI",
                    "nameMiddle": None
                }
            ],
            "recordId": None,
            "filedDate": "2019-06-17 00:00:00",
            "filedTime": None,
            "uccNumber": None,
            "bookNumber": None,
            "caseNumber": None,
            "filmNumber": None,
            "loanNumber": None,
            "pageNumber": None,
            "recordType": None,
            "userField1": None,
            "userField2": None,
            "userField3": None,
            "userField4": None,
            "userField5": None,
            "orderNumber": None,
            "otherFields": None,
            "propertyZip": None,
            "acreageLegal":
            [
                {
                    "arb":
                    [],
                    "lot": None,
                    "pid": None,
                    "unit": None,
                    "block": None,
                    "range": "24",
                    "action": "0",
                    "parcel": None,
                    "comment": None,
                    "recDate": None,
                    "section": "35",
                    "addition": None,
                    "bookType": None,
                    "landType": "0",
                    "quarters": "S2NENW; S2SENW;",
                    "township": "28",
                    "landFlags": "64",
                    "bookNumber": None,
                    "pageNumber": None,
                    "previousArb": None,
                    "subdivision": None,
                    "abstractName": None,
                    "abstractNumber": None,
                    "previousParcel": None
                }
            ],
            "checkedOutBy": None,
            "marketSource": None,
            "orderOfCourt": None,
            "propertyCity": None,
            "consideration": None,
            "propertyState": None,
            "instrumentDate": None,
            "instrumentType": "ORDER",
            "returnUnitType": None,
            "microFilmNumber": None,
            "indexingRecordId": None,
            "instrumentNumber": "12345678910",
            "propertyUnitType": None,
            "returnAddressZip": None,
            "returnStreetName": None,
            "returnStreetType": None,
            "returnUnitNumber": None,
            "subdivisionLegal":
            [
                {
                    "arb":
                    [],
                    "lot":
                    [
                        {
                            "rangeMax": "5",
                            "rangeMin": "1",
                            "rangeAction": None,
                            "rangePrecision": None
                        }
                    ],
                    "pid": None,
                    "unit":
                    [],
                    "block":
                    [],
                    "range": None,
                    "action": None,
                    "parcel": None,
                    "comment": None,
                    "recDate": None,
                    "addition": "ABIGAIL FARMS",
                    "bookType": None,
                    "landType": None,
                    "township": None,
                    "landFlags": "0",
                    "bookNumber": None,
                    "pageNumber": None,
                    "previousArb": None,
                    "subdivision": None,
                    "abstractName": None,
                    "abstractNumber": None,
                    "previousParcel": None
                }
            ],
            "returnAddressCity": None,
            "propertyStreetName": None,
            "propertyStreetType": None,
            "propertyUnitNumber": None,
            "returnAddressState": None,
            "returnStreetNumber": None,
            "propertyStreetNumber": None,
            "returnStreetDirection": None,
            "propertyStreetDirection": None
        }
    }

    doc = Document(json.dumps(document_json))

    # do this first, before we modify data
    assert doc.to_json() == json.dumps(document_json)

    assert doc.id == "074ed20e-5251-11ed-97c8-024203b4b07a"
    assert doc.subdivisionLegal[0].landFlags == "0"
    assert doc.subdivisionLegal[0].addition == "ABIGAIL FARMS"
    assert doc.acreageLegal[0].range == "24"
    assert doc.acreageLegal[0].section == "35"
    assert doc.acreageLegal[0].quarters == "S2NENW; S2SENW;"
    assert doc.acreageLegal[0].landFlags == "64"
    assert doc.acreageLegal[0].township == "28"

    assert doc.grantors[0].nameFirst == "STACI"
    assert doc.grantors[0].nameLast == "CRAWFORD"

    assert doc.grantees[0].nameFirst == "ROBERT"
    assert doc.grantees[0].nameLast == "MARTINSON"


    assert doc.tags[0] == "tag1"
    assert doc.tags[1] == "tag2"

    # make sure we can add a new subdivisionLegal
    doc.add_subdivision_legal(SubdivisionLegal({"addition": "Jimmy Bob's", "legal": "legal 3"}))
    assert len(doc.subdivisionLegal) == 2

    # make sure we can add a new acreageLegal
    doc.add_acreage_legal(AcreageLegal({"parcel": "1234", "legal": "legal 3"}))
    assert len(doc.acreageLegal) == 2

    # make sure we can add a new grantor
    doc.add_grantor(Grantor({"nameFirst": "John", "nameLast": "Smith"}))
    assert len(doc.grantors) == 2

    # make sure we can add a new grantee
    doc.add_grantee(Grantee({"nameFirst": "Jane", "nameLast": "Doe"}))
    assert len(doc.grantees) == 3

    # make sure we can add a new tag
    doc.add_tag("tag3")
    assert len(doc.tags) == 3

    # make sure we can remove a tag
    doc.tags.remove("tag3")
    assert len(doc.tags) == 2

    # test the has_tags method
    assert doc.has_tags(["tag1", "tag2"])
    assert not doc.has_tags(["tag1", "tag2", "tag3"])

    # test the replace method
    doc.replace("$.subdivisionLegal[?(@.addition=='ABIGAIL FARMS')].addition","ROB FARMS")
    assert doc.subdivisionLegal[0].addition == "ROB FARMS"


    