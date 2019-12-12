import sys
from flask import Flask
from flask_restful import Api
from app.api.api_context import ApiContext
from app.lib.runner.runner import EaseRunner

app = Flask(__name__)
api = Api(app)

ApiContext(api).init_controller_list()
EaseRunner.get_instance(sys.argv)

"""
Running method for development mode
"""
if __name__ == '__main__':
    ApiContext(api).init_controller_list()
    EaseRunner.get_instance(sys.argv)
    app.run()
