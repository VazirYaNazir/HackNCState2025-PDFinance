import os.path
import sqlite3
import pickle
from PyPDF2 import PdfReader
from functools import wraps


db_name = 'PDFs.db'
def with_pdf_directory(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        current_dir = os.getcwd()
        parent_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
        pdf_dir = os.path.join(parent_dir, "PDFs")
        try:
            os.chdir(os.path.abspath(os.path.join(os.getcwd(), "..")))
            if os.path.exists("PDFs"):
                os.chdir(pdf_dir)
            return func(*args, **kwargs)
        finally:
            os.chdir(current_dir)
    return wrapper


@with_pdf_directory
def get_last_id():
    connection = sqlite3.connect(db_name)
    cursor = connection.cursor()

    cursor.execute('SELECT MAX(id) FROM pdfs')
    max_id = cursor.fetchone()[0]

    connection.close()
    return max_id if max_id is not None else 0

@with_pdf_directory
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

@with_pdf_directory
def store_pdf(file_path: str) -> None:
        file_name = os.path.basename(file_path)
        pages = []

        reader = PdfReader(file_path)
        for page in reader.pages:
            pages.append(page.extract_text())

        connection = sqlite3.connect(db_name)
        cursor = connection.cursor()

        cursor.execute('INSERT INTO pdfs (filename, pages) VALUES (?, ?)', (file_name, pickle.dumps(pages)))

        connection.commit()
        connection.close()