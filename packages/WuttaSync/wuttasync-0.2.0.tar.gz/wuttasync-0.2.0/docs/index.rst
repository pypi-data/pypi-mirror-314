
WuttaSync
=========

This package adds data import/export and real-time sync utilities for
the `Wutta Framework <https://wuttaproject.org>`_.

*(NB. the real-time sync has not been added yet.)*

The primary use cases in mind are:

* keep operational data in sync between various business systems
* import data from user-specified file
* export to file

This isn't really meant to replace typical ETL tools; it is smaller
scale and (hopefully) more flexible.

While it of course supports import/export to/from the Wutta :term:`app
database`, it may be used for any "source → target" data flow.


.. toctree::
   :maxdepth: 2
   :caption: Documentation

   glossary
   narr/install
   narr/cli/index
   narr/concepts
   narr/custom/index

.. toctree::
   :maxdepth: 1
   :caption: API

   api/wuttasync
   api/wuttasync.cli
   api/wuttasync.cli.base
   api/wuttasync.cli.import_csv
   api/wuttasync.importing
   api/wuttasync.importing.base
   api/wuttasync.importing.csv
   api/wuttasync.importing.handlers
   api/wuttasync.importing.model
   api/wuttasync.importing.wutta
   api/wuttasync.util
