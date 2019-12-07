import subprocess

from lib.config.main_config import MainConfigContext
from lib.config.utils import pwd
from lib.io.io_yml import yml_change
from lib.log.logger import log
import os.path
import shutil

"""
WorkspaceContext is a class that holds context and information about EaseCI's filesystem.
The singleton object of this class knows everything about resources used for running
EaseCI instance. Here you can refers to pipelines, users, configurations, and other files.
"""


class WorkspaceContext:
    __instance = None
    _workspace = None

    def __init__(self):
        raise RuntimeError('Cannot instantiate singleton by constructor!')

    @classmethod
    def get_instance(cls, workspace):
        if workspace is None:
            raise WorkspaceException('Workspace must be initialized value with correct path!')
        log(f"workspace initialize in: {workspace}")
        cls._workspace = workspace
        if cls.__instance is None:
            cls.__instance = cls.__new__(cls)
        return cls.__instance

    """
    Starts chain of initialization process of EaseCI
    """
    def bootstrap(self):
        if self.is_new():
            self.mount()
            return
        res = self.check()
        if res:
            log("integrity of workspace is correct")
        else:
            WorkspaceException("Integrity of workspace is incorrect so EaseCI cannot run!")

    """
    Checks if directory indicated to mounting is new (empty) or not
     - returns 'True' if indicated directory is new (empty)
     - return 'False' if indicated directory is used before
    """
    def is_new(self):
        def is_exists(path):
            return os.path.exists(path)
        first = self._workspace + '/general.yml'
        second = self._workspace + '/easeci/general.yml'
        if os.path.isdir(self._workspace) and (is_exists(first) or is_exists(second)):
            log("workspace is detected. Preparation of workspace ... wait for a while")
            return False
        return True

    """
    Checks data integrity before EaseCI startup
    - returns 'True' if data integrity is correct
    - returns 'False' if data integrity is incorrect
    """
    def check(self):
        # TODO
        return True

    """
    Mounts required directories in workspace.
    Simply moves required resources to indicated directory designated for workspace being
    * Be advised that this method uses recursion - if indicated directory exists,
      we must create one next, nested directory, because shutil.copytree() throws FileExistsError
    """
    def mount(self):
        def deploy():
            src = pwd().strip() + '/config'
            shutil.copytree(src, self._workspace)
            yml_change(src + '/general.yml', ('main.paths.home', self._workspace))
            log(f"mounting new workspace in {self._workspace} ...")

        if MainConfigContext.get_instance().get_property('main.mount.copy') is True:
            deploy()
            log('required resources moved with success and workspace mounted here: ' + self._workspace)
        else:
            try:
                deploy()
                log('required resources moved with success and workspace mounted here: ' + self._workspace)
            except subprocess.CalledProcessError:
                log(f"Run EaseCI with super user privileges, because directory creation is impossible in directory "
                    f"{self._workspace}", err=True)
                raise WorkspaceException('Cannot create directory')
            except FileExistsError:
                if os.path.isdir(self._workspace) and os.path.exists(self._workspace + '/general.yml'):
                    return
                self._workspace = self._workspace + '/easeci'
                self.mount()


class WorkspaceException(Exception):
    def __init__(self, message):
        super().__init__(message)
