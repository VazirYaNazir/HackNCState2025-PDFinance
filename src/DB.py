import sqlite3
import os
import pathlib as Path
from fileinput import filename

from PyPDF2 import PdfReader

db_name = 'PDFs.db'
pdf_folder = 'PDFs'

def create_database():
    connection = sqlite3.connect('pdfs.db')
    cursor = connection.cursor()
    # ID: Key
    # Filename: String containing the name of the pdf uploaded
    # Pages: List containing strings which contain the text on each page
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS pdfs (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        filename TEXT NOT NULL,
        pages BLOB NOT NULL
    )
    '''
    )

    cursor.execute('''
    CREATE TABLE IF NOT EXISTS vectors (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        pdf_vector BLOB NOT NULL,
        page_vectors BLOB NOT NULL
    )
    '''
    )

    connection.commit()
    connection.close()

def store_pdf(filename):
    pdf_path = Path.cwd()/"PDFs"/filename
    temp = []

    reader = PdfReader(pdf_path)
    for page in reader.pages:
        temp.append(page.extract_text())

    connection = sqlite3.connect(db_name)
    cursor = connection.cursor()

    cursor.execute

    connection.commit()
    connection.close()

def retrieve_pdf(pdf_id):
    connection = sqlite3.connect(db_name)
    cursor = connection.cursor()

    cursor.execute('''
    SELECT pages
    FROM pdfs
    WHERE id = ?
    ''',
    (pdf_id,))


