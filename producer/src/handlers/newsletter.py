import logging

import pydantic
import requests

from flask_restful import Resource

from src.utils.apm import apm
from src.utils.kafka import Kafka
from src.utils.redis import Cache
from src.schemas.newsletter.create import CreateLetter
from src.database.sqllite import SqlLite


class Newsletter(Resource):

    def __init__(self):
        self.cache = Cache()
        self.kafka = Kafka()
        self.apm = apm
        self.db = SqlLite(apm).create_connection()

    def post(self):
        payload = requests.json

        try:
            news = CreateLetter(**payload)
        except pydantic.ValidationError as e:
            self.apm.capture_exception(e)
            return 'error in request body', 422

        # save to database
        # send to kafka
        # send to cache
        # cover by apm
        logging.info('sending news to cache!')
        self.cache.save(news.title, news)
        logging.info('sending message to kafka topic!')
        self.kafka.send_message(news)
        self.db.insert_news(news)
        return 'Upload done!', 201

    def delete(self, title):
        # delete post from database
        self.db.delete_by_title(title)
        return "title deleted", 200

    def get(self, title):
        # find in cache, else in database (SQL) - elastic so no consumer
        if news := self.cache.get(title):
            return news, 200

        news = self.db.select_news_by_title(title)
        return news, 200

