from flask import Flask
from flask_restful import Api
from api.api_context import ApiContext

app = Flask(__name__)
api = Api(app)

if __name__ == '__main__':
    ApiContext(api).init_controller_list()
    app.run()
