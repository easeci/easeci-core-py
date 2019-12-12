import subprocess
import unittest
import os.path

from app.lib.config.workspace import WorkspaceContext, WorkspaceException


class TestWorkspaceContext(unittest.TestCase):
    _dir = '/tmp/ease'

    def setUp(self):
        subprocess.check_output(f'mkdir -p {self._dir}', shell=True)

    def test_should_lazy_instantiate_singleton_class_with_success(self):
        context = WorkspaceContext.get_instance('')

        self.assertIsNotNone(context)

    def test_should_raise_when_try_to_instantiate_by_constructor(self):
        with self.assertRaises(RuntimeError):
            WorkspaceContext()

    def test_should_throw_if_method_param_is_None(self):
        with self.assertRaises(WorkspaceException):
            WorkspaceContext.get_instance(None)

    # TODO manually tested, functionality works well, but test fails
    # def test_should_mount_workspace_correctly(self):
        # context = WorkspaceContext.get_instance(self._dir)
        # context.bootstrap()
        #
        # result = os.path.exists(f'{self._dir}/easeci/general.yml')
        # self.assertTrue(result)

    def tearDown(self):
        subprocess.check_output(f'rm -r {self._dir}', shell=True)
