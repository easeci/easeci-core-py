"""
class EaseRunner is main context of whole Ease library.
This singleton object will manage flow of each component and module in application
Central point of entire lib application part
"""
from app.lib.config.main_config import MainConfigContext
from app.lib.config.utils import pwd
from app.lib.config.workspace import WorkspaceContext
from app.lib.pre.prepare import prepare


# This function loads pipeline from file or user's input and returns yaml dict object
#   `name`     - this parameter indicate what pipeline take to loads.
#                If name is specified, function will looking for pipeline file in current workspace
#                If there is no such pipeline, exception will be raise
#   `content`  - If name is None, content will be prepared as yaml dict to processing
#   `args`     - Provide variables to pipeline execution as dictionary of key and values
#   `metadata` - this dictionary provide information about pipeline run (author, date, IP etc.)
def load_pipeline(name=None, content=None, args=None, metadata=None):
    pass


# This function is responsible for initiating pipeline execution.
# Invokes the entire sequence of events.
#   `pipeline` - is a well-formed yaml file loaded to application (from file, or from user's input etc.)
#   `output_method` - if there is no specified in pipeline `output_method` parameter,
#                   default will be loaded from general.yml file.
#                   This value tells how output of pipeline execution process will be published
#   `logs_persister` - if there is not specified in pipeline `logs_persister` parameter,
#                   default will be loaded from general.yml file.
#                   This value tells how logs will be persisted.
def execute_pipeline(pipeline, output_method, logs_persister):
    pipeline_wrapper = prepare(pipeline, output_method, logs_persister)


class EaseRunner:
    __instance = None
    _config_ctx = None
    _workspace_ctx = None

    @staticmethod
    def get_instance(argv=None):
        if EaseRunner.__instance is None:
            EaseRunner(argv)
        return EaseRunner.__instance

    def __init__(self, argv=None):
        self.argv = argv
        self.pipeline_executors = []
        if len(argv) > 1:
            self.config_dir = argv[1]
            self._config_ctx = MainConfigContext.get_instance(self.config_dir)
            self.init_workspace(in_place=False)
            self._config_ctx.search_config(self.config_dir)
        else:
            self._config_ctx = MainConfigContext.get_instance()
            is_path_found = self._config_ctx.scan_paths()
            if is_path_found:
                self.init_workspace(True)
            else:
                raise RunnerException("Configuration directory not specified.\n"
                                      "Please indicate path where EaseCI will create workspace for config, projects etc.\n"
                                      "Run application with argument $python3 ease_ci_app.py "
                                      "'/absolute/path/on/machine'\n\n"
                                      "Be advised that if configuration exists Ease will looking for general.yml file "
                                      "for bootstrapping instance")

        if EaseRunner.__instance is not None:
            raise RunnerException('Cannot instantiate EaseRunner twice!')
        else:
            EaseRunner.__instance = self

    def init_workspace(self, in_place=False):
        if in_place is False:
            self._workspace_ctx = WorkspaceContext.get_instance(self.config_dir)
            self._workspace_ctx.bootstrap()
            return
        else:
            workspace = f"{pwd()}/workspace"
            self._workspace_ctx = WorkspaceContext.get_instance(workspace)
            self._workspace_ctx.bootstrap()

    def change_config_dir(self, path):
        self.config_dir = path


class RunnerException(Exception):
    def __init__(self, message):
        super().__init__(message)
