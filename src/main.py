import sys
import os
import subprocess
import shutil
import sqlite3
import time
from pathlib import Path


#file imports


def main():
    #compile_to_executable()
    compile_prog()
    return 0


def compile_to_executable (output_file = "JMM", main_py = "GUI.py") -> None:
    """
    Compiles the .main file into an EXE which can be run,
    created in the current working directory.

    :param directory: Outputs file in cwd
    :param output_file: name of the output file
    :param main_py: do not change
    :return: None
    """

    def create_folder() -> None:
        """
        Simply creates the DB folder
        WARNING DELETES ANY FOLDER named
        PDFs THAT ARE IN THE DIRECTORY,
        :return None:
        """
        ORIGINAL_PATH = os.getcwd()
        if os.path.exists(Path.cwd()/"PDFs"):
            #check if dup pdf
            print("Duplicate PDFs folder in current dir...")
            print("deleting PDFs in three seconds")
            time.sleep(3)
            shutil.rmtree(Path.cwd()/"PDFs")
        else:
            #make DB dir
            DB_path = Path.cwd()/"PDFs"
            DB_path.mkdir(parents=True, exist_ok=True) #makes a directory
            try:
                #make DB path
                os.chdir(Path.cwd()/"PDFs")
                DB.create_database()
            except:
                #Expection handling
                print("problem changing dir!")
            finally:
                #move back to original dir
                os.chdir(ORIGINAL_PATH)
            #Pyinstaller_cmd
            pyinstaller_cmd_ = [
                "pyinstaller",
                "--onefile",
                "--noconsole",
                "--clean",
                "--name", output_file,
                main_py
            ]
            subprocess.run(pyinstaller_cmd_,check=True)
    return None

def compile_prog() -> None:
    ORIGINAL_PATH = os.getcwd()
    _data_dir = os.path.join(os.path.expanduser('~'), 'Documents')

    for item in os.listdir(ORIGINAL_PATH):
        _actual_item_dir = os.path.join(ORIGINAL_PATH, item)
        print(_actual_item_dir)
        if os.path.isfile(_actual_item_dir):
            shutil.copy2(_actual_item_dir, _data_dir)

if __name__ == "__main__":
    main()

