import sqlite3
import os

class DB_process:
    def __init__(self, db_name = 'pdf_storage.db'):
        self.db_name = db_name
        self.create_database():

        def create_database(self):
            connection = sqlite3.connect(self.db_name)
            cursor = connection.cursor()

            cursor.execute('''
            CREATE TABLE IF NOT EXISTS pdfs (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                filename TEXT NOT NULL,
                content BLOB NOT NULL
            '''
            )

            cursor.execute('''
            CREATE TABLE IF NOT EXISTS vectors (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                pdf_id INTEGER NOT NULL,
                vector 
            '''
            )


class DB_access(DB_process):
        pass