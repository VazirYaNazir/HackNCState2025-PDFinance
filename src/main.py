import os
import sqlite3
import shutil
import nltk
from nltk.corpus import words

#file imports
import DB
import GUIR


def main():
    create_db()
    # GUI.run_gui()
    GUIR.run_gui()
    return 0


def create_db() -> None:
    current_dir = os.getcwd()
    parent_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
    pdf_dir = os.path.join(parent_dir, "PDFs")
    try:
        os.chdir(os.path.abspath(os.path.join(os.getcwd(), "..")))
        if not os.path.exists("PDFs"):
            os.makedirs("PDFs")
            os.chdir(pdf_dir)
            try:
                con_db = sqlite3.connect("PDFs.db")
                cursor = con_db.cursor()
                cursor.execute('''
                CREATE TABLE IF NOT EXISTS pdfs (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    filename TEXT NOT NULL,
                    pages BLOB NOT NULL
                )
                ''')
                con_db.commit()
                con_db.close()
            except:
                print("were cooked!")
        else:
            print("dir already exists!")
    except:
        print("couldn't change to parent dir")
    finally:
        os.chdir(current_dir)


class File_Handler:
    def __init__(self,path: str):
        self.path = path

    def move_file(self, move_path: str):
        current_dir = os.path.dirname(__file__)
        pdfs_dir = os.path.join(current_dir, "..", "pdfs")
        file_name = os.path.basename(move_path)
        destination_path = os.path.join(pdfs_dir, file_name)
        shutil.move(move_path, destination_path)
        DB.store_pdf(destination_path)


nltk.download('words')
english_words = list(words.words())

def get_english_words():
    """BE VERY CAREFUL WITH THIS!!!"""
    return english_words


if __name__ == "__main__":
    main()