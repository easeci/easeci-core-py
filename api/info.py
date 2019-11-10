from flask_restful import Resource
from flask import jsonify


class InfoController:
    def __init__(self, api):
        api.add_resource(Info, '/')


class Info(Resource):
    def __init__(self):
        self.status = 'OK'

    def serialize(self):
        return {self.status: 'OK'}

    def get(self):
        return jsonify(self.serialize())

    def post(self):
        return jsonify({'method': 'POST'})
