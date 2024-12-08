.. _glossary:

Glossary
========

.. glossary::
   :sorted:

   import handler
     This a type of :term:`handler` which is responsible for a
     particular set of data import/export task(s).

     The import handler manages data connections and transactions, and
     invokes one or more :term:`importers <importer>` to process the
     data.  See also :ref:`import-handler-vs-importer`.

     Note that "import/export handler" is the more proper term to use
     here but it is often shortened to just "import handler" for
     convenience.

   importer
     This refers to a Python class/instance responsible for processing
     a particular :term:`data model` for an import/export job.

     For instance there is usually one importer per table, when
     importing to the :term:`app database` (regardless of source).
     See also :ref:`import-handler-vs-importer`.

     Note that "importer/exporter" is the more proper term to use here
     but it is often shortened to just "importer" for convenience.
