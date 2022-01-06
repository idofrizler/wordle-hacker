import copy
import re
from collections import defaultdict

import requests

ENGLISH_DICTIONARY_URL = 'https://raw.githubusercontent.com/dwyl/english-words/master/words.txt'

downloaded_dictionary = None


def init_dictionary_from_url():
    global downloaded_dictionary

    if downloaded_dictionary is not None:
        return downloaded_dictionary

    resp = requests.get(ENGLISH_DICTIONARY_URL)
    words = resp.text.splitlines()

    r = re.compile("^([a-z]|[A-Z]){5}$")
    five_letter_words = list(filter(r.match, words))
    downloaded_dictionary = [word.upper() for word in five_letter_words]

    return downloaded_dictionary


class WordleDictionary:
    def __init__(self) -> None:
        self.words = copy.deepcopy(init_dictionary_from_url())

    def find_letter_frequency_in_current_dict(self):
        frequencies = defaultdict(int)
        for word in self.words:
            for c in set([c for c in word]):
                frequencies[c] += 1

        return frequencies

    @staticmethod
    def sum_word_frequencies(word, letter_frequencies):
        freq_sum = 0
        letters_set = set()
        for c in word:
            if c not in letters_set:
                freq_sum += letter_frequencies[c]
                letters_set.add(c)

        return freq_sum

    def calc_aggregate_frequency_per_word(self):
        letter_frequencies = self.find_letter_frequency_in_current_dict()
        word_frequencies = [(word, self.sum_word_frequencies(word, letter_frequencies)) for word in self.words]
        return sorted(word_frequencies, key=lambda x: x[1], reverse=True)


