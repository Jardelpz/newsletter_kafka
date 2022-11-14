import json
import ast
import elasticapm

from kafka import KafkaConsumer
from src.database.sqllite import SqlLite
from src.handlers.consume import process_message


def main():
    consumer = KafkaConsumer(
        'topic_test',
        bootstrap_servers='localhost:9092',
        # auto_offset_reset='earliest',
        api_version=(0, 10, 2)
    )

    db = SqlLite()
    for message in consumer:
        print(message.value)
        try:
            process_message(db, ast.literal_eval(json.loads(message.value.decode('utf-8'))))
        except Exception as e:
            client.capture_exception()


if __name__ == '__main__':
    try:
        client = elasticapm.Client(service_name="consumer_kafka_app", server_url="http://localhost:8200")
        elasticapm.instrument()
        client.begin_transaction(transaction_type="script")
        main()
        client.end_transaction(name=__name__, result="success")
    except Exception as e:
        client.capture_exception()
        print(e)

# trabalhar com cenario - e se meu produtor mandar mensagem pro topico e ningue tiver consumindo
# eu perco a mensagem? tem o earlsit na isntancia do consumer que faz algo assim acho