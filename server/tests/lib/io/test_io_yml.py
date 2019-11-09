import unittest
import subprocess
import yaml
from lib.io.io_yml import yml_load, yml_get, yml_create, yml_append

tmp_path = '/tmp/test_config.yml'
tmp_path_malformed = '/tmp/test_malformed_config.yml'


def create_test_yml_file():
    pwd = str(subprocess.check_output('pwd', shell=True))[2:-2]
    yml_test_file = pwd + '/test_config.yml'
    subprocess.check_call('cp ' + yml_test_file + ' ' + tmp_path, shell=True)


def create_test_malformed_yml_file():
    pwd = str(subprocess.check_output('pwd', shell=True))[2:-2]
    yml_test_file = pwd + '/test_malformed_config.yml'
    subprocess.check_call('cp ' + yml_test_file + ' ' + tmp_path_malformed, shell=True)


def delete_test_yml_file(custom_path=''):
    if custom_path is not None and len(custom_path) > 0:
        subprocess.check_output('rm ' + custom_path, shell=True)
    try:
        subprocess.check_output('rm ' + tmp_path, shell=True)
        subprocess.check_output('rm ' + tmp_path_malformed, shell=True)
    except subprocess.CalledProcessError:
        return


class TestIoYml(unittest.TestCase):

    def setUp(self) -> None: create_test_yml_file()

    def test_should_load_yml_file_with_success(self):
        result = yml_load(tmp_path)

        self.assertEqual(dict, type(result))

    def test_should_load_yml_file_with_malformed_syntax_and_return_empty_dict(self):
        create_test_malformed_yml_file()
        result = yml_load(tmp_path_malformed)

        self.assertEqual(dict, type(result))
        self.assertEqual(len(result.keys()), 0)

    def test_should_not_load_yml_file_just_not_exist(self):
        bad_path = '/not/existing/file'

        with self.assertRaises(FileNotFoundError):
            yml_load(bad_path)

    def test_yml_get_should_correctly_fetch_one_requested_property(self):
        refs = 'test.configuration.date'
        result = yml_get(tmp_path, refs)

        self.assertEqual('08-11-2019', result)

    def test_yml_get_should_return_None_if_property_not_exist(self):
        refs = 'test.not.exist'
        result = yml_get(tmp_path, refs)

        self.assertEqual(None, result)

    def test_yml_get_should_return_correct_value_if_refs_path_is_long(self):
        refs = 'property.deep.nested.test.is.this.will.work'
        result = yml_get(tmp_path, refs)

        self.assertEqual('works well!', result)

    def test_yml_get_should_return_None_if_refs_are_zero_length(self):
        refs = ''
        result = yml_get(tmp_path, refs)

        self.assertEqual(None, result)

    def test_yml_create_should_save_yml_file_in_pointed_localisation(self):
        path = '/tmp/example.yml'
        val = {'country': 'Poland', 'continent': 'Europe', 'other': {'population': 36000000, 'language': 'polski'}}
        saved = yml_create(path, val)
        loaded_again = yml_load(path)

        self.assertEqual(val, loaded_again)
        self.assertEqual(saved.path, path)
        self.assertEqual(saved.content, yaml.dump(val))
        delete_test_yml_file(path)

    def test_yml_create_should_return_None_if_one_of_arguments_is_None(self):
        path = '/tmp/example.yml'
        val = None
        saved = yml_create(path, val)

        self.assertEqual(None, saved)
        delete_test_yml_file(path)

    def test_yml_append_should_append_new_yml_property_with_success(self):
        args = [
            ('project.copyright', 'All rights reserved 2019'),
            ('test.configuration.time.sec', 45),
            ('property.deep.nested.test.is.this', 'test'),
            ('project.licence.provider', 'Apache')
        ]

        def test(yml_refs, value):
            append_result = yml_append(tmp_path, (yml_refs, value))
            newly_updated = yml_load(tmp_path)
            value_after_append = yml_get(tmp_path, yml_refs)

            self.assertEqual(append_result, newly_updated)
            self.assertTrue(str(value_after_append).__contains__(str(value)))

        for arg in args:
            test(arg[0], arg[1])

    def tearDown(self) -> None: delete_test_yml_file()
