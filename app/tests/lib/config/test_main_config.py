import unittest

from app.lib.config.main_config import MainConfigContext
from app.lib.io.io_file import file_save, file_delete
from app.tests.lib.config.utils import generate_fake_config


class TestMainConfig(unittest.TestCase):
    _config_path = '/tmp/ease/general.yml'
    _dir = '/tmp/ease'

    def setUp(self):
        file = generate_fake_config()
        file_save(file)

    def test_should_lazy_instantiate_singleton_class_with_success(self):
        config = MainConfigContext.get_instance()

        self.assertIsNotNone(config)

    def test_should_raise_when_try_to_instantiate_by_constructor(self):
        with self.assertRaises(RuntimeError):
            MainConfigContext()

    def test_all_path_should_return_paths_to_search_in_correct_order(self):
        paths = MainConfigContext.get_instance().all_paths()

        self.assertEqual(3, len(paths))

    def test_config_context_should_initialize_with_path_provided_as_argument(self):
        config = MainConfigContext.get_instance(self._dir)
        result = config.scan_paths()
        prop = config.get_property('main.paths.temp')

        self.assertIsNotNone(config)
        self.assertIsNotNone(prop)
        self.assertTrue(result)
        self.assertEqual('/tmp/ease', prop)

    def test_should_get_default_config_file_from_this_project_if_path_is_not_specified(self):
        config = MainConfigContext.get_instance()
        result = config.scan_paths()

        self.assertTrue(result)

    def test_should_get_property_returns_value_with_success_when_initialize_MainConfigContext_with_specified_path(self):
        config = MainConfigContext.get_instance(self._dir)
        config.scan_paths()
        result = config.get_property('main.paths.temp')

        self.assertIsNotNone(result)
        self.assertEqual(result, '/tmp/ease')

    def test_should_get_property_returns_value_with_success_when_initialize_MainConfigContext_with_no_specified_path(self):
        config = MainConfigContext.get_instance()
        config.scan_paths()
        result = config.get_property('main.paths.temp')

        self.assertIsNotNone(result)
        self.assertEqual(result, '/tmp/ease')

    def test_should_info_returns_string_value_of_context_state(self):
        config = MainConfigContext.get_instance()
        config.scan_paths()
        result = config.info()

        self.assertIsNotNone(result)

    def tearDown(self):
        file_delete(self._config_path)
