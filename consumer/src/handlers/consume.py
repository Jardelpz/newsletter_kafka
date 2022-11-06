from src.database.sqllite import SqlLite

from src.utils.elasticsearch import ESManager
from src.utils.email import is_valid_email, send_email


def process_message(db: SqlLite, message):
    es_client = ESManager()
    users = db.select_subscribers_by_genre(message.get('genre'))
    es_client.send_message(message, 'newsletter', 'newsletter_post')
    for user in users:
        if email := is_valid_email(user['email']):
            send_email(email, message['body'], message['title'])
            es_client.send_message(user, 'email', 'email_sent')

