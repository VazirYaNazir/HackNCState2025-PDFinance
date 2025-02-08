import sqlite3
import os
import pathlib as Path

from PyPDF2 import PdfReader


class DB_process:
    def __init__(self, db_name = 'PDFs.db', pdf_folder = 'PDFs'):
        self.db_name = db_name
        self.pdf_folder = pdf_folder
        self.create_database()


class DB_access(DB_process):
        def store_pdf(self, filename):
            pdf_path = Path.cwd()/"PDFs"/filename
            temp = []

            reader = PdfReader(pdf_path)
            for page in reader.pages:
                temp.append(page.extract_text())

            connection = sqlite3.connect(self.db_name)
            cursor = connection.cursor()

            cursor.execute




def create_database():
    connection = sqlite3.connect('pdfs.db')
    cursor = connection.cursor()
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS pdfs (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        filename TEXT NOT NULL,
        content BLOB NOT NULL
    )
    '''
    )

    cursor.execute('''
    CREATE TABLE IF NOT EXISTS vectors (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        pdf_id INTEGER NOT NULL,
        vector BLOB NOT NULL
    )
    '''
    )
    connection.commit()
    connection.close()
