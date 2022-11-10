import json
from kafka import KafkaProducer


class Kafka:
    def __init__(self):
        self.producer = KafkaProducer(
            bootstrap_servers=['localhost:9092'],
            value_serializer=self.serializer,
            api_version=(0, 10, 2)
        )

    @staticmethod
    def serializer(message):
        return json.dumps(message).encode('utf-8')

    def send_message(self, message):
        self.producer.send('topic_test', message)
