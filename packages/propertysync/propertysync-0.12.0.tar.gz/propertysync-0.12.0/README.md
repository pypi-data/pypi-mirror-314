# PropertySync Python Client

[![PyPI version](https://badge.fury.io/py/propertysync.svg)](https://badge.fury.io/py/propertysync)
[![PyPI](https://img.shields.io/pypi/pyversions/propertysync.svg)](https://pypi.python.org/pypi/propertysync)

This is a python packagefor working with the [PropertySync API](https://developer.propertysync.com/api.html).

## Installation

```console
pip install propertysync
```

## Usage
```python
import propertysync

# Create a connection to the API
# ---
# *Note:* email and password will be retrieved from Psync environment variables if not 
# provided on this line and if available. Those are: PROPERTYSYNC_API_EMAIL, PROPERTYSYNC_API_PASSWORD
api = propertysync.ApiClient('your_email', 'your_password')

# Set the correct document group
api.set_document_group_id("your_document_group_id")

# Get document group info
document_group_info = api.get_document_group_info()

# get all additions
additions = api.get_autocompletes("addition")

# run a search where the address is 123 Main St
search = propertysync.Search()
search.add_address("123 Main St")

search_results = api.run_search(search.get_query())

```