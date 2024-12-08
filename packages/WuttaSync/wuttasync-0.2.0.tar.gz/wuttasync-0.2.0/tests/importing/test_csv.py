#-*- coding: utf-8; -*-

import csv
import uuid as _uuid
from unittest.mock import patch

from wuttjamaican.testing import DataTestCase

from wuttasync.importing import csv as mod, ImportHandler, ToSqlalchemyHandler, ToSqlalchemy


class TestFromCsv(DataTestCase):

    def setUp(self):
        self.setup_db()
        self.handler = ImportHandler(self.config)

        self.data_path = self.write_file('data.txt', """\
name,value
foo,bar
foo2,bar2
""")

    def make_importer(self, **kwargs):
        kwargs.setdefault('handler', self.handler)
        return mod.FromCsv(self.config, **kwargs)

    def test_get_input_file_name(self):
        model = self.app.model
        imp = self.make_importer(model_class=model.Setting)

        # name can be guessed
        self.assertEqual(imp.get_input_file_name(), 'Setting.csv')

        # name can be explicitly set
        imp.input_file_name = 'data.txt'
        self.assertEqual(imp.get_input_file_name(), 'data.txt')

    def test_open_input_file(self):
        model = self.app.model
        imp = self.make_importer(model_class=model.Setting)

        # normal operation, input file includes all fields
        imp = self.make_importer(model_class=model.Setting, input_file_path=self.data_path)
        self.assertEqual(imp.fields, ['name', 'value'])
        imp.open_input_file()
        self.assertEqual(imp.input_file.name, self.data_path)
        self.assertIsInstance(imp.input_reader, csv.DictReader)
        self.assertEqual(imp.fields, ['name', 'value'])
        imp.input_file.close()

        # this file is missing a field, plus we'll pretend more are
        # supported - but should wind up with just the one field
        missing = self.write_file('missing.txt', 'name')
        imp = self.make_importer(model_class=model.Setting, input_file_path=missing)
        imp.fields.extend(['lots', 'more'])
        self.assertEqual(imp.fields, ['name', 'value', 'lots', 'more'])
        imp.open_input_file()
        self.assertEqual(imp.fields, ['name'])
        imp.input_file.close()

        # and what happens when no known fields are found
        bogus = self.write_file('bogus.txt', 'blarg')
        imp = self.make_importer(model_class=model.Setting, input_file_path=bogus)
        self.assertEqual(imp.fields, ['name', 'value'])
        self.assertRaises(ValueError, imp.open_input_file)

    def test_close_input_file(self):
        model = self.app.model
        imp = self.make_importer(model_class=model.Setting)

        imp.input_file_path = self.data_path
        imp.open_input_file()
        imp.close_input_file()
        self.assertFalse(hasattr(imp, 'input_reader'))
        self.assertFalse(hasattr(imp, 'input_file'))

    def test_get_source_objects(self):
        model = self.app.model
        imp = self.make_importer(model_class=model.Setting)

        imp.input_file_path = self.data_path
        imp.open_input_file()
        objects = imp.get_source_objects()
        imp.close_input_file()
        self.assertEqual(len(objects), 2)
        self.assertEqual(objects[0], {'name': 'foo', 'value': 'bar'})
        self.assertEqual(objects[1], {'name': 'foo2', 'value': 'bar2'})


class MockMixinImporter(mod.FromCsvToSqlalchemyMixin, mod.FromCsv, ToSqlalchemy):
    pass


class TestFromCsvToSqlalchemyMixin(DataTestCase):

    def setUp(self):
        self.setup_db()
        self.handler = ImportHandler(self.config)

    def make_importer(self, **kwargs):
        kwargs.setdefault('handler', self.handler)
        return MockMixinImporter(self.config, **kwargs)

    def test_constructor(self):
        model = self.app.model

        # no uuid keys
        imp = self.make_importer(model_class=model.Setting)
        self.assertEqual(imp.uuid_keys, [])

        # typical
        # nb. as of now Upgrade is the only table using proper UUID
        imp = self.make_importer(model_class=model.Upgrade)
        self.assertEqual(imp.uuid_keys, ['uuid'])

    def test_normalize_source_object(self):
        model = self.app.model

        # no uuid keys
        imp = self.make_importer(model_class=model.Setting)
        result = imp.normalize_source_object({'name': 'foo', 'value': 'bar'})
        self.assertEqual(result, {'name': 'foo', 'value': 'bar'})

        # source has proper UUID
        # nb. as of now Upgrade is the only table using proper UUID
        imp = self.make_importer(model_class=model.Upgrade, fields=['uuid', 'description'])
        result = imp.normalize_source_object({'uuid': _uuid.UUID('06753693-d892-77f0-8000-ce71bf7ebbba'),
                                              'description': 'testing'})
        self.assertEqual(result, {'uuid': _uuid.UUID('06753693-d892-77f0-8000-ce71bf7ebbba'),
                                  'description': 'testing'})

        # source has string uuid
        # nb. as of now Upgrade is the only table using proper UUID
        imp = self.make_importer(model_class=model.Upgrade, fields=['uuid', 'description'])
        result = imp.normalize_source_object({'uuid': '06753693d89277f08000ce71bf7ebbba',
                                              'description': 'testing'})
        self.assertEqual(result, {'uuid': _uuid.UUID('06753693-d892-77f0-8000-ce71bf7ebbba'),
                                  'description': 'testing'})


class MockMixinHandler(mod.FromCsvToSqlalchemyHandlerMixin, ToSqlalchemyHandler):
    ToImporterBase = ToSqlalchemy


class TestFromCsvToSqlalchemyHandlerMixin(DataTestCase):

    def make_handler(self, **kwargs):
        return MockMixinHandler(self.config, **kwargs)

    def test_get_target_model(self):
        with patch.object(mod.FromCsvToSqlalchemyHandlerMixin, 'define_importers', return_value={}):
            handler = self.make_handler()
            self.assertRaises(NotImplementedError, handler.get_target_model)

    def test_define_importers(self):
        model = self.app.model
        with patch.object(mod.FromCsvToSqlalchemyHandlerMixin, 'get_target_model', return_value=model):
            handler = self.make_handler()
            importers = handler.define_importers()
            self.assertIn('Setting', importers)
            self.assertTrue(issubclass(importers['Setting'], mod.FromCsv))
            self.assertTrue(issubclass(importers['Setting'], ToSqlalchemy))
            self.assertIn('User', importers)
            self.assertIn('Person', importers)
            self.assertIn('Role', importers)

    def test_make_importer_factory(self):
        model = self.app.model
        with patch.object(mod.FromCsvToSqlalchemyHandlerMixin, 'define_importers', return_value={}):
            handler = self.make_handler()
            factory = handler.make_importer_factory(model.Setting, 'Setting')
            self.assertTrue(issubclass(factory, mod.FromCsv))
            self.assertTrue(issubclass(factory, ToSqlalchemy))


class TestFromCsvToWutta(DataTestCase):

    def make_handler(self, **kwargs):
        return mod.FromCsvToWutta(self.config, **kwargs)

    def test_get_target_model(self):
        handler = self.make_handler()
        self.assertIs(handler.get_target_model(), self.app.model)
