import math
import string
from collections import defaultdict

from WordleBotInterface import WordleBotInterface
from GuessPattern import SQUARE


class NaiveWordleBot(WordleBotInterface):
    def __init__(self, game) -> None:
        super().__init__(game)
        self.green_squares = set()
        self.green_letters = set()
        self.yellow_letters = set()
        self.grey_squares = set()
        self.grey_letters = set()

    def choose_optimal_word(self):
        # Bot option 1
        # frequencies = self.calc_aggregate_frequency_per_word()
        # Bot option 2
        # frequencies = self.calc_information_gain_per_word_from_current_dict()
        # Bot option 3
        # frequencies = self.calc_information_gain_per_word_from_orig_dict()

        # Bot option 4
        word_dict_len = len(self.words_dictionary.remaining_puzzle_words)
        greens = len(self.green_squares)
        yellows = len(self.yellow_letters)
        existing_information = greens + yellows
        print('Green squares: {}'.format(self.green_squares))
        print('Yellow letters: {}'.format(self.yellow_letters))
        print('Grey squares: {}'.format(self.grey_squares))
        print('Existing information: {}'.format(existing_information))
        frequencies = self.calc_information_gain_approx_per_word_from_orig_dict() if existing_information < 3 or (word_dict_len > 6) else self.calc_information_gain_approx_per_word_from_current_dict()
        if frequencies:
            print('Chosen word: {}, aggregate frequency: {}'.format(frequencies[0][0], frequencies[0][1]))
            return frequencies[0][0]

        random_word = self.guess_random_from_current_dict()
        print('Chosen word: {} at random'.format(random_word))
        return random_word

    def update_after_turn(self, turn):
        all_occurrences = self.count_all_occurrences(turn.guess)
        green_yellow_occurrences = self.count_green_yellow_occurrences(turn.pattern)
        for i, (p, c) in enumerate(turn.pattern.pattern):
            if p == SQUARE.GREEN:
                self.words_dictionary.remaining_puzzle_words = [word for word in self.words_dictionary.remaining_puzzle_words if word[i] == c]
                self.green_squares.add((i, c))
                self.green_letters.add(c)
            elif p == SQUARE.YELLOW:
                self.words_dictionary.remaining_puzzle_words = [word for word in self.words_dictionary.remaining_puzzle_words if word[i] != c and word.count(c) >= green_yellow_occurrences[c]]
                self.yellow_letters.add(c)
            elif p == SQUARE.GREY:
                self.words_dictionary.remaining_puzzle_words = [word for word in self.words_dictionary.remaining_puzzle_words if word[i] != c and word.count(c) < all_occurrences[c]]
                self.grey_squares.add((i, c))
                self.grey_letters.add(c)

        print('New dictionary size is: {}'.format(len(self.words_dictionary.remaining_puzzle_words)))
        self.update_grey_letters()

    def update_grey_letters(self):
        remaining_letters = set()
        for word in self.words_dictionary.remaining_puzzle_words:
            remaining_letters = set.union(remaining_letters, set(word))
        self.grey_letters = set.union(self.grey_letters, set(string.ascii_uppercase) - remaining_letters)
        print('Remaining letters: {}'.format(remaining_letters))

    def find_letter_frequency_in_current_dict(self):
        frequencies = defaultdict(int)
        for word in self.words_dictionary.remaining_puzzle_words:
            for c in set([c for c in word]):
                frequencies[c] += 1

        return frequencies

    def sum_word_information_gain_approx(self, word, letter_frequencies, total_word_count):
        information_gain_sum = 0
        letter_count_in_curr_word = defaultdict(int)
        for i, c in enumerate(word):
            if (i, c) not in self.green_squares and c not in self.grey_letters:
                if letter_count_in_curr_word[c] == 0 or (letter_count_in_curr_word[c] > 0 and (i, c) not in self.grey_squares):
                    yellow_penalty = 0.2 if c in self.yellow_letters or c in self.green_letters else 1
                    grey_penalty = 0.2**letter_count_in_curr_word[c]
                    information_gain_sum += grey_penalty*yellow_penalty*(1.0-abs(0.5-(float(letter_frequencies[c])/total_word_count)))
                    letter_count_in_curr_word[c] += 1

        return information_gain_sum

    def calc_information_gain_approx_per_word(self, word_dict):
        letter_frequencies = self.find_letter_frequency_in_current_dict()
        word_information_gain = [(word, self.sum_word_information_gain_approx(word, letter_frequencies, len(self.words_dictionary.remaining_puzzle_words))) for word in word_dict]
        return sorted(word_information_gain, key=lambda x: x[1], reverse=True)

    def calc_information_gain_approx_per_word_from_current_dict(self):
        return self.calc_information_gain_approx_per_word(self.words_dictionary.remaining_puzzle_words)

    def calc_information_gain_approx_per_word_from_orig_dict(self):
        return self.calc_information_gain_approx_per_word(self.words_dictionary.valid_words)

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
        word_frequencies = [(word, self.sum_word_frequencies(word, letter_frequencies)) for word in self.words_dictionary.remaining_puzzle_words]
        return sorted(word_frequencies, key=lambda x: x[1], reverse=True)
