import sys
import os
import subprocess
import shutil
import sqlite3
import time
from os import getcwd
import pathlib
from shutil import copytree


#file imports


def main():
    copy_current_dir()
    return 0

def copy_current_dir():
    document_dir = pathlib.Path.home()/"Documents"/"__name__"
    print(document_dir)
    os.mkdir(document_dir)
    document_dir.mkdir(parents=True, exist_ok=True)




if __name__ == "__main__":
    main()

