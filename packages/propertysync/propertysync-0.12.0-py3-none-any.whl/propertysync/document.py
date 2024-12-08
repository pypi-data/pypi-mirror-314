import json
from jsonpath_ng import jsonpath
from jsonpath_ng.ext import parse

"""
This is a helper class for working with PropertySync documents.
"""

# define a base class for all json elements
class BaseJsonElement(dict):
    def __init__(self, json_string=None):
        if json_string:
            # if json_string is a string, load it into the dictionary
            if isinstance(json_string, str):
                self.__dict__ = json.loads(json_string)
            # if json_string is a dictionary, load it into the dictionary
            elif isinstance(json_string, dict):
                self.__dict__ = json_string
            else:
                raise TypeError("json_string must be a string or dictionary")
            
        super().__init__(self)

    # magic method to find items in the json if they are not already attributes
    def __getattr__(self, item):
        # if we have a json attribute that contains the item, return it
        if "json" in self.__dict__ and item in self.__dict__["json"]:
            return self.__dict__["json"][item]
        
    # magic method to set the value
    def __setattr__(self, key, value):
        # if we have a json attribute, set the value there
        if "json" in self.__dict__:
            self.__dict__["json"][key] = value
        # otherwise, set the value in the object
        else:
            self.__dict__[key] = value

        # prevent recursion 
        super().__setattr__(key, value)
        
    
    def __setitem__(self, key, value):
        super().__setitem__(key, value)

    def __getitem__(self, key):  
        return super().__getitem__(key)

    def __str__(self):
        return super().__str__()

    def items(self):
        yield from super().items()

    def keys(self):
        yield from super().keys()

    # if we try to convert this object to json, return the json string
    def __str__(self):
        return self.to_json()

    # if we try to convert this object to json, return the json string
    def __repr__(self):
        return self.to_json()

    # deprecated method
    def get_json(self):
        return self.to_json()
    
    def to_json(self):
        # dump the dictionary to json, hiding any private variables
        return json.dumps({k: v for k, v in self.__dict__.items() if not k.startswith("_")})
        
class Legal(BaseJsonElement):
    def __init__(self, json_string=None):
        super().__init__(json_string)

class SubdivisionLegal(Legal):
    def __init__(self, json_string=None):
        super().__init__(json_string)

class AcreageLegal(Legal):
    def __init__(self, json_string=None):
        super().__init__(json_string)

class Party(BaseJsonElement):
    def __init__(self, json_string=None):
        self.nameFirst = None
        self.nameLast = None
        self.nameMiddle = None
        self.nameType = None
        super().__init__(json_string)

class Grantor(Party):
    def __init__(self, json_string=None):
        super().__init__(json_string)

class Grantee(Party):
    def __init__(self, json_string=None):
        super().__init__(json_string)

class Document(BaseJsonElement):
    def __init__(self, json_string=None):
        super().__init__(json_string)

    # subdivisionLegal
    @property
    def subdivisionLegal(self):
        # return a list of SubdivisionLegal objects
        return [SubdivisionLegal(x) for x in self.json["subdivisionLegal"]]
    
    @subdivisionLegal.setter
    def subdivisionLegal(self, value):
        # value should be a list of SubdivisionLegal objects
        self.json["subdivisionLegal"] = [x.to_json() for x in value]

    # add_subdivision_legal
    def add_subdivision_legal(self, subdivision_legal):
        # subdivision_legal should be a SubdivisionLegal object
        self.json["subdivisionLegal"].append(subdivision_legal.to_json())

    # acreageLegal
    @property
    def acreageLegal(self):
        # return a list of AcreageLegal objects
        return [AcreageLegal(x) for x in self.json["acreageLegal"]]
    
    @acreageLegal.setter
    def acreageLegal(self, value):
        # value should be a list of AcreageLegal objects
        self.json["acreageLegal"] = [x.to_json() for x in value]

    # add_acreage_legal
    def add_acreage_legal(self, acreage_legal):
        # acreage_legal should be a AcreageLegal object
        self.json["acreageLegal"].append(acreage_legal.to_json())

    # grantors
    @property
    def grantors(self):
        # return a list of Grantor objects
        return [Grantor(x) for x in self.json["grantors"]]
    
    @grantors.setter
    def grantors(self, value):
        # value should be a list of Grantor objects
        self.json["grantors"] = [x.to_json() for x in value]

    # add_grantor
    def add_grantor(self, grantor):
        # grantor should be a Grantor object
        self.json["grantors"].append(grantor.to_json())

    # grantees
    @property
    def grantees(self):
        # return a list of Grantee objects
        return [Grantee(x) for x in self.json["grantees"]]

    @grantees.setter
    def grantees(self, value):
        # value should be a list of Grantee objects
        self.json["grantees"] = [x.to_json() for x in value]

    # add_grantee   
    def add_grantee(self, grantee):
        # grantee should be a Grantee object
        self.json["grantees"].append(grantee.to_json())

    # tags
    @property
    def tags(self):
        return self.json["tags"]
    
    @tags.setter
    def tags(self, value):
        self.json["tags"] = value

    # add a tag to this document
    def add_tag(self, tag):
        if tag not in self.tags:
            self.tags.append(tag)

    # has this document been tagged with a specific tag?
    def has_tags(self, tags):
        for tag in tags:
            if tag not in self.tags:
                return False
        return True

    # serialize the document to json, this is just for backwards compatibility
    def get_json(self):
        return self.to_json()
    
    # return subdivisionlegals where parcel matches a value
    def subdivisionlegals_with_parcel(self, parcel):
        return [legal for legal in self.subdivisionLegal if legal["parcel"] == parcel]
    
    # replace  with "value" in "json_path" for this document 
    def replace(self, json_path, value):
        jsonpath_expr = parse(json_path)
        jsonpath_expr.find(self.json)
        jsonpath_expr.update(self.json, value)
                
    # find all nodes in the document that have a specific value
    def find(self, json_path):
        jsonpath_expr = parse(json_path)
        matches = jsonpath_expr.find(self.json)
        if len(matches) > 0:
            return matches
            
        return False
    