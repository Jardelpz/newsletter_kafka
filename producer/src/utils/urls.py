from flask_restful import Api, Resource
from src.handlers import Newsletter, Subscription


class HealthCheck(Resource):
    @staticmethod
    def get():
        return {'status': 'Alive and Kicking'}


def make_resources(app):
    api = Api()
    api.add_resource(HealthCheck, "/hc")
    api.add_resource(Newsletter, "/newsletter")
    api.add_resource(Subscription, "/subscription")
    api.init_app(app)
