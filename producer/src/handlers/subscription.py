
import pydantic

from flask_restful import Resource
from flask import request

from src.schemas.subscription.create import Subscription as SubscriptionSchema
from src.database.sqllite import SqlLite
from src.utils.apm import apm


class Subscription(Resource):

    def __init__(self):
        self.db = SqlLite()

    def post(self):
        payload = request.json

        try:
            subscription = SubscriptionSchema(**payload)
        except pydantic.ValidationError as e:
            apm.capture_exception()
            return {'status': 'error in request body'}, 422

        self.db.insert_subscription(subscription)
        return {'status': 'Subscription done!'}, 201

    def delete(self):
        payload = request.json
        genre = payload.get('genre')
        email = payload.get('email')
        self.db.delete_subscription_on_genre(genre, email)
        return "subscription deleted", 200

    def get(self):
        email = request.args.get('email')
        return self.db.select_subscriptitions_genre_by_email(email)

