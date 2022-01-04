import random
from collections import defaultdict

from WordleDictionary import WordleDictionary
from WordleTurn import WordleTurn, SQUARE


class WordleBot:
    def __init__(self) -> None:
        self.words_dictionary = WordleDictionary()

    def make_guess(self):
        # choice = self.guess_random_from_all_words()
        choice = self.guess_most_common_letters_from_dictionary()
        return choice

    # Bot option 1
    def guess_random_from_all_words(self):
        return random.choice(self.words_dictionary.words)

    # Bot option 2
    def guess_most_common_letters_from_dictionary(self):
        most_common_letters = self.words_dictionary.find_most_common_letters_no_repetitions()
        print('Most common letters: {}'.format(most_common_letters))

        best_mapping = self.words_dictionary.find_best_mapping()
        print('Best mapping is: {}'.format(best_mapping))

        if len(best_mapping) > 0:
            return best_mapping[0]

        return self.guess_random_from_all_words()

    def update_dictionary_after_turn(self, turn):
        all_occurrences = self.count_all_occurrences(turn.guess)
        green_yellow_occurrences = self.count_green_yellow_occurrences(turn.pattern)
        for i, (p, c) in enumerate(turn.pattern.pattern):
            if p == SQUARE.GREEN:
                self.words_dictionary.words = [word for word in self.words_dictionary.words if word[i] == c]
            elif p == SQUARE.YELLOW:
                self.words_dictionary.words = [word for word in self.words_dictionary.words if word[i] != c and word.count(c) >= green_yellow_occurrences[c]]
            elif p == SQUARE.MISS:
                self.words_dictionary.words = [word for word in self.words_dictionary.words if word[i] != c and word.count(c) < all_occurrences[c]]

        print('New dictionary size is: {}'.format(len(self.words_dictionary.words)))

        self.words_dictionary.five_letter_set_mapping = self.words_dictionary.create_five_letter_set_mapping()

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