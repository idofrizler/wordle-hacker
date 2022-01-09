import random
from collections import defaultdict

from WordleDictionary import WordleDictionary
from WordleTurn import SQUARE, WordleTurn, GuessPattern


class WordleBotInterface(object):
    def __init__(self, game) -> None:
        super().__init__()
        self.game = game
        self.words_dictionary = WordleDictionary()

    def play_game(self):
        while not self.game.is_over():
            self.play_turn()

    def play_turn(self):
        assert not self.game.is_over()

        guess = self.make_guess() if len(self.game.turns) > 0 else 'LATER'
        turn = self.game.play_turn(guess)
        self.update_after_turn(turn)

    def make_guess(self):
        choice = self.choose_optimal_word()
        return choice

    def guess_random_from_current_dict(self):
        return random.choice(self.words_dictionary.words)

    def choose_optimal_word(self):
        pass

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
