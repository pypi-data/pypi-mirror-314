#-*- coding: utf-8; -*-

from unittest.mock import patch

from wuttjamaican.testing import DataTestCase

from wuttasync.importing import base as mod, ImportHandler, Orientation


class TestImporter(DataTestCase):

    def setUp(self):
        self.setup_db()
        self.handler = ImportHandler(self.config)

    def make_importer(self, **kwargs):
        kwargs.setdefault('handler', self.handler)
        return mod.Importer(self.config, **kwargs)

    def test_constructor(self):
        model = self.app.model

        # basic importer
        imp = self.make_importer(model_class=model.Setting)

        # fields
        self.assertEqual(imp.supported_fields, ['name', 'value'])
        self.assertEqual(imp.simple_fields, ['name', 'value'])
        self.assertEqual(imp.fields, ['name', 'value'])

        # orientation etc.
        self.assertEqual(imp.orientation, Orientation.IMPORT)
        self.assertEqual(imp.actioning, 'importing')
        self.assertTrue(imp.create)
        self.assertTrue(imp.update)
        self.assertTrue(imp.delete)
        self.assertFalse(imp.dry_run)

    def test_constructor_fields(self):
        model = self.app.model

        # basic importer
        imp = self.make_importer(model_class=model.Setting, fields='name')
        self.assertEqual(imp.fields, ['name'])

    def test_constructor_excluded_fields(self):
        model = self.app.model

        # basic importer
        imp = self.make_importer(model_class=model.Setting, excluded_fields='value')
        self.assertEqual(imp.fields, ['name'])

    def test_get_model_title(self):
        model = self.app.model
        imp = self.make_importer(model_class=model.Setting)
        self.assertEqual(imp.get_model_title(), 'Setting')
        imp.model_title = "SeTtInG"
        self.assertEqual(imp.get_model_title(), 'SeTtInG')

    def test_get_simple_fields(self):
        model = self.app.model
        imp = self.make_importer(model_class=model.Setting)
        self.assertEqual(imp.get_simple_fields(), ['name', 'value'])
        imp.simple_fields = ['name']
        self.assertEqual(imp.get_simple_fields(), ['name'])

    def test_get_supported_fields(self):
        model = self.app.model
        imp = self.make_importer(model_class=model.Setting)
        self.assertEqual(imp.get_supported_fields(), ['name', 'value'])
        imp.supported_fields = ['name']
        self.assertEqual(imp.get_supported_fields(), ['name'])

    def test_get_fields(self):
        model = self.app.model
        imp = self.make_importer(model_class=model.Setting)
        self.assertEqual(imp.get_fields(), ['name', 'value'])
        imp.fields = ['name']
        self.assertEqual(imp.get_fields(), ['name'])

    def test_get_keys(self):
        model = self.app.model
        imp = self.make_importer(model_class=model.Setting)
        self.assertEqual(imp.get_keys(), ['name'])
        with patch.multiple(imp, create=True, key='value'):
            self.assertEqual(imp.get_keys(), ['value'])
        with patch.multiple(imp, create=True, keys=['foo', 'bar']):
            self.assertEqual(imp.get_keys(), ['foo', 'bar'])

    def test_process_data(self):
        model = self.app.model
        imp = self.make_importer(model_class=model.Setting, caches_target=True,
                                 delete=True)

        def make_cache():
            setting1 = model.Setting(name='foo1', value='bar1')
            setting2 = model.Setting(name='foo2', value='bar2')
            setting3 = model.Setting(name='foo3', value='bar3')
            cache = {
                ('foo1',): {
                    'object': setting1,
                    'data': {'name': 'foo1', 'value': 'bar1'},
                },
                ('foo2',): {
                    'object': setting2,
                    'data': {'name': 'foo2', 'value': 'bar2'},
                },
                ('foo3',): {
                    'object': setting3,
                    'data': {'name': 'foo3', 'value': 'bar3'},
                },
            }
            return cache

        # nb. delete always succeeds
        with patch.object(imp, 'delete_target_object', return_value=True):

            # create + update + delete all as needed
            with patch.object(imp, 'get_target_cache', return_value=make_cache()):
                created, updated, deleted = imp.process_data([
                    {'name': 'foo3', 'value': 'BAR3'},
                    {'name': 'foo4', 'value': 'BAR4'},
                    {'name': 'foo5', 'value': 'BAR5'},
                ])
                self.assertEqual(len(created), 2)
                self.assertEqual(len(updated), 1)
                self.assertEqual(len(deleted), 2)

            # same but with --max-total so delete gets skipped
            with patch.object(imp, 'get_target_cache', return_value=make_cache()):
                with patch.object(imp, 'max_total', new=3):
                    created, updated, deleted = imp.process_data([
                        {'name': 'foo3', 'value': 'BAR3'},
                        {'name': 'foo4', 'value': 'BAR4'},
                        {'name': 'foo5', 'value': 'BAR5'},
                    ])
                    self.assertEqual(len(created), 2)
                    self.assertEqual(len(updated), 1)
                    self.assertEqual(len(deleted), 0)

            # delete all if source data empty
            with patch.object(imp, 'get_target_cache', return_value=make_cache()):
                created, updated, deleted = imp.process_data()
                self.assertEqual(len(created), 0)
                self.assertEqual(len(updated), 0)
                self.assertEqual(len(deleted), 3)

    def test_do_create_update(self):
        model = self.app.model
        imp = self.make_importer(model_class=model.Setting, caches_target=True)

        def make_cache():
            setting1 = model.Setting(name='foo1', value='bar1')
            setting2 = model.Setting(name='foo2', value='bar2')
            cache = {
                ('foo1',): {
                    'object': setting1,
                    'data': {'name': 'foo1', 'value': 'bar1'},
                },
                ('foo2',): {
                    'object': setting2,
                    'data': {'name': 'foo2', 'value': 'bar2'},
                },
            }
            return cache

        # change nothing if data matches
        with patch.multiple(imp, create=True, cached_target=make_cache()):
            created, updated = imp.do_create_update([
                {'name': 'foo1', 'value': 'bar1'},
                {'name': 'foo2', 'value': 'bar2'},
            ])
            self.assertEqual(len(created), 0)
            self.assertEqual(len(updated), 0)

        # update all as needed
        with patch.multiple(imp, create=True, cached_target=make_cache()):
            created, updated = imp.do_create_update([
                {'name': 'foo1', 'value': 'BAR1'},
                {'name': 'foo2', 'value': 'BAR2'},
            ])
            self.assertEqual(len(created), 0)
            self.assertEqual(len(updated), 2)

        # update all, with --max-update
        with patch.multiple(imp, create=True, cached_target=make_cache(), max_update=1):
            created, updated = imp.do_create_update([
                {'name': 'foo1', 'value': 'BAR1'},
                {'name': 'foo2', 'value': 'BAR2'},
            ])
            self.assertEqual(len(created), 0)
            self.assertEqual(len(updated), 1)

        # update all, with --max-total
        with patch.multiple(imp, create=True, cached_target=make_cache(), max_total=1):
            created, updated = imp.do_create_update([
                {'name': 'foo1', 'value': 'BAR1'},
                {'name': 'foo2', 'value': 'BAR2'},
            ])
            self.assertEqual(len(created), 0)
            self.assertEqual(len(updated), 1)

        # create all as needed
        with patch.multiple(imp, create=True, cached_target=make_cache()):
            created, updated = imp.do_create_update([
                {'name': 'foo1', 'value': 'bar1'},
                {'name': 'foo2', 'value': 'bar2'},
                {'name': 'foo3', 'value': 'BAR3'},
                {'name': 'foo4', 'value': 'BAR4'},
            ])
            self.assertEqual(len(created), 2)
            self.assertEqual(len(updated), 0)

        # what happens when create gets skipped
        with patch.multiple(imp, create=True, cached_target=make_cache()):
            with patch.object(imp, 'create_target_object', return_value=None):
                created, updated = imp.do_create_update([
                    {'name': 'foo1', 'value': 'bar1'},
                    {'name': 'foo2', 'value': 'bar2'},
                    {'name': 'foo3', 'value': 'BAR3'},
                    {'name': 'foo4', 'value': 'BAR4'},
                ])
                self.assertEqual(len(created), 0)
                self.assertEqual(len(updated), 0)

        # create all, with --max-create
        with patch.multiple(imp, create=True, cached_target=make_cache(), max_create=1):
            created, updated = imp.do_create_update([
                {'name': 'foo1', 'value': 'bar1'},
                {'name': 'foo2', 'value': 'bar2'},
                {'name': 'foo3', 'value': 'BAR3'},
                {'name': 'foo4', 'value': 'BAR4'},
            ])
            self.assertEqual(len(created), 1)
            self.assertEqual(len(updated), 0)

        # create all, with --max-total
        with patch.multiple(imp, create=True, cached_target=make_cache(), max_total=1):
            created, updated = imp.do_create_update([
                {'name': 'foo1', 'value': 'bar1'},
                {'name': 'foo2', 'value': 'bar2'},
                {'name': 'foo3', 'value': 'BAR3'},
                {'name': 'foo4', 'value': 'BAR4'},
            ])
            self.assertEqual(len(created), 1)
            self.assertEqual(len(updated), 0)

        # create + update all as needed
        with patch.multiple(imp, create=True, cached_target=make_cache()):
            created, updated = imp.do_create_update([
                {'name': 'foo1', 'value': 'BAR1'},
                {'name': 'foo2', 'value': 'BAR2'},
                {'name': 'foo3', 'value': 'BAR3'},
                {'name': 'foo4', 'value': 'BAR4'},
            ])
            self.assertEqual(len(created), 2)
            self.assertEqual(len(updated), 2)

        # create + update all, with --max-total
        with patch.multiple(imp, create=True, cached_target=make_cache(), max_total=1):
            created, updated = imp.do_create_update([
                {'name': 'foo1', 'value': 'BAR1'},
                {'name': 'foo2', 'value': 'BAR2'},
                {'name': 'foo3', 'value': 'BAR3'},
                {'name': 'foo4', 'value': 'BAR4'},
            ])
            # nb. foo1 is updated first
            self.assertEqual(len(created), 0)
            self.assertEqual(len(updated), 1)

    def test_do_delete(self):
        model = self.app.model

        # this requires a mock target cache
        setting1 = model.Setting(name='foo1', value='bar1')
        setting2 = model.Setting(name='foo2', value='bar2')
        imp = self.make_importer(model_class=model.Setting, caches_target=True)
        cache = {
            ('foo1',): {
                'object': setting1,
                'data': {'name': 'foo1', 'value': 'bar1'},
            },
            ('foo2',): {
                'object': setting2,
                'data': {'name': 'foo2', 'value': 'bar2'},
            },
        }

        with patch.object(imp, 'delete_target_object') as delete_target_object:

            # delete nothing if source has same keys
            with patch.multiple(imp, create=True, cached_target=dict(cache)):
                source_keys = set(imp.cached_target)
                result = imp.do_delete(source_keys)
                self.assertFalse(delete_target_object.called)
                self.assertEqual(result, [])

            # delete both if source has no keys
            delete_target_object.reset_mock()
            with patch.multiple(imp, create=True, cached_target=dict(cache)):
                source_keys = set()
                result = imp.do_delete(source_keys)
                self.assertEqual(delete_target_object.call_count, 2)
                self.assertEqual(len(result), 2)

            # delete just one if --max-delete was set
            delete_target_object.reset_mock()
            with patch.multiple(imp, create=True, cached_target=dict(cache)):
                source_keys = set()
                with patch.object(imp, 'max_delete', new=1):
                    result = imp.do_delete(source_keys)
                    self.assertEqual(delete_target_object.call_count, 1)
                    self.assertEqual(len(result), 1)

            # delete just one if --max-total was set
            delete_target_object.reset_mock()
            with patch.multiple(imp, create=True, cached_target=dict(cache)):
                source_keys = set()
                with patch.object(imp, 'max_total', new=1):
                    result = imp.do_delete(source_keys)
                    self.assertEqual(delete_target_object.call_count, 1)
                    self.assertEqual(len(result), 1)

    def test_get_record_key(self):
        model = self.app.model
        imp = self.make_importer(model_class=model.Setting)
        record = {'name': 'foo', 'value': 'bar'}
        self.assertEqual(imp.get_record_key(record), ('foo',))
        imp.key = ('name', 'value')
        self.assertEqual(imp.get_record_key(record), ('foo', 'bar'))

    def test_data_diffs(self):
        model = self.app.model
        imp = self.make_importer(model_class=model.Setting)

        # 2 identical records
        rec1 = {'name': 'foo', 'value': 'bar'}
        rec2 = {'name': 'foo', 'value': 'bar'}
        result = imp.data_diffs(rec1, rec2)
        self.assertEqual(result, [])

        # now they're different
        rec2['value'] = 'baz'
        result = imp.data_diffs(rec1, rec2)
        self.assertEqual(result, ['value'])

    def test_normalize_source_data(self):
        model = self.app.model
        imp = self.make_importer(model_class=model.Setting)

        # empty source data
        data = imp.normalize_source_data()
        self.assertEqual(data, [])

        # now with 1 record
        setting = model.Setting(name='foo', value='bar')
        data = imp.normalize_source_data(source_objects=[setting])
        self.assertEqual(len(data), 1)
        # nb. default normalizer returns object as-is
        self.assertIs(data[0], setting)

    def test_get_unique_data(self):
        model = self.app.model
        imp = self.make_importer(model_class=model.Setting)

        setting1 = model.Setting(name='foo', value='bar1')
        setting2 = model.Setting(name='foo', value='bar2')

        result = imp.get_unique_data([setting2, setting1])
        self.assertIsInstance(result, tuple)
        self.assertEqual(len(result), 2)
        self.assertIsInstance(result[0], list)
        self.assertEqual(len(result[0]), 1)
        self.assertIs(result[0][0], setting2) # nb. not setting1
        self.assertIsInstance(result[1], set)
        self.assertEqual(result[1], {('foo',)})

    def test_get_source_objects(self):
        model = self.app.model
        imp = self.make_importer(model_class=model.Setting)
        self.assertEqual(imp.get_source_objects(), [])

    def test_normalize_source_object_all(self):
        model = self.app.model
        imp = self.make_importer(model_class=model.Setting)
        setting = model.Setting()
        result = imp.normalize_source_object_all(setting)
        self.assertEqual(len(result), 1)
        self.assertIs(result[0], setting)

    def test_normalize_source_object(self):
        model = self.app.model
        imp = self.make_importer(model_class=model.Setting)
        setting = model.Setting()
        result = imp.normalize_source_object(setting)
        self.assertIs(result, setting)

    def test_get_target_cache(self):
        model = self.app.model
        imp = self.make_importer(model_class=model.Setting)

        with patch.object(imp, 'get_target_objects') as get_target_objects:
            get_target_objects.return_value = []

            # empty cache
            cache = imp.get_target_cache()
            self.assertEqual(cache, {})

            # cache w/ one record
            setting = model.Setting(name='foo', value='bar')
            get_target_objects.return_value = [setting]
            cache = imp.get_target_cache()
            self.assertEqual(len(cache), 1)
            self.assertIn(('foo',), cache)
            foo = cache[('foo',)]
            self.assertEqual(len(foo), 2)
            self.assertEqual(set(foo), {'object', 'data'})
            self.assertIs(foo['object'], setting)
            self.assertEqual(foo['data'], {'name': 'foo', 'value': 'bar'})

    def test_get_target_objects(self):
        model = self.app.model
        imp = self.make_importer(model_class=model.Setting)
        self.assertRaises(NotImplementedError, imp.get_target_objects)

    def test_get_target_object(self):
        model = self.app.model
        setting = model.Setting(name='foo', value='bar')

        # nb. must mock up a target cache for this one
        imp = self.make_importer(model_class=model.Setting, caches_target=True)
        imp.cached_target = {
            ('foo',): {
                'object': setting,
                'data': {'name': 'foo', 'value': 'bar'},
            },
        }

        # returns same object
        result = imp.get_target_object(('foo',))
        self.assertIs(result, setting)

        # and one more time just for kicks
        result = imp.get_target_object(('foo',))
        self.assertIs(result, setting)

        # but then not if cache flag is off
        imp.caches_target = False
        result = imp.get_target_object(('foo',))
        self.assertIsNone(result)

    def test_normalize_target_object(self):
        model = self.app.model
        imp = self.make_importer(model_class=model.Setting)
        setting = model.Setting(name='foo', value='bar')
        data = imp.normalize_target_object(setting)
        self.assertEqual(data, {'name': 'foo', 'value': 'bar'})

    def test_get_deletable_keys(self):
        model = self.app.model
        imp = self.make_importer(model_class=model.Setting)

        # empty set by default (nb. no target cache)
        result = imp.get_deletable_keys()
        self.assertIsInstance(result, set)
        self.assertEqual(result, set())

        setting = model.Setting(name='foo', value='bar')
        cache = {
            ('foo',): {
                'object': setting,
                'data': {'name': 'foo', 'value': 'bar'},
            },
        }

        with patch.multiple(imp, create=True, caches_target=True, cached_target=cache):

            # all are deletable by default
            result = imp.get_deletable_keys()
            self.assertEqual(result, {('foo',)})

            # but some maybe can't be deleted
            with patch.object(imp, 'can_delete_object', return_value=False):
                result = imp.get_deletable_keys()
                self.assertEqual(result, set())

    def test_create_target_object(self):
        model = self.app.model
        imp = self.make_importer(model_class=model.Setting)

        # basic
        setting = imp.create_target_object(('foo',), {'name': 'foo', 'value': 'bar'})
        self.assertIsInstance(setting, model.Setting)
        self.assertEqual(setting.name, 'foo')
        self.assertEqual(setting.value, 'bar')

        # will skip if magic delete flag is set
        setting = imp.create_target_object(('foo',), {'name': 'foo', 'value': 'bar',
                                                      '__ignoreme__': True})
        self.assertIsNone(setting)

    def test_make_empty_object(self):
        model = self.app.model
        imp = self.make_importer(model_class=model.Setting)
        obj = imp.make_empty_object(('foo',))
        self.assertIsInstance(obj, model.Setting)
        self.assertEqual(obj.name, 'foo')

    def test_make_object(self):
        model = self.app.model
        imp = self.make_importer(model_class=model.Setting)
        obj = imp.make_object()
        self.assertIsInstance(obj, model.Setting)

    def test_update_target_object(self):
        model = self.app.model
        imp = self.make_importer(model_class=model.Setting)
        setting = model.Setting(name='foo')

        # basic logic for updating *new* object
        obj = imp.update_target_object(setting, {'name': 'foo', 'value': 'bar'})
        self.assertIs(obj, setting)
        self.assertEqual(setting.value, 'bar')

    def test_can_delete_object(self):
        model = self.app.model
        imp = self.make_importer(model_class=model.Setting)
        setting = model.Setting(name='foo')
        self.assertTrue(imp.can_delete_object(setting))

    def test_delete_target_object(self):
        model = self.app.model
        imp = self.make_importer(model_class=model.Setting)
        setting = model.Setting(name='foo')
        # nb. default implementation always returns false
        self.assertFalse(imp.delete_target_object(setting))


class TestFromFile(DataTestCase):

    def setUp(self):
        self.setup_db()
        self.handler = ImportHandler(self.config)

    def make_importer(self, **kwargs):
        kwargs.setdefault('handler', self.handler)
        return mod.FromFile(self.config, **kwargs)

    def test_setup(self):
        model = self.app.model
        imp = self.make_importer(model_class=model.Setting)
        with patch.object(imp, 'open_input_file') as open_input_file:
            imp.setup()
            open_input_file.assert_called_once_with()

    def test_teardown(self):
        model = self.app.model
        imp = self.make_importer(model_class=model.Setting)
        with patch.object(imp, 'close_input_file') as close_input_file:
            imp.teardown()
            close_input_file.assert_called_once_with()

    def test_get_input_file_path(self):
        model = self.app.model
        imp = self.make_importer(model_class=model.Setting)

        # path is guessed from dir+filename
        path = self.write_file('data.txt', '')
        imp.input_file_dir = self.tempdir
        imp.input_file_name = 'data.txt'
        self.assertEqual(imp.get_input_file_path(), path)

        # path can be explicitly set
        path2 = self.write_file('data2.txt', '')
        imp.input_file_path = path2
        self.assertEqual(imp.get_input_file_path(), path2)

    def test_get_input_file_dir(self):
        model = self.app.model
        imp = self.make_importer(model_class=model.Setting)

        # path cannot be guessed
        self.assertRaises(NotImplementedError, imp.get_input_file_dir)

        # path can be explicitly set
        imp.input_file_dir = self.tempdir
        self.assertEqual(imp.get_input_file_dir(), self.tempdir)

    def test_get_input_file_name(self):
        model = self.app.model
        imp = self.make_importer(model_class=model.Setting)

        # name cannot be guessed
        self.assertRaises(NotImplementedError, imp.get_input_file_name)

        # name can be explicitly set
        imp.input_file_name = 'data.txt'
        self.assertEqual(imp.get_input_file_name(), 'data.txt')

    def test_open_input_file(self):
        model = self.app.model
        imp = self.make_importer(model_class=model.Setting)
        self.assertRaises(NotImplementedError, imp.open_input_file)

    def test_close_input_file(self):
        model = self.app.model
        imp = self.make_importer(model_class=model.Setting)

        path = self.write_file('data.txt', '')
        with open(path, 'rt') as f:
            imp.input_file = f
            with patch.object(f, 'close') as close:
                imp.close_input_file()
                close.assert_called_once_with()


class TestToSqlalchemy(DataTestCase):

    def setUp(self):
        self.setup_db()
        self.handler = ImportHandler(self.config)

    def make_importer(self, **kwargs):
        kwargs.setdefault('handler', self.handler)
        return mod.ToSqlalchemy(self.config, **kwargs)

    def test_get_target_objects(self):
        model = self.app.model
        imp = self.make_importer(model_class=model.Setting, target_session=self.session)

        setting1 = model.Setting(name='foo', value='bar')
        self.session.add(setting1)
        setting2 = model.Setting(name='foo2', value='bar2')
        self.session.add(setting2)
        self.session.commit()

        result = imp.get_target_objects()
        self.assertEqual(len(result), 2)
        self.assertEqual(set(result), {setting1, setting2})

    def test_get_target_object(self):
        model = self.app.model
        setting = model.Setting(name='foo', value='bar')

        # nb. must mock up a target cache for this one
        imp = self.make_importer(model_class=model.Setting, caches_target=True)
        imp.cached_target = {
            ('foo',): {
                'object': setting,
                'data': {'name': 'foo', 'value': 'bar'},
            },
        }

        # returns same object
        result = imp.get_target_object(('foo',))
        self.assertIs(result, setting)

        # and one more time just for kicks
        result = imp.get_target_object(('foo',))
        self.assertIs(result, setting)

        # now let's put a 2nd setting in the db
        setting2 = model.Setting(name='foo2', value='bar2')
        self.session.add(setting2)
        self.session.commit()

        # nb. disable target cache
        with patch.multiple(imp, create=True,
                            target_session=self.session,
                            caches_target=False):

            # now we should be able to fetch that via query
            result = imp.get_target_object(('foo2',))
            self.assertIsInstance(result, model.Setting)
            self.assertIs(result, setting2)

            # but sometimes it will not be found
            result = imp.get_target_object(('foo3',))
            self.assertIsNone(result)

    def test_create_target_object(self):
        model = self.app.model
        imp = self.make_importer(model_class=model.Setting, target_session=self.session)
        setting = model.Setting(name='foo', value='bar')

        # new object is added to session
        setting = imp.create_target_object(('foo',), {'name': 'foo', 'value': 'bar'})
        self.assertIsInstance(setting, model.Setting)
        self.assertEqual(setting.name, 'foo')
        self.assertEqual(setting.value, 'bar')
        self.assertIn(setting, self.session)

    def test_delete_target_object(self):
        model = self.app.model

        setting = model.Setting(name='foo', value='bar')
        self.session.add(setting)

        self.assertEqual(self.session.query(model.Setting).count(), 1)
        imp = self.make_importer(model_class=model.Setting, target_session=self.session)
        imp.delete_target_object(setting)
        self.assertEqual(self.session.query(model.Setting).count(), 0)
