from propertysync.batch import Batch
from propertysync.document import Document

import json

def test_batch():


    batch_json = {
        "id": "0720b1f8-838e-4b99-8048-b1400cd4b2ab",
        "documentGroupId": "41cbc5b8-0015-11ea-93e1-0a58a9feac2a",
        "createdAt": "2023-04-20T18:41:38.000000Z",
        "updatedAt": "2023-04-20T18:41:38.000000Z",
        "name": "ABIGAIL FARMS",
        "createdBy": "property-sync",
        "lastModifiedBy": "property-sync",
        "lastModifiedAt": "2023-04-20T18:41:38.000000Z",
        "numOfDocs": 2,
        "numOfCompletedDocs": 2,
        "recordedDate": None,
        "rawFileGroupType": "9388501a-1ac4-4dd7-8a97-014747c042a6",
        "documents": [
            {
                "id": "41cbc5b8-0015-11ea-93e1-0a58a9feac2a",
                "json": {   
                    "instrumentType": "Deed",
                    "instrumentNumber": "123456789",
                    "subdivisionLegal": [
                        {
                            "addition":"ABIGAIL FARMS"
                        }
                    ],
                    "tags": ["tag1", "tag2"]
                }
            },
            {
                "id": "41cbc5b8-0015-11ea-93e1-0a58a9feac2a",
                "json": {
                    
                    "instrumentType": "Warranty Deed",
                    "instrumentNumber": "123456780",
                    "tags": ["RIS", "LOCATE"]
                }
            }
        ]
    }

    # create a batch
    batch = Batch(json.dumps(batch_json))

    # do this first, before we modify data
    assert batch.to_json() == json.dumps(batch_json)
    
    # test legacy methods
    assert batch.get_json() == json.dumps(batch_json)

    assert batch.id == "0720b1f8-838e-4b99-8048-b1400cd4b2ab"
    assert len(batch.documents) == 2
    assert batch.documents[0].id == "41cbc5b8-0015-11ea-93e1-0a58a9feac2a"

    # these two should be the same
    assert batch.documents[0].json["instrumentType"] == "Deed"
    assert batch.documents[0].instrumentType == "Deed"

    # now change the value of instrumentType using the property
    batch.documents[0].instrumentType = "Warranty Deed"

    # these two should be the same
    assert batch.documents[0].json["instrumentType"] == "Warranty Deed"
    assert batch.documents[0].instrumentType == "Warranty Deed"

    # see if documents[0] is a Document object, defined in propertysync/document.py
    assert isinstance(batch.documents[0], Document)

    # test tags
    assert batch.documents[0].has_tags(["tag1", "tag2"])
    assert batch.documents[0].tags == ["tag1", "tag2"]
    batch.documents[0].add_tag("tag3")
    assert batch.documents[0].tags == ["tag1", "tag2", "tag3"]

    # test find
    # find all documents with instrumentType == "Warranty Deed", this should now be two because we modified a document above
    assert len(batch.find_documents("$.instrumentType", "Warranty Deed")) == 2

    # find all documents with instrumentType == "Deed" and change to "Warranty Deed", this is via a loop
    for doc in batch.find_documents("$.instrumentType", "Warranty Deed"):
        doc.instrumentType = "LIEN"

    # using batch json replace, find all documents with instrumentType == "LIEN" and replace with "MASTER DEED"
    # this changes json in the batch, but not the Document object, actually it looks like this isn't working at all
    # batch.replace("$.documents[?(@.instrumentType=='LIEN')].instrumentType", "MASTER DEED")

    print (batch.to_json())
    for doc in batch.documents :
        print (doc.to_json())

    # for some reason, the line above changes the json, but not the Document object
    assert len(batch.find_documents("$.instrumentType", "LIEN")) == 2

    # replace all instrumentTypes with MASTER DEED
    batch.replace_in_documents("$.instrumentType", "MASTER DEED")

    # verify that the instrumentType was changed
    assert len(batch.find_documents("$.instrumentType", "MASTER DEED")) == 2

    # replace all instrumentTypes with MASTER DEED where instrumentNumber == 123456789
    batch.replace_in_documents("$.instrumentType", "WARRANTY DEED", "$.instrumentNumber", "123456789")

    # verify that the instrumentType was changed
    assert len(batch.find_documents("$.instrumentType", "WARRANTY DEED")) == 1 

