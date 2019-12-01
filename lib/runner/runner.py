"""
class EaseRunner is main context of whole Ease library.
This singleton object will manage flow of each component and module in application
Central point of entire lib application part
"""


class EaseRunner:
    __instance = None

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
        else:
            raise RunnerException("Configuration directory not specified.\n"
                                  "Please indicate path where EaseCI will create workspace for config, projects etc.\n"
                                  "Run application with argument $python3 ease_ci_app.py "
                                  "'/absolute/path/on/machine'\n\n"
                                  "Be advised that if configuration exists Ease will looking for general.yml file"
                                  "for bootstrapping instance")
        if EaseRunner.__instance is not None:
            raise RunnerException('Cannot instantiate EaseRunner twice!')
        else:
            EaseRunner.__instance = self

    def change_config_dir(self, path):
        self.config_dir = path

    def execute_pipeline(self):
        pass


class RunnerException(Exception):
    def __init__(self, message):
        super().__init__(message)
