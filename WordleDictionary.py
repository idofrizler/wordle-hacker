import copy
import re
import ast
from collections import defaultdict

import requests

ENGLISH_DICTIONARY_URL = 'https://raw.githubusercontent.com/dwyl/english-words/master/words.txt'
WORDLE_PUZZLE_WORDS = 'https://gist.githubusercontent.com/yonbergman/2fa71b216475cf6bc18cb2bf95e437d6/raw/f23fc2e9705ba48ac94ef9d034fe5ec24697c431/wordle.js'

downloaded_dictionary = None


def init_dictionary_from_wordle_source():
    global downloaded_dictionary

    if downloaded_dictionary is not None:
        return downloaded_dictionary

    resp = requests.get(WORDLE_PUZZLE_WORDS)
    puzzle_words_str = resp.text.splitlines()[0]
    puzzle_words = ast.literal_eval(puzzle_words_str[20:-1])
    downloaded_dictionary = [word.upper() for word in puzzle_words]

    return downloaded_dictionary


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
        self.words = copy.deepcopy(init_dictionary_from_wordle_source())

    def find_letter_frequency_in_current_dict(self):
        frequencies = defaultdict(int)
        for word in self.words:
            for c in set([c for c in word]):
                frequencies[c] += 1

        return frequencies

    @staticmethod
    def sum_word_information_gain(word, letter_frequencies, total_word_count):
        information_gain_sum = 0
        letters_set = set()
        for c in word:
            if c not in letters_set:
                information_gain_sum += 1.0-abs(0.5-(float(letter_frequencies[c])/total_word_count))
                letters_set.add(c)

        return information_gain_sum

    def calc_information_gain_per_word(self):
        letter_frequencies = self.find_letter_frequency_in_current_dict()
        word_information_gain = [(word, self.sum_word_information_gain(word, letter_frequencies, len(self.words))) for word in self.words]
        return sorted(word_information_gain, key=lambda x: x[1], reverse=True)

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


