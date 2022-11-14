import logging

import pydantic

from flask_restful import Resource
from flask import request

from src.utils.kafka_ import Kafka
from src.utils.redis import Cache
from src.schemas.newsletter.create import CreateLetter
from src.database.sqllite import SqlLite
from src.utils.apm import apm

class Newsletter(Resource):

    def __init__(self):
        self.cache = Cache()
        self.kafka = Kafka()
        self.db = SqlLite()

    def post(self):
        payload = request.json

        try:
            news = CreateLetter(**payload)
        except pydantic.ValidationError as e:
            apm.capture_exception()
            return 'error in request body', 422

        # save to database
        # send to kafka
        # send to cache
        # cover by apm
        logging.info('sending news to cache!')
        self.cache.save(news.title, news)
        logging.info('sending message to kafka topic!')
        self.kafka.send_message(news.json())
        self.db.insert_news(news)
        return 'Upload done!', 201

    def delete(self):
        # delete post from database
        title = request.args.get('title')
        self.db.delete_by_title(title)
        return "title deleted", 200

    def get(self):
        title = request.args.get('title')
        if news := self.cache.get(title):
            return news.dict(), 200

        news = self.db.select_news_by_title(title)
        return news, 200

