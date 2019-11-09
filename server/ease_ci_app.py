import sys
from flask import Flask
from flask_restful import Api
from api.api_context import ApiContext
from lib.runner.runner import EaseRunner

app = Flask(__name__)
api = Api(app)

if __name__ == '__main__':
    ApiContext(api).init_controller_list()
    EaseRunner.get_instance(sys.argv)
    app.run()
