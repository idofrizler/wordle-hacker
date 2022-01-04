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
        self.five_letter_set_mapping = self.create_five_letter_set_mapping()

    def find_most_common_letters_no_repetitions(self):
        dict = defaultdict(int)
        for word in self.words:
            for c in set([c for c in word]):
                dict[c] += 1

        most_common = sorted(dict.items(), key=lambda item: item[1])
        return most_common[-5:]

    def create_five_letter_set_mapping(self):
        dict = defaultdict(list)
        for word in self.words:
            word_set = ''.join(sorted(set([c for c in word])))
            dict[word_set].append(word)

        return dict

    def find_best_mapping(self):
        most_common_letters_keys = [t[0] for t in self.find_most_common_letters_no_repetitions()]
        word_set = ''.join(sorted(set([c for c in most_common_letters_keys])))

        match = self.five_letter_set_mapping.get(word_set, [])
        return match

    # def get_valid_words_for_pattern(self, pattern):