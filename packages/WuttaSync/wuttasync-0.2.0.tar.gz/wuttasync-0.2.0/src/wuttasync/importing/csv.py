# -*- coding: utf-8; -*-
################################################################################
#
#  WuttaSync -- Wutta Framework for data import/export and real-time sync
#  Copyright © 2024 Lance Edgar
#
#  This file is part of Wutta Framework.
#
#  Wutta Framework is free software: you can redistribute it and/or modify it
#  under the terms of the GNU General Public License as published by the Free
#  Software Foundation, either version 3 of the License, or (at your option) any
#  later version.
#
#  Wutta Framework is distributed in the hope that it will be useful, but
#  WITHOUT ANY WARRANTY; without even the implied warranty of MERCHANTABILITY or
#  FITNESS FOR A PARTICULAR PURPOSE.  See the GNU General Public License for
#  more details.
#
#  You should have received a copy of the GNU General Public License along with
#  Wutta Framework.  If not, see <http://www.gnu.org/licenses/>.
#
################################################################################
"""
Importing from CSV
"""

import csv
import logging
import uuid as _uuid
from collections import OrderedDict

from sqlalchemy_utils.functions import get_primary_keys

from wuttjamaican.db.util import make_topo_sortkey, UUID

from .base import FromFile
from .handlers import FromFileHandler
from .wutta import ToWuttaHandler
from .model import ToWutta


log = logging.getLogger(__name__)


class FromCsv(FromFile):
    """
    Base class for importer/exporter using CSV file as data source.

    Note that this assumes a particular "format" for the CSV files.
    If your needs deviate you should override more methods, e.g.
    :meth:`open_input_file()`.

    The default logic assumes CSV file is mostly "standard" - e.g.
    comma-delimited, UTF-8-encoded etc.  But it also assumes the first
    line/row in the file contains column headers, and all subsequent
    lines are data rows.

    .. attribute:: input_reader

       While the input file is open, this will reference a
       :class:`python:csv.DictReader` instance.
    """

    csv_encoding = 'utf_8'
    """
    Encoding used by the CSV input file.

    You can specify an override if needed when calling
    :meth:`~wuttasync.importing.handlers.ImportHandler.process_data()`.
    """

    def get_input_file_name(self):
        """
        By default this returns the importer/exporter model name plus
        CSV file extension, e.g. ``Widget.csv``

        It calls
        :meth:`~wuttasync.importing.base.Importer.get_model_title()`
        to obtain the model name.
        """
        if hasattr(self, 'input_file_name'):
            return self.input_file_name

        model_title = self.get_model_title()
        return f'{model_title}.csv'

    def open_input_file(self):
        """
        Open the input file for reading, using a CSV parser.

        This tracks the file handle via
        :attr:`~wuttasync.importing.base.FromFile.input_file` and the
        CSV reader via :attr:`input_reader`.

        It also updates the effective
        :attr:`~wuttasync.importing.base.Importer.fields` list per the
        following logic:

        First get the current effective field list, e.g. as defined by
        the class and/or from caller params.  Then read the column
        header list from CSV file, and discard any which are not found
        in the first list.  The result becomes the new effective field
        list.
        """
        path = self.get_input_file_path()
        log.debug("opening input file: %s", path)
        self.input_file = open(path, 'rt', encoding=self.csv_encoding)
        self.input_reader = csv.DictReader(self.input_file)

        # nb. importer may have all supported fields by default, so
        # must prune to the subset also present in the input file
        fields = self.get_fields()
        orientation = self.orientation.value
        log.debug(f"supported fields for {orientation}: %s", fields)
        self.fields = [f for f in self.input_reader.fieldnames or []
                       if f in fields]
        log.debug("fields present in source data: %s", self.fields)
        if not self.fields:
            self.input_file.close()
            raise ValueError("input file has no recognized fields")

    def close_input_file(self):
        """ """
        self.input_file.close()
        del self.input_reader
        del self.input_file

    def get_source_objects(self):
        """
        This returns a list of data records "as-is" from the CSV
        source file (via :attr:`input_reader`).

        Since this uses :class:`python:csv.DictReader` by default,
        each record will be a dict with key/value for each column in
        the file.
        """
        return list(self.input_reader)


class FromCsvToSqlalchemyMixin:
    """
    Mixin class for CSV → SQLAlchemy ORM :term:`importers <importer>`.

    Meant to be used by :class:`FromCsvToSqlalchemyHandlerMixin`.

    This mixin adds some logic to better handle ``uuid`` key fields
    which are of :class:`~wuttjamaican:wuttjamaican.db.util.UUID` data
    type (i.e. on the target side).  Namely, when reading ``uuid``
    values as string from CSV, convert them to proper UUID instances,
    so the key matching between source and target will behave as
    expected.
    """

    def __init__(self, config, **kwargs):
        super().__init__(config, **kwargs)

        # nb. keep track of any key fields which use proper UUID type
        self.uuid_keys = []
        for field in self.get_keys():
            attr = getattr(self.model_class, field)
            if len(attr.prop.columns) == 1:
                if isinstance(attr.prop.columns[0].type, UUID):
                    self.uuid_keys.append(field)

    def normalize_source_object(self, obj):
        """ """
        data = dict(obj)

        # nb. convert to proper UUID values so key matching will work
        # properly, where applicable
        for key in self.uuid_keys:
            uuid = data[key]
            if uuid and not isinstance(uuid, _uuid.UUID):
                data[key] = _uuid.UUID(uuid)

        return data


class FromCsvToSqlalchemyHandlerMixin:
    """
    Mixin class for CSV → SQLAlchemy ORM :term:`import handlers
    <import handler>`.

    This knows how to dynamically generate :term:`importer` classes to
    target the particular ORM involved.  Such classes will inherit
    from :class:`FromCsvToSqlalchemyMixin`, in addition to whatever
    :attr:`FromImporterBase` and :attr:`ToImporterBase` reference.

    This all happens within :meth:`define_importers()`.
    """
    source_key = 'csv'
    generic_source_title = "CSV"

    FromImporterBase = FromCsv
    """
    This must be set to a valid base class for the CSV source side.
    Default is :class:`FromCsv` which should typically be fine; you
    can change if needed.
    """

    # nb. subclass must define this
    ToImporterBase = None
    """
    For a handler to use this mixin, this must be set to a valid base
    class for the ORM target side.  The :meth:`define_importers()`
    logic will use this as base class when dynamically generating new
    importer/exporter classes.
    """

    def get_target_model(self):
        """
        This should return the :term:`app model` or a similar module
        containing data model classes for the target side.

        The target model is used to dynamically generate a set of
        importers (e.g. one per table in the target DB) which can use
        CSV file as data source.  See also :meth:`define_importers()`.

        Subclass must override this if needed; default behavior is not
        implemented.
        """
        raise NotImplementedError

    def define_importers(self):
        """
        This mixin overrides typical (manual) importer definition, and
        instead dynamically generates a set of importers, e.g. one per
        table in the target DB.

        It does this based on the target model, as returned by
        :meth:`get_target_model()`.  It calls
        :meth:`make_importer_factory()` for each model class found.
        """
        importers = {}
        model = self.get_target_model()

        # mostly try to make an importer for every data model
        for name in dir(model):
            cls = getattr(model, name)
            if isinstance(cls, type) and issubclass(cls, model.Base) and cls is not model.Base:
                importers[name] = self.make_importer_factory(cls, name)

        # sort importers according to schema topography
        topo_sortkey = make_topo_sortkey(model)
        importers = OrderedDict([
            (name, importers[name])
            for name in sorted(importers, key=topo_sortkey)
        ])

        return importers

    def make_importer_factory(self, model_class, name):
        """
        Generate and return a new :term:`importer` class, targeting
        the given :term:`data model` class.

        The newly-created class will inherit from:

        * :class:`FromCsvToSqlalchemyMixin`
        * :attr:`FromImporterBase`
        * :attr:`ToImporterBase`

        :param model_class: A data model class.

        :param name: The "model name" for the importer/exporter.  New
           class name will be based on this, so e.g. ``Widget`` model
           name becomes ``WidgetImporter`` class name.

        :returns: The new class, meant to process import/export
           targeting the given data model.
        """
        return type(f'{name}Importer',
                    (FromCsvToSqlalchemyMixin, self.FromImporterBase, self.ToImporterBase), {
            'model_class': model_class,
            'key': list(get_primary_keys(model_class)),
        })


class FromCsvToWutta(FromCsvToSqlalchemyHandlerMixin, FromFileHandler, ToWuttaHandler):
    """
    Handler for CSV → Wutta :term:`app database` import.

    This uses :class:`FromCsvToSqlalchemyHandlerMixin` for most of the
    heavy lifting.
    """
    ToImporterBase = ToWutta

    def get_target_model(self):
        """ """
        return self.app.model
