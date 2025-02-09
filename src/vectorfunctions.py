from pypdf import PdfReader
import numpy as np
from transformers.data.data_collator import tolist

import DB
from nltk.tokenize import word_tokenize
import nltk

from src.DB import get_last_id, retrieve_pdf

nltk.download('punkt_tab')

reader = PdfReader("pdfs/PrinciplesofFinance-WEB.pdf")
for page in reader.pages:
    print(page.extract_text())


def clean_string(str):
    # Keep only alphabetical characters in the string
    cleaned_string = ""
    for char in str:
        if char.isalpha() or char==" ":  # Check if the character is a letter or a space
            #line missing here!!!
            cleaned_string += char

    return cleaned_string.lower()

def word_count_dictionary(str1):
    #returns a dictonary containing frequencies of any word in string
    #e.g. str1 = 'quick brown fox is quick.'
    x = {}
    str1 = clean_string(str1)
    words = word_tokenize(str1)
    for b in words:
        if b in x:
            x[b]+=1
        else:
            x[b] = 1
    return(x)


def word_vector(word_set, word_dict):
    vector = []
    for word in word_set:
        # Get the value from word_dict or use 0 if the word is not found
        value = word_dict.get(word, 0)
        vector.append(value)
    return vector

def build_clean_set(*dicts):
    s = set() #makes empty set
    for d in dicts:
        for word in d.keys():
            s.add(word)
    return sorted(s)


def make_page_vectors(strings, question):
    word_dicts = []
    strings.append(question)
    for s in strings:
        word_dicts.append(word_count_dictionary(s))
    word_set = build_clean_set(word_dicts)
    vectors = []
    for d in word_dicts:
        vectors.append(word_vector(word_set,d))
    print(word_set)
    return vectors

def angle_between_vectors(vector1, vector2):
    v1 = np.array(vector1)
    v2 = np.array(vector2)

    dotProduct = np.dot(v1,v2)
    magnitudeMultiply = np.linalg.norm(v1) * np.linalg.norm(v2)
    angle_in_rad = np.arccos(dotProduct/magnitudeMultiply)
    angle_in_degrees = np.degrees(angle_in_rad)
    return angle_in_degrees

# creating vectors for each pdf
def create_vectorsPdfs_with_question(question):
    pdfTexts = []
    for i in range(1,DB.get_last_id()+1):
        pdfText = ""
        for page in retrieve_pdf(i):
            pdfText.append(page)

        pdfTexts.append(pdfText)

    pdfTexts.append(question)

    return make_page_vectors(pdfTexts)


#create the vectors for the questions
def createVectorsPagesWithQuestion(question,pdfIndex):
    pagesList = []
    for page in retrieve_pdf(pdfIndex):
        pagesList.append(page)

    pagesList.append(question)

    return make_page_vectors(pagesList)

def checkVectorWithQuestionVector(vectors):
    minimum = angle_between_vectors(vectors[0], vectors[-1])
    id = 1
    for index, vector in enumerate(vectors[1:-1]):
        if minimum > angle_between_vectors(vector, vectors[-1]):
            minimum = angle_between_vectors(vector, vectors[-1])
            id += index + 1
        else:
            continue

def make_pdf_vector_with_question(strings,question):
    word_dicts = []
    strings.append(question)
    for s in strings:
        word_dicts.append(word_count_dictionary(s))
    word_set = build_clean_set(word_dicts)
    vectors = []
    for d in word_dicts:
        vectors.append(word_vector(word_set,d))

    questionVector = vectors.pop()
    pdfVector = np.array()
    for vector in vectors:
        pdfVector.add(pdfVector, np.array(vector))


    return tolist(pdfVector).append(questionVector)