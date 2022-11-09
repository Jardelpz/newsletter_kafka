import pickle

from redis import StrictRedis


class Cache:
    def __init__(self):
        self.cache = StrictRedis(host='localhost', port=6379)

    def save(self, key, value):
        data = self.cache.hset('post_content', key, pickle.dumps(value))
        if data:
            return data

    def get(self, key):
        if data := self.cache.hget('post_content', key):
            return pickle.loads(data)
