import re
import ast

import requests
from LoggerFactory import LoggerFactory

ENGLISH_DICTIONARY_URL = 'https://raw.githubusercontent.com/dwyl/english-words/master/words.txt'
WORDLE_PUZZLE_WORDS = 'https://gist.githubusercontent.com/yonbergman/2fa71b216475cf6bc18cb2bf95e437d6/raw/f23fc2e9705ba48ac94ef9d034fe5ec24697c431/wordle.js'
WORDLE_PUZZLE_WORDS_FILE_PATH = './wordle.js'

logger = LoggerFactory.get_logger()


def init_dictionary_from_file(line_num, offset):
    logger.info('Reading dictionary from disk')

    with open(WORDLE_PUZZLE_WORDS_FILE_PATH, 'r') as f:
        words_str = f.readlines()[line_num]
        words = ast.literal_eval(words_str[offset:-2])
        return [word.upper() for word in words]


def init_dictionary_from_wordle_source(line_num, offset):
    logger.info('Downloading dictionary from web')

    resp = requests.get(WORDLE_PUZZLE_WORDS)
    words_str = resp.text.splitlines()[line_num]
    words = ast.literal_eval(words_str[offset:-1])
    return [word.upper() for word in words]


def init_dictionary_from_url():
    resp = requests.get(ENGLISH_DICTIONARY_URL)
    words = resp.text.splitlines()

    r = re.compile("^([a-z]|[A-Z]){5}$")
    five_letter_words = list(filter(r.match, words))
    return [word.upper() for word in five_letter_words]


class DictionaryFetcher(object):
    def __init__(self) -> None:
        super().__init__()
        self.puzzle_words = init_dictionary_from_file(0, 20)
        self.valid_words = init_dictionary_from_file(1, 19) + self.puzzle_words

