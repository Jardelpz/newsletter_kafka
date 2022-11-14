import json

from src.database.sqllite import SqlLite

from src.utils.elasticsearch import ESManager
from src.utils.email_ import is_valid_email, send_email


def process_message(db: SqlLite, message):
    es_client = ESManager()
    users = db.select_subscribers_by_genre(message.get('genre'))
    for user in users:
        if email := is_valid_email(user['email']):
            send_email(email, message['title'], json.loads(message['body']))
            user['title'] = message['title']
            es_client.send_message(user, 'email')

    es_client.send_message(message, 'newsletter')
