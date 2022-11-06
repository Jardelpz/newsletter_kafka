import sqlite3
from sqlite3 import Error
from src.utils.apm import ElasticAPM


class SqlLite:
    def __init__(self, apm: ElasticAPM):
        self.apm = apm
        self.conn = None

    def start_db(self):
        conn = self.create_connection('newsletter.db') #esta base precisara ser compartilha entre produtor e consumidor para acessar a mesma informacao (mudar path)
        if conn is not None:
            self.conn = conn
            sql_newsletter = """ CREATE TABLE IF NOT EXISTS newsletter (
                                                    id integer PRIMARY KEY AUTOINCREMENT,
                                                    title text NOT NULL,
                                                    genre text NOT NULL,
                                                    body text NOT NULL,
                                                    creation_date NOT NULL text,
                                                    images text
                                                ); """

            sql_subscription = """ CREATE TABLE IF NOT EXISTS subscription (
                                                                id integer PRIMARY KEY AUTOINCREMENT,
                                                                name text NOT NULL,
                                                                email text NOT NULL,
                                                                age integer NOT NULL,
                                                                genre text NOT NULL,
                                                                subscription_date NOT NULL text,
                                                                images text
                                                            ); """

            self.create_table(sql_newsletter)
            self.create_table(sql_subscription)

    def create_connection(self, db_file):
        conn = None
        try:
            conn = sqlite3.connect(db_file)
            return conn
        except Error as e:
            self.apm.capture_exception(e)
            print(e)

        return conn

    def create_table(self, create_table_sql):
        try:
            c = self.conn.cursor()
            c.execute(create_table_sql)
        except Error as e:
            self.apm.capture_exception(e)
            print(e)

    def insert_news(self, newsletter):

        sql = ''' INSERT INTO newsletter(title, genre, body, images, creation_date)
                  VALUES(:title, :genre, :body, :images, :creation_date) '''
        cur = self.conn.cursor()
        cur.execute(sql, **newsletter.dict())
        self.conn.commit()
        return cur.lastrowid

    def insert_subscription(self, subscription):
        sql = ''' INSERT INTO subscription(name, email, age, body, genre, subscription_date)
                  VALUES(:name, :email, :age, :body, :genre, :subscription_date) '''
        cur = self.conn.cursor()
        cur.execute(sql, **subscription.dict())
        self.conn.commit()
        return cur.lastrowid

    def select_news_by_title(self, title):
        cur = self.conn.cursor()
        cur.execute("SELECT * FROM newsletter WHERE title=?", (title,))

        rows = cur.fetchall()
        if rows:
            return rows[0]
        return []

    def delete_by_title(self, title):
        sql = 'DELETE FROM tasks WHERE title=?'
        cur = self.conn.cursor()
        cur.execute(sql, (title,))
        self.conn.commit()
