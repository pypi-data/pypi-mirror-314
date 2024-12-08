
===================
 Built-in Commands
===================

Below are the :term:`subcommands <subcommand>` which come with
WuttaSync.

It is fairly simple to add more; see :doc:`custom`.


.. _wutta-import-csv:

``wutta import-csv``
--------------------

Import data from CSV file(s) to the Wutta :term:`app database`.

This *should* be able to automatically target any table mapped in the
:term:`app model`.  The only caveat is that it is "dumb" and does not
have any special field handling.  This means the column headers in the
CSV file must be named the same as in the target table, and some data
types may not behave as expected etc.

Defined in: :mod:`wuttasync.cli.import_csv`

.. program-output:: wutta import-csv --help
