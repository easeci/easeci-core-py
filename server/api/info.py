from flask_restful import Resource


class InfoController:
    def __init__(self, api):
        api.add_resource(Info, '/info')
        api.add_resource(Info, '/')


class Info(Resource):
    def get(self):
        return {"status": "OK"}
