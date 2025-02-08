import sqlite3
import pathlib
import pickle
from PyPDF2 import PdfReader

db_name = 'PDFs.db'

def create_database():
    connection = sqlite3.connect(db_name)
    cursor = connection.cursor()

    cursor.execute('''
    CREATE TABLE IF NOT EXISTS pdfs (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        filename TEXT NOT NULL,
        pages BLOB NOT NULL
    )
    ''')

    cursor.execute('''
    CREATE TABLE IF NOT EXISTS vectors (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        pdf_vector BLOB NOT NULL,
        page_vectors BLOB NOT NULL
    )
    ''')

    connection.commit()
    connection.close()

def get_last_id():
    connection = sqlite3.connect(db_name)
    cursor = connection.cursor()

    cursor.execute('SELECT MAX(id) FROM pdfs')
    max_id = cursor.fetchone()[0]

    connection.close()
    return max_id if max_id is not None else 0

def store_pdf(filename):
    pdf_path = pathlib.Path.cwd() / "PDFs" / filename
    pages = []

    reader = PdfReader(pdf_path)
    for page in reader.pages:
        pages.append(page.extract_text())

    connection = sqlite3.connect(db_name)
    cursor = connection.cursor()

    cursor.execute('''
    INSERT INTO pdfs (filename, pages)
    VALUES (?, ?);
    ''', (filename, pickle.dumps(pages)))

    connection.commit()
    connection.close()

def retrieve_pdf(pdf_id):
    connection = sqlite3.connect(db_name)
    cursor = connection.cursor()

    cursor.execute('''
    SELECT pages
    FROM pdfs
    WHERE id = ?
    ''', (pdf_id,))
    pages = cursor.fetchone()

    connection.close()
    return pickle.loads(pages[0]) if pages else []

def store_vectors(vector_id, pdf_vector, page_vectors):
    connection = sqlite3.connect(db_name)
    cursor = connection.cursor()

    cursor.execute('''
    INSERT INTO vectors (id, pdf_vector, page_vectors)
    VALUES (?, ?, ?);
    ''', (vector_id, pickle.dumps(pdf_vector), pickle.dumps(page_vectors)))

    connection.commit()
    connection.close()

def retrieve_pdf_vectors(vector_id):
    connection = sqlite3.connect(db_name)
    cursor = connection.cursor()

    cursor.execute('''
    SELECT pdf_vector 
    FROM vectors 
    WHERE id = ?
     ''', (vector_id,))
    pdf_vector = cursor.fetchone()

    connection.close()
    return pickle.loads(pdf_vector[0]) if pdf_vector else None

def retrieve_page_vectors(vector_id):
    connection = sqlite3.connect(db_name)
    cursor = connection.cursor()

    cursor.execute('''
    SELECT page_vectors 
    FROM vectors 
    WHERE id = ?
    ''', (vector_id,))
    page_vectors = cursor.fetchone()

    connection.close()
    return pickle.loads(page_vectors[0]) if page_vectors else None
