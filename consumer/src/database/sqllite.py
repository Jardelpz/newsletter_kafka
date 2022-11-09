import sqlite3
from sqlite3 import Error


class SqlLite:
    def __init__(self):
        self.conn = None
        self.start_db()

    def start_db(self):
        conn = self.create_connection('C:/Users/Jardel/PycharmProjects/online-news-kafka/producer/newsletter.db')
        if conn is not None:
            self.conn = conn

    @staticmethod
    def create_connection(db_file):
        conn = None
        try:
            conn = sqlite3.connect(db_file)
            return conn
        except Error as e:
            print(e)

        return conn

    def select_subscribers_by_genre(self, genre):
        cur = self.conn.cursor()
        cur.execute("SELECT id, name, email, age, genre, subscription_date FROM subscription WHERE genre=?", (genre,))

        rows = cur.fetchall()
        result = []
        if rows:
            for row in rows:
                result.append({
                    "id": row[0],
                    "name": row[1],
                    "email": row[2],
                    "age": row[3],
                    "genre": row[4],
                    "subscription_date": row[5]
                })

        return result
