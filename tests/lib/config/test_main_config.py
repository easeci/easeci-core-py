import unittest

from lib.config.main_config import MainConfigContext
from lib.io.io_file import file_save, file_delete
from tests.lib.config.utils import generate_fake_config


class TestMainConfig(unittest.TestCase):
    _config_path = '/tmp/general.yml'
    _dir = '/tmp'

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

    def tearDown(self):
        file_delete(self._config_path)
