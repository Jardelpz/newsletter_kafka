import json
import sys
import os

from kafka import KafkaConsumer
from src.database.sqllite import SqlLite
from src.handlers.consume import process_message


def main():
    consumer = KafkaConsumer(
        'testtopic',
        # bootstrap_servers='localhost:9092',
        # auto_offset_reset='earliest'
    )

    db = SqlLite().start_db()
    for message in consumer:
        process_message(db, json.loads(message.value))


if __name__ == '__main__':
    try:
        main()
    except KeyboardInterrupt:
        print('Interrupted')
        try:
            sys.exit(0)
        except SystemExit:
            os.exit(0)
