import os
import sqlite3

class Database:
    def __init__(self):
        db_exists = os.path.exists("database/barman.db")

        self.conn = sqlite3.connect("database/barman.db")
        self.cur = self.conn.cursor()
        self.setup()

        if not db_exists:
            # self.seed()
            print("Tworze baze danych")

    def setup(self):
        with open("database/schema.sql", "r", encoding="utf-8") as f:
            sql_script = f.read()
        self.cur.executescript(sql_script)