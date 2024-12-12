# PyPigeon

PyPigeon is an easy-to-use Python client for the Pigeon data commons
platform. It's great for scripts, notebooks, or as a foundation for
other clients to interact with Pigeon's public API.

# Quickstart

```
$ pip install pypigeon
$ python
>>> from pypigeon import login
>>> client = login('pigeon.bioteam.net')
To activate your session, visit the URL below:
   https://pigeon.bioteam.net/login/activate/........

Waiting for session activation...
>>> collection = client.get_collection_by_name('MHSVI')
>>> collection
<PigeonCollection: name=MHSVI version=LIVE id=...>
```

# Features

* Interact with collections, folders, and items
* Read and write data streams (raw files)
* Read and write data tables via Pandas DataFrames

Coming soon:

* Work with data elements
    * Persist data elements through DataFrames
* Work with dataviews (create, edit using simple construction tools)
