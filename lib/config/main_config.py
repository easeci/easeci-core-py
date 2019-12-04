import subprocess
import os.path

from lib.io.io_yml import yml_load, yml_get


class MainConfigContext:
    __instance = None
    _config_file = None
    _config_file_path = None
    _conf_file_name = 'general.yml'

    """
    Ease will scan this paths in searching for general.yml
    """
    _paths = [
        '/usr/local/ease',
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

    def all_paths(self):
        pwd = subprocess.check_output('pwd', shell=True)
        path = pwd.decode('utf-8')
        return self._paths + [path[:-1] + '/config']

    """
    This method scans path in order to searching for config general.yml file
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
                print(f'==> [EaseCI] configuration detected: {self._config_file_path}')
                return True
        return False

    def read_config_file(self):
        self._config_file = yml_load(self._config_file_path)
        return self._config_file

    def get_property(self, refs):
        return yml_get(self._config_file_path, refs)
