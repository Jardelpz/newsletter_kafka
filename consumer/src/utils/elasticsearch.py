from elasticsearch import Elasticsearch


class ESManager:

    def __init__(self):
        self.es_client = Elasticsearch(hosts=["http://localhost:9200"])

    def send_message(self, message, index):
        self.es_client.index(index=index, body=message)
