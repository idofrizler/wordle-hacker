from collections import defaultdict
from enum import Enum


WORDLE_WORD_LENGTH = 5


class SQUARE(Enum):
    BLANK = 0
    GREEN = 1
    YELLOW = 2
    MISS = 3


class GuessPattern:
    def __init__(self, secret_word, guessed_word) -> None:
        self.pattern = self.create_pattern(secret_word, guessed_word)

    def print_pattern(self):
        pattern_str = ''

        for (p, c) in self.pattern:
            if p == SQUARE.GREEN:
                pattern_str += 'V'
            elif p == SQUARE.YELLOW:
                pattern_str += '?'
            elif p == SQUARE.MISS:
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
                square = SQUARE.YELLOW if g in secret_word and occurrences[g] < secret_word.count(g) - green_occurrences[g] else SQUARE.MISS
                pattern.append((square, g))
                occurrences[g] += 1

        return pattern


class WordleTurn:

    def __init__(self, guess, pattern) -> None:
        self.guess = guess
        self.pattern = pattern