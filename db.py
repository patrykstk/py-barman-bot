import os
import sqlite3
from utils import log

class Database:
    def __init__(self):
        db_dir = "database"
        if not os.path.exists(db_dir):
            os.makedirs(db_dir)
            log("INITIALIZATION", f"Created directory: {db_dir}")

        db_path = os.path.join(db_dir, "barman.db")
        db_exists = os.path.exists(db_path)

        self.conn = None
        self.cur = None

        try:
            self.conn = sqlite3.connect(db_path)
            self.cur = self.conn.cursor()
            log("INITIALIZATION", f"Successfully connected to the database: {db_path}")

            self.setup()
            if not db_exists:
                log("INITIALIZATION", "Creating new database and schema.")
            else:
                log("INITIALIZATION", "Database already exists, checking schema.")

        except sqlite3.Error as e:
            log("ERROR", f"Error connecting to database '{db_path}': {e}")
            raise ConnectionError(f"Failed to connect to database: {e}")

    def setup(self):
        schema_path = os.path.join("database", "schema.sql")
        try:
            with open(schema_path, "r", encoding="utf-8") as f:
                sql_script = f.read()
            self.cur.executescript(sql_script)
            self.conn.commit()
            log("INITIALIZATION", f"Database schema loaded from '{schema_path}'.")
        except FileNotFoundError:
            log("ERROR", f"Schema file '{schema_path}' not found. Make sure it exists.")
            raise FileNotFoundError(f"SQL schema file not found: {schema_path}")
        except sqlite3.Error as e:
            log("ERROR", f"Error executing SQL script from '{schema_path}': {e}")
            self.conn.rollback()
            raise RuntimeError(f"Error during database schema setup: {e}")

    def close(self):
        if self.conn:
            self.conn.close()
            log("INITIALIZATION", "Database connection closed.")