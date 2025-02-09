import math as m
import regex as rg
from collections import Counter
import main

# ---------------------------
# Vector Functions
# ---------------------------

def calculate_mag(vector: list[int]) -> float:
    """
    Calculate the magnitude (Euclidean norm) of a vector.

    Args:
        vector: A list of integers representing the vector.

    Returns:
        The magnitude of the vector.
    """
    return m.sqrt(sum(x ** 2 for x in vector))


def dot_product(vector1: list[int], vector2: list[int]) -> float:
    """
    Calculate the dot product of two vectors. Pads the shorter vector with zeros.

    Args:
        vector1: The first vector as a list of integers.
        vector2: The second vector as a list of integers.

    Returns:
        The dot product of the two vectors.
    """
    v1 = vector1.copy()
    v2 = vector2.copy()

    if len(v1) > len(v2):
        v2.extend([0] * (len(v1) - len(v2)))
    elif len(v2) > len(v1):
        v1.extend([0] * (len(v2) - len(v1)))

    return sum(a * b for a, b in zip(v1, v2))


def calculate_vector_angle(vector1: list[int], vector2: list[int]) -> float:
    """
    Calculate the angle (in radians) between two vectors.
    Raises an exception if one of the vectors has zero magnitude.

    Args:
        vector1: The first vector as a list of integers.
        vector2: The second vector as a list of integers.

    Returns:
        The angle between the two vectors in radians.

    Raises:
        ValueError: If either vector has zero magnitude.
    """
    mag1 = calculate_mag(vector1)
    mag2 = calculate_mag(vector2)

    if mag1 == 0 or mag2 == 0:
        raise ValueError("Cannot calculate angle between vectors with zero magnitude.")

    dp = dot_product(vector1, vector2)
    return m.acos(dp / (mag1 * mag2))


# ---------------------------
# String (Word) Functions
# ---------------------------

def count_words_and_transform_dict(pages: list[str]) -> dict:
    """
    Given a list of pages (strings), count the occurrences of each word.
    Only words that appear in main.english_words are kept.

    Args:
        pages: A list of strings representing the text from each page.

    Returns:
        A dictionary mapping each word (key) to its count (value).
    """
    text = " ".join(pages).lower()
    words_found = rg.findall(r'\b[a-zA-Z]+\b', text)
    word_counts = Counter(words_found)

    return {word: word_counts[word] for word in main.english_words if word in word_counts}


def create_vector(pages: list[str]) -> list[int]:
    """
    Given a list of pages, return a vector of word counts for each word in the predefined word set.

    Args:
        pages: A list of strings representing the text from each page.

    Returns:
        A list of integers where each element represents the count of a word from the predefined set.
    """
    word_counts = count_words_and_transform_dict(pages)
    return [word_counts.get(word, 0) for word in main.english_words]
