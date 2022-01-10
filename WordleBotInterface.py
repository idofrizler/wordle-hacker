import random
from abc import abstractmethod, ABC
from collections import defaultdict

from WordleTurn import SQUARE


class WordleBotInterface(ABC):
    def __init__(self, game, puzzle_words, valid_words) -> None:
        super().__init__()
        self.game = game
        self.words_dictionary = WordleDictionary(puzzle_words, valid_words)

    def play_game(self):
        while not self.game.is_over():
            self.play_turn()

    def play_turn(self):
        assert not self.game.is_over()

        guess = self.make_guess() if len(self.game.turns) > 0 else 'TARES'
        turn = self.game.play_turn(guess)
        self.update_after_turn(turn)

    def make_guess(self) -> str:
        choice = self.choose_optimal_word()
        return choice

    def guess_random_from_current_dict(self):
        return random.choice(self.words_dictionary.remaining_puzzle_words)

    @abstractmethod
    def choose_optimal_word(self):
        pass

    @abstractmethod
    def update_after_turn(self, turn):
        pass

    @staticmethod
    def count_all_occurrences(guess):
        occurrences = defaultdict(int)
        for c in guess:
            occurrences[c] += 1
        return occurrences

    @staticmethod
    def count_green_yellow_occurrences(pattern):
        occurrences = defaultdict(int)
        for (p, c) in pattern.pattern:
            if p == SQUARE.GREEN or p == SQUARE.YELLOW:
                occurrences[c] += 1
        return occurrences


class WordleDictionary(object):
    def __init__(self, puzzle_words, valid_words) -> None:
        self.remaining_puzzle_words = puzzle_words
        self.valid_words = valid_words
