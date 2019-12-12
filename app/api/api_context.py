"""
This class is responsible for initialization all controller classes in this application.
In order to add new controller just will be listen URI path, just add name of controller's
class to `controller_register` list. Then context of API will automatically initialize
instance of specified class.
"""
from app.api.info import InfoController

controller_register = [
    InfoController
]


class ApiContext:
    def __init__(self, api, controllers=None):
        self.controllers_predefined = controllers
        self.api = api
        self.controllers_initialized = [
        ]

    def init_controller_list(self):
        def init(controller_list):
            for controller in controller_list:
                ready = controller(self.api)
                self.controllers_initialized.append(ready)

        if self.controllers_predefined is not None:
            init(self.controllers_predefined)
        else:
            init(controller_register)


