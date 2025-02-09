from numpy.f2py.auxfuncs import throw_error
import math as m
import functools
import regex as rg
from typing_extensions import overload
import main
from collections import Counter

class VectorFunctions(object):
    def __init__(self, vector: list[int]):
        self.vector = vector

    def calculate_mag(self) -> float:
        _sum_ = 0
        for i in self.vector:
            _sum_ = _sum_ + i**2
        return m.sqrt(_sum_)

    def dot_product(self, compare_vector: list[int]) -> float:
        while True:
            if len(self.vector) == len(compare_vector):
                break
            else:
                if len(self.vector) > len(compare_vector):
                    compare_vector.append(0)

                elif len(self.vector) < len(compare_vector):
                    self.vector.append(0)
        sum_ = 0
        for i in compare_vector:
            sum_ = sum_ + compare_vector[i]*self.vector[i]

        return sum_

    def calculate_vector_angle(self, comparison_vector: list[int], comparison_vector_2: list[int]) -> float:
        v2 = VectorFunctions(comparison_vector_2)
        v1 = VectorFunctions(comparison_vector)

        v1_mag = v1.calculate_mag()
        v2_mag = v2.calculate_mag()

        v1_v2_dot = v1.dot_product(compare_vector=v2.vector)

        return m.acos(v1_v2_dot/(v1_mag*v2_mag))


class StringFunctions(VectorFunctions):
    def __init__(self, vector: list[int], pages: list[str], question: str):
        super().__init__(vector)
        self.question = question
        self.pages = pages
        self.dict_words = {}

    def delete_punctuation(self) -> None:
        """
        Removes all regex from self.string_list
        :return: None
        """
        self.pages = [rg.sub(r'[^a-zA-Z]', '', item) for item in self.pages]

    def count_words_and_transform_dict(self) -> None:
        """
        Where each key is a word and each value
        is the amount that word is said
        :return:
        """
        words_found = rg.findall(r'\b[a-zA-Z]+\b', " ".join(self.pages).tolower())
        word_counts = Counter(words_found)
        self.dict_words = {word: word_counts[word] for word in main.english_words if word in word_counts}
        pass


    def create_vector(self):
        # takes in a set a word_set probably made by build clean set maybe smth like: [cucumber, apple, banana, pineapple, coconut]
        # takes in a dictionary with word counts, smth like {cucumber: 2, apple:1, pineapple:3}
        # returns a vector array that puts the word counts from the dictionary in the same format as the word set.
        # ex: [2,1,0,3,0]

        vector = []
        for value in self.dict_words.values():
            vector.append(value)

        return vector