from pypdf import PdfReader
import sqlite3 as sql
import numpy as np

reader = PdfReader("pdfs/PrinciplesofFinance-WEB.pdf")
for page in reader.pages:
    print(page.extract_text())


def make_vectors(strings):
    word_dicts = []
    for s in strings:
        word_dicts.append(word_count_dictionary(s))
    word_set = build_clean_set(*word_dicts)
    vectors = []
    for d in word_dicts:
        vectors.append(word_vector(word_set,d))
    print(word_set)
    return vectors
