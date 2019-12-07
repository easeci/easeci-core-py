from flask_restful import Resource
from flask import jsonify

from lib.config.main_config import MainConfigContext


class InfoController:
    def __init__(self, api):
        api.add_resource(Info, '/')
        api.add_resource(ContextInfo, '/context')


class Info(Resource):
    def __init__(self):
        self.status = 'OK'

    def serialize(self):
        return {self.status: 'OK'}

    def get(self):
        return jsonify(self.serialize())

    def post(self):
        return jsonify({'method': 'POST'})


class ContextInfo(Resource):

    def get(self):
        return jsonify(MainConfigContext.get_instance().info())
