import os
import unittest

from lib.io.io_file import file_load, File, file_exist, file_save, file_delete, file_change

file_path = '/tmp/test_file'

fake_content = 'This is fake file content\n' \
               'created in order to\n' \
               'testing IO operations\n'


def create_tmp_file():
    os.system('touch ' + file_path)
    return file_path


def delete_tmp_file(path):
    os.system('rm ' + path)


class TestIoFacade(unittest.TestCase):

    def test_should_load_file_with_success(self):
        path = '/etc/hosts'
        file = file_load(path)

        self.assertEqual(type(file), File)
        self.assertTrue(len(file.path) > 0)
        self.assertTrue(len(file.content) > 0)

    def test_should_not_load_file_because_of_raise_exception(self):
        path = '/not/existing/file'

        with self.assertRaises(FileNotFoundError):
            file_load(path)

    def test_should_file_save_append_mode_with_success(self):
        to_append = 'New appended line!'
        create_tmp_file()
        # Write some content to test file in write mode
        file_save(File(file_path, fake_content), False)
        # Append one row to test file
        file_save(File(file_path, to_append), True)

        self.assertEqual(file_load(file_path).content, fake_content + to_append)

    def test_should_file_save_append_mode_with_failure__file_should_not_be_same_as_before(self):
        create_tmp_file()
        for x in range(2):
            file_save(File(file_path, fake_content), True)

        self.assertNotEqual(file_load(file_path).content, fake_content)

    def test_should_file_save_override_mode_with_success__file_should_be_always_the_same(self):
        create_tmp_file()
        for x in range(2):
            file_save(File(file_path, fake_content), False)

        self.assertEqual(file_load(file_path).content, fake_content)

    def test_should_file_save_create_new_file_if_not_exist(self):
        path = '/tmp/another_test_file'
        content = 'File created once not exist'
        delete_tmp_file(path)
        file_save(File(path, content))

        self.assertTrue(file_exist(path))
        self.assertEqual(file_load(path).content, content)
        delete_tmp_file(path)

    def test_should_delete_file_if_exist(self):
        path = create_tmp_file()
        file_save(File(path, fake_content), False)
        result = file_delete(path)

        self.assertEqual(0, result)

    def test_should_raise_if_wants_to_delete_not_existing_file(self):
        not_existing_path = '/not/existing/file'
        result = file_delete(not_existing_path)

        self.assertEqual(1, result)

    def test_should_replace_content_with_success_if_content_exist(self):
        path = create_tmp_file()
        file_save(File(path, fake_content), False)
        old = 'This is fake file content'
        new = 'This is a file content'
        result = file_change(file_path, old, new)
        contains = str(file_load(path).content).__contains__(new)

        self.assertEqual(0, result)
        self.assertTrue(contains)

    def test_should_not_replace_when_content_not_occur_in_file(self):
        path = create_tmp_file()
        file_save(File(path, fake_content), False)
        old = 'this phrase not occur'
        new = 'This is a file content'
        result = file_change(file_path, old, new)
        contains = str(file_load(path).content).__contains__(new)

        self.assertEqual(1, result)
        self.assertFalse(contains)

    def test_should_not_replace_when_file_not_exist(self):
        old = 'this phrase not occur'
        new = 'This is a file content'
        result = file_change(file_path, old, new)

        self.assertEqual(1, result)

    def test_should_return_True_if_file_exist(self):
        path = create_tmp_file()
        result = file_exist(path)

        self.assertTrue(result)

    def test_should_return_False_if_file_not_exist(self):
        result = file_exist(file_path)

        self.assertFalse(result)

    def tearDown(self):
        delete_tmp_file(file_path)
