import re
from collections import defaultdict
from enum import Enum

WORDLE_WORD_LENGTH = 5


class SQUARE(Enum):
    GREEN = 0
    YELLOW = 1
    GREY = 2


STR_TO_SQUARE = {
    'V': SQUARE.GREEN,
    '?': SQUARE.YELLOW,
    'X': SQUARE.GREY
}


class GuessPattern:
    ALL_GREENS = 'VVVVV'

    def __init__(self, first_param, guessed_word, init_from_str=False) -> None:
        if init_from_str:
            self.pattern = self.create_pattern_from_str(first_param, guessed_word)
        else:
            self.pattern = self.create_pattern(first_param, guessed_word)

    def print_pattern(self):
        pattern_str = ''

        for (p, c) in self.pattern:
            if p == SQUARE.GREEN:
                pattern_str += 'V'
            elif p == SQUARE.YELLOW:
                pattern_str += '?'
            elif p == SQUARE.GREY:
                pattern_str += 'X'
            else:
                pattern_str += '_'

        return pattern_str

    @staticmethod
    def create_pattern(secret_word, guessed_word):
        assert len(secret_word) == WORDLE_WORD_LENGTH and len(guessed_word) == WORDLE_WORD_LENGTH

        green_occurrences = defaultdict(int)
        for s, g in zip(secret_word, guessed_word):
            if s == g:
                green_occurrences[g] += 1

        occurrences = defaultdict(int)
        pattern = []
        for s, g in zip(secret_word, guessed_word):
            if s == g:
                pattern.append((SQUARE.GREEN, g))
            else:
                square = SQUARE.YELLOW if g in secret_word and occurrences[g] < secret_word.count(g) - \
                                          green_occurrences[g] else SQUARE.GREY
                pattern.append((square, g))
                occurrences[g] += 1

        return pattern

    @staticmethod
    def create_pattern_from_str(pattern_str, guessed_word):
        return [(STR_TO_SQUARE[c1], c2) for c1, c2 in zip(pattern_str, guessed_word)]

    @staticmethod
    def validate_pattern(stdin_pattern):
        return re.match('^[VX?]{5}$', stdin_pattern)


# class PatternCache(object):
#     def __init__(self, puzzle_words, valid_words) -> None:
#         super().__init__()
#         self.cache = self.create_pattern_mapping(puzzle_words, valid_words)
#
#     def get(self, secret_word, guessed_word):
#         return self.cache[(secret_word, guessed_word)]
#
#     @staticmethod
#     def create_pattern_mapping(puzzle_words, valid_words):
#         pattern_mapping = {}
#         for valid_word in valid_words:
#             for puzzle_word in puzzle_words:
#                 pattern_mapping[(puzzle_word, valid_word)] = GuessPattern(puzzle_word, valid_word)
#         return pattern_mapping



