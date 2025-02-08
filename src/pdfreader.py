from pypdf import PdfReader
import sqlite3 as sql
import numpy as np

reader = PdfReader("pdfs/PrinciplesofFinance-WEB.pdf")
for page in reader.pages:
    print(page.extract_text())



