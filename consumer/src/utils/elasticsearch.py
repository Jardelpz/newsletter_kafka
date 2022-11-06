import logging
from elasticsearch import Elasticsearch


class ESManager:

    def __init__(self):
        self.es_client = Elasticsearch(["http://elasticsearch_p:9200"])
        logging.warning(f'{self.es_client.info()}')

    def send_message(self, message, index, doc_type):
        self.es_client.index(index=index, doc_type=doc_type, body=message, id=message['id'])
