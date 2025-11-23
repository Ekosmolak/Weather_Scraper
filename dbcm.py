# dbcm.py
import sqlite3

class DBCM:
    """
    A context manager for handling SQLite DB connections.
    """

    def __init__(self, db_name: str):
        """
        Creating an instance of the context manager.
        """
        self.db_name = db_name
        self.conn = None
        self.cursor = None

    def __enter__(self):
        """
        Enters the runtinme and makes a connection to the daatabase.
        """
        self.conn = sqlite3.connect(self.db_name)
        self.cursor = self.conn.cursor()
        return self.cursor

    def __exit__(self, exc_type, exc_val, exc_tb):
        """
        Exits the runtime and closes the database connection
        """
        if self.conn:
            if exc_type is None:
                self.conn.commit()
            self.conn.close()

        return False
