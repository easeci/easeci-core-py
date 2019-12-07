import os.path

from lib.config.utils import pwd
from lib.io.io_yml import yml_get
from lib.log.logger import log
import os.path

"""
MainConfigContext is singleton class that hold context for application
By object of this class we can get configuration properties, preferences etc.
The main configuration file is 'general.yml' which must be places in workspace directory
"""


class MainConfigContext:
    __instance = None
    _config_file = None
    _config_file_path = None
    _conf_file_name = 'general.yml'

    """
    Ease will scan this paths in searching for general.yml
    """
    _paths = [
        '/usr/local/share/ease',
        '/home/ease'
    ]

    def __init__(self):
        raise RuntimeError('Cannot instantiate singleton by constructor!')

    @classmethod
    def get_instance(cls, workspace=None):
        if cls.__instance is None:
            cls.__instance = cls.__new__(cls)
            if workspace is not None:
                cls.__instance._paths = [workspace] + cls.__instance._paths
        return cls.__instance

    """
    Search for configuration file, similar to scan_paths() but
     * is using only if user specify custom path to workspace
     This iterates through 'paths' list till the general.yml file found
    """
    def search_config(self, workspace):
        paths = [
            workspace + '/' + self._conf_file_name,
            workspace + '/easeci/' + self._conf_file_name
        ]
        for current in paths:
            res = os.path.exists(current)
            if res is True:
                self._config_file_path = current
                log('main configuration file correctly detected')
        if self._config_file_path is None:
            log('main configuration file not found!', err=True)

    def all_paths(self):
        path = pwd()
        return self._paths + [path.strip() + '/config']

    """
    This method scans path in order to searching for config general.yml file
    * method is used only if user not specified path in startup
    If path is found this returns True
    If path is not found returns False
    """
    def scan_paths(self):
        def is_config_exist(config_path):
            if config_path is None:
                return False
            file_path = config_path + '/' + self._conf_file_name
            return os.path.isfile(file_path)
        for path in self.all_paths():
            if is_config_exist(path):
                self._config_file_path = path + '/' + self._conf_file_name
                log(f"configuration detected: {self._config_file_path}")
                return True
        return False

    def get_property(self, refs):
        if self._config_file_path is not None and refs is not None:
            return yml_get(self._config_file_path, refs)

    def info(self):
        return {
            'general': self._config_file_path,
            'workspace': self._config_file_path[:-12]
        }
