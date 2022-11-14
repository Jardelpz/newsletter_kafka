import sqlite3
from sqlite3 import Error
from src.schemas.newsletter.create import CreateLetter
from src.schemas.subscription.create import Subscription
from src.utils.apm import apm


class SqlLite:
    def __init__(self):
        self.conn = None
        self.start_db()

    def start_db(self):
        conn = self.create_connection('./newsletter.db') #esta base precisara ser compartilha entre produtor e consumidor para acessar a mesma informacao (mudar path)
        if conn is not None:
            self.conn = conn
            sql_newsletter = """ CREATE TABLE IF NOT EXISTS news (
                                                    idt integer PRIMARY KEY,
                                                    title string NOT NULL,
                                                    genre string NOT NULL,
                                                    body string NOT NULL,
                                                    creation_date string NOT NULL
                                                ); """

            sql_subscription = """ CREATE TABLE IF NOT EXISTS subscription (
                                                                id integer PRIMARY KEY AUTOINCREMENT,
                                                                name string NOT NULL,
                                                                email string NOT NULL,
                                                                age integer NOT NULL,
                                                                genre string NOT NULL,
                                                                subscription_date string NOT NULL
                                                            ); """

            self.create_table(sql_newsletter)
            self.create_table(sql_subscription)

    def create_connection(self, db_file):
        conn = None
        try:
            conn = sqlite3.connect(db_file)
            return conn
        except Error as e:
            apm.capture_exception()
            print(e)

        return conn

    def create_table(self, create_table_sql):
        try:
            c = self.conn.cursor()
            c.execute(create_table_sql)
        except Error as e:
            apm.capture_exception()
            print(e)

    def insert_news(self, newsletter: CreateLetter):
        data = (newsletter.idt, newsletter.title, newsletter.genre, newsletter.body, newsletter.creation_date)
        sql = ''' INSERT INTO news(idt, title, genre, body, creation_date)
                  VALUES(?,?,?,?,?) '''
        try:
            cur = self.conn.cursor()
            cur.execute(sql, data)
            self.conn.commit()
        except Exception as e:
            apm.capture_exception()
            print(e)
            print(e)

        return cur.lastrowid

    def insert_subscription(self, subscription: Subscription):
        data = (subscription.name, subscription.email, subscription.age, subscription.genre, subscription.subscription_date)
        sql = ''' INSERT INTO subscription(name, email, age, genre, subscription_date)
                  VALUES(?,?,?,?,?) '''
        cur = self.conn.cursor()
        cur.execute(sql, data)
        self.conn.commit()
        return cur.lastrowid

    def select_news_by_title(self, title):
        cur = self.conn.cursor()
        cur.execute("SELECT idt, title, genre, body, creation_date FROM news WHERE title=?", (title,))

        rows = cur.fetchall()
        result = []
        if rows:
            for row in rows:
                result.append({
                    'id': row[0],
                    'title': row[1],
                    'genre': row[2],
                    'body': row[3],
                    'creation_date': row[4]
                })

        return result

    def select_subscriptitions_genre_by_email(self, email):
        cur = self.conn.cursor()
        cur.execute("SELECT genre FROM subscription WHERE email=?", (email,))

        rows = cur.fetchall()
        result = []
        if rows:
            for row in rows:
                result.append(row[0])

        return result

    def delete_by_title(self, title):
        sql = 'DELETE FROM news WHERE title=?'
        cur = self.conn.cursor()
        cur.execute(sql, (title,))
        self.conn.commit()

    def delete_subscription_on_genre(self, genre, email):
        sql = 'DELETE FROM subscription WHERE genre=? AND email=?'
        cur = self.conn.cursor()
        cur.execute(sql, (genre, email,))
        self.conn.commit()

