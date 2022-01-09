import copy
import re
import ast
from collections import defaultdict

import requests

ENGLISH_DICTIONARY_URL = 'https://raw.githubusercontent.com/dwyl/english-words/master/words.txt'
WORDLE_PUZZLE_WORDS = 'https://gist.githubusercontent.com/yonbergman/2fa71b216475cf6bc18cb2bf95e437d6/raw/f23fc2e9705ba48ac94ef9d034fe5ec24697c431/wordle.js'

downloaded_dictionary = None


def init_dictionary_from_wordle_source(line_num, offset):
    global downloaded_dictionary

    if downloaded_dictionary is not None:
        return downloaded_dictionary

    resp = requests.get(WORDLE_PUZZLE_WORDS)
    puzzle_words_str = resp.text.splitlines()[line_num]
    puzzle_words = ast.literal_eval(puzzle_words_str[offset:-1])
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
        # self.words = copy.deepcopy(init_dictionary_from_wordle_source(0, 20))
        self.words = copy.deepcopy(init_dictionary_from_wordle_source(1, 19))
        self.words_orig = copy.deepcopy(self.words)
