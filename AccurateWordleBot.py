import math
from collections import defaultdict

from WordleBotInterface import WordleBotInterface
from WordleTurn import SQUARE, GuessPattern


class AccurateWordleBot(WordleBotInterface):
    def __init__(self, game) -> None:
        super().__init__(game)

    def choose_optimal_word(self):
        if len(self.words_dictionary.words) > 2:
            frequencies = self.calc_information_gain_by_entropy_for_all_words()
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
                self.words_dictionary.words = [word for word in self.words_dictionary.words if word[i] == c]
            elif p == SQUARE.YELLOW:
                self.words_dictionary.words = [word for word in self.words_dictionary.words if word[i] != c and word.count(c) >= green_yellow_occurrences[c]]
            elif p == SQUARE.MISS:
                self.words_dictionary.words = [word for word in self.words_dictionary.words if word[i] != c and word.count(c) < all_occurrences[c]]

        print('New dictionary size is: {}'.format(len(self.words_dictionary.words)))

    def calc_information_gain_by_entropy(self, word):
        dict_len = len(self.words_dictionary.words)
        pattern_dict = defaultdict(int)
        for secret in self.words_dictionary.words:
            pattern = GuessPattern(secret, word).print_pattern()
            pattern_dict[pattern] += 1.0/dict_len

        information_gain = -1 * sum([val * math.log(val) for val in pattern_dict.values()])
        return information_gain

    def calc_information_gain_by_entropy_for_all_words(self):
        gains = [(word, self.calc_information_gain_by_entropy(word)) for word in self.words_dictionary.words_orig]
        return sorted(gains, key=lambda x: x[1], reverse=True)

    # Dynamic programming: pre-calculate pattern between any (secret, guess) tuples
    # def create_pattern_cache(self):
    #     for secret in self.words_dictionary.words_orig:
    #         for guess in self.words_dictionary.words_orig:
    #             pattern = GuessPattern(secret, guess).print_pattern()
