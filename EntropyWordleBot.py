import math
from collections import defaultdict

from LoggerFactory import LoggerFactory
from WordleBotInterface import WordleBotInterface
from GuessPattern import SQUARE, GuessPattern

logger = LoggerFactory.get_logger()


class EntropyWordleBot(WordleBotInterface):

    def __init__(self, game, puzzle_words, valid_words) -> None:
        super().__init__(game, puzzle_words, valid_words)

    def choose_optimal_word(self):
        if len(self.words_dictionary.remaining_puzzle_words) > 2:
            frequencies = self.calc_information_gain_by_entropy_for_all_words()
            logger.debug('Chosen word: {}, aggregate frequency: {}'.format(frequencies[0][0], frequencies[0][1]))
            return frequencies[0][0]

        random_word = self.guess_random_from_current_dict()
        logger.debug('Chosen word: {} at random'.format(random_word))
        return random_word

    def update_after_turn(self, turn):
        all_occurrences = self.count_all_occurrences(turn.guess)
        green_yellow_occurrences = self.count_green_yellow_occurrences(turn.pattern)
        self.words_dictionary.remaining_puzzle_words = self.update_dict_after_turn(
            turn,
            self.words_dictionary.remaining_puzzle_words,
            all_occurrences,
            green_yellow_occurrences)

        if self.game.hard_mode:
            self.words_dictionary.valid_words = self.update_dict_after_turn(
                turn,
                self.words_dictionary.valid_words,
                all_occurrences,
                green_yellow_occurrences)

    @staticmethod
    def update_dict_after_turn(turn, word_dict, all_occurrences, green_yellow_occurrences):
        for i, (p, c) in enumerate(turn.pattern.pattern):
            if p == SQUARE.GREEN:
                word_dict = [word for word in word_dict if word[i] == c]
            elif p == SQUARE.YELLOW:
                word_dict = [word for word in word_dict if word[i] != c and word.count(c) >= green_yellow_occurrences[c]]
            elif p == SQUARE.GREY:
                word_dict = [word for word in word_dict if word[i] != c and word.count(c) < all_occurrences[c]]

        logger.debug('New dictionary size is: {}'.format(len(word_dict)))

        return word_dict

    def calc_information_gain_by_entropy(self, word):
        dict_len = len(self.words_dictionary.remaining_puzzle_words)
        pattern_dict = defaultdict(int)
        for secret in self.words_dictionary.remaining_puzzle_words:
            pattern = GuessPattern(secret, word).print_pattern()
            pattern_dict[pattern] += 1.0/dict_len

        information_gain = -1 * sum([val * math.log(val) for val in pattern_dict.values()])
        return information_gain

    def calc_information_gain_by_entropy_for_all_words(self):
        gains = [(word, self.calc_information_gain_by_entropy(word)) for word in self.words_dictionary.valid_words]
        return sorted(gains, key=lambda x: x[1], reverse=True)
