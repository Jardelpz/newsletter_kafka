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

    def select_subscribers_by_genre(self, genre):
        cur = self.conn.cursor()
        cur.execute("SELECT * FROM subscription WHERE genre=?", (genre,))

        rows = cur.fetchall()
        if rows:
            return rows
        return []
