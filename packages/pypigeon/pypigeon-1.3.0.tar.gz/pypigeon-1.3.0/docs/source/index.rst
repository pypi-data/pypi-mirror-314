Welcome to PyPigeon's documentation!
====================================

PyPigeon is an easy-to-use client library for interacting with a
Pigeon instance via Python.

Quickstart
----------

Install PyPigeon using pip on the command line:

.. code-block:: bash

  pip install pypigeon

Or in a Jupyter notebook cell::

  import sys
  !{sys.executable} -m pip install pypigeon

Then, log in to your Pigeon instance and get a client::

  from pypigeon import login
  client = login('pigeon.bioteam.net')  # Your Pigeon hostname

It will print out a URL to visit to activate your session. Clicking
the URL will take you to your Pigeon instance, where you will log in
and confirm that you want to activate this session. Once you do so,
the :py:func:`~pypigeon.client.login` method will return with the
activated client, and you can close your browser page or continue to
use it to navigate Pigeon.

With your client ready to go, you can interact with your Pigeon
collections, items, and tables::

  # Get a collection...
  collection = client.get_collection_by_name('MHSVI')

  # Get an item from the collection...
  item = collection["mh_svi_county_2018.csv"]

  # Get its table contents as a Pandas DataFrame
  dataframe = item.table()

  # Make a new dataframe
  import pandas as pd
  new_df = pd.DataFrame({"A": [1, 2, 3, 4, 5]})

  # Write the new dataframe as a new item
  collection.write_table("new-dataframe.csv", new_df, format="csv")


User Documentation
==================

PyPigeon offers three user interfaces to choose from:

* A high-level library which is focused on ease of use, available at
  :py:mod:`pypigeon`.

* A command-line utility named ``pcmd`` for scripting and general
  operations not otherwise handled by the Pigeon web interface.

* And a low-level library which is auto-generated from the Pigeon API
  definition and contains methods for every API endpoint, available at
  :py:mod:`pypigeon.pigeon_core`.


High-level :py:mod:`pypigeon` interface
---------------------------------------

.. toctree::
   :maxdepth: 2

   pypigeon_api


``pcmd`` command-line utility
-----------------------------

.. toctree::
   :maxdepth: 2

   pcmd_cli


Low-level :py:mod:`~pypigeon.pigeon_core` interface
---------------------------------------------------

.. toctree::
   :maxdepth: 2

   pigeon_core



Indices and tables
------------------

* :ref:`genindex`
* :ref:`modindex`
* :ref:`search`
