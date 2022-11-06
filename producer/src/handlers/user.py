import logging

import pydantic
import requests

from flask_restful import Resource

from src.utils.apm import apm
from src.schemas.user.create import User as UserSchema
from src.database.sqllite import SqlLite


class User(Resource):

    def __init__(self):
        self.db = SqlLite(apm)

    def post(self):
        payload = requests.json

        try:
            subscription = UserSchema(**payload)
        except pydantic.ValidationError as e:
            self.apm.capture_exception(e)
            return 'error in request body', 422

        self.db.insert_subscription(subscription)
        return 'Upload done!', 201

    def delete(self, title):
        # delete post from database
        self.db.delete_by_title(title)
        return "title deleted", 200

    def get(self, title):
        # find in cache, else in database (SQL) - elastic so no consumer
        if news := self.cache.get(title):
            return news, 200

        else:
            news = self.db.select_news_by_title(title)
            return news, 200

