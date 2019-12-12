import unittest

from app.lib.io.io_dir import dir_create, dir_delete, is_dir_exist, dir_change_name
from app.lib.io.io_file import file_save, File, file_exist

test_path = '/tmp/ease/'
path_not_exist = '/not/existing/path'


class TestIoDir(unittest.TestCase):

    def test_should_create_dir_with_success(self):
        result = dir_create(test_path)

        self.assertTrue(result)

    def test_should_not_create_dir_because_path_is_not_valid(self):
        result = dir_create(path_not_exist)

        self.assertFalse(result)

    def test_should_change_directory_name_with_success(self):
        dir_create(test_path)
        dir_change_name(test_path, 'easeCI')

        self.assertTrue(is_dir_exist('/tmp/easeCI/'))

    def test_should_not_change_directory_name_if_dir_not_exist(self):
        dir_change_name(path_not_exist, 'new_name')

        self.assertFalse(is_dir_exist(path_not_exist))

    def test_should_delete_directory_with_success(self):
        dir_create(test_path)
        dir_delete(test_path, force=False)

        self.assertFalse(False, is_dir_exist(test_path))

    def test_should_delete_directory_with_success_with_content(self):
        dir_create(test_path)
        file_path = test_path + '/test_file.txt'
        file_save(File(file_path, 'Test content'), append=False)
        dir_delete(test_path, force=True)

        self.assertFalse(is_dir_exist(file_path))
        self.assertFalse(file_exist(file_path))

    def test_should_not_delete_directory_because_directory_exist_but_has_content(self):
        dir_create(test_path)
        file_path = test_path + '/test_file.txt'
        file_save(File(file_path, 'Test content'), append=False)
        dir_delete(test_path, force=False)

        self.assertTrue(is_dir_exist(test_path))
        self.assertTrue(file_exist(file_path))

    def test_should_not_delete_directory_that_not_exist(self):
        result = dir_delete(path_not_exist, force=False)

        self.assertFalse(result)

    def tearDown(self):
        dir_delete(test_path, force=True)
