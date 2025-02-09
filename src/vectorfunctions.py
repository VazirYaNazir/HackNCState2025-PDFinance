import numpy as np
import nltk
from nltk.tokenize import word_tokenize
nltk.download('punkt_tab')



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

def build_clean_set(*dicts: dict):
    s = set() #makes empty set
    dictionaries = dicts[0]
    for d in dictionaries:
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
    return vectors

def angle_between_vectors(vector1: list, vector2:list):
    v1 = np.array(vector1)
    v2 = np.array(vector2)

    min_length = min(len(v1), len(v2))
    v1 = v1[:min_length]
    v2 = v2[:min_length]
    dot_product = np.dot(v1,v2)
    magnitude_multiply = np.linalg.norm(v1) * np.linalg.norm(v2)
    angle_in_rad = np.arccos(dot_product/magnitude_multiply)
    angle_in_degrees = np.degrees(angle_in_rad)
    return float(angle_in_degrees)

def make_pdf_vector_with_question(strings: list,question: str):
    word_dicts = []
    temp_ = [question]
    strings.extend(temp_)

    for s in strings:
        word_dicts.append(word_count_dictionary(s))
    #works until here
    word_set = build_clean_set(word_dicts)

    vectors = []
    for d in word_dicts:
        vectors.append(word_vector(word_set,d))


    question_vector = vectors[-1]
    del vectors[-1]
    pdf_vector = np.array(len(np.array(vectors)))
    for vector in vectors:
        pdf_vector = np.add(pdf_vector, np.array(vector))

    list(pdf_vector).append(question_vector)

    return pdf_vector