import os
import sqlite3
import shutil
import sys
import pathlib

#file imports
import GUI


def main():
    create_DB()
    GUI.run_gui()
    return 0


def create_DB() -> None:
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
                con_db.close()
            except:
                print("were cooked!")
        else:
            print("dir already exists!")
    except:
        print("couldn't change to parent dir")
    finally:
        os.chdir(current_dir)


if __name__ == "__main__":
    main()

