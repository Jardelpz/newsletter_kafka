import json
import ast

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
        process_message(db, ast.literal_eval(json.loads(message.value.decode('utf-8'))))


if __name__ == '__main__':
    try:
        main()
    except Exception as e:
        print(e)

# trabalhar com cenario - e se meu produtor mandar mensagem pro topico e ningue tiver consumindo
# eu perco a mensagem? tem o earlsit na isntancia do consumer que faz algo assim acho