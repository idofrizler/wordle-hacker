from abc import ABC, abstractmethod

from LoggerFactory import LoggerFactory
from GuessPattern import GuessPattern

TOTAL_GUESSES = 6
logger = LoggerFactory.get_logger()


class WordleGameInterface(ABC):

    def __init__(self) -> None:
        self.turns = []

    def last_guess(self):
        if len(self.turns) == 0:
            return None
        return self.turns[-1]

    def turns_played(self):
        return len(self.turns)

    def guesses_left(self):
        return TOTAL_GUESSES - self.turns_played()

    def is_successful(self):
        return self.last_guess() is not None and self.last_guess().pattern.print_pattern() == GuessPattern.ALL_GREENS  # self.last_guess().guess == self.secret_word

    def is_over(self):
        return self.guesses_left() <= 0 or self.is_successful()

    def play_turn(self, guess):
        assert not self.is_over()

        logger.info('Playing turn #{}'.format(len(self.turns)+1))
        logger.info('Guess is:   {}'.format(guess))
        guess_pattern = self.get_pattern_for_guess(guess)
        logger.info('Pattern is: {}'.format(guess_pattern.print_pattern()))

        turn = WordleTurn(guess, guess_pattern)
        self.turns.append(turn)

        return turn

    @abstractmethod
    def get_pattern_for_guess(self, guess):
        pass


class BenchmarkWordleGame(WordleGameInterface):
    def __init__(self, word) -> None:
        super().__init__()
        self.secret_word = word

    def get_pattern_for_guess(self, guess):
        return GuessPattern(self.secret_word, guess)


class InteractiveWordleGame(WordleGameInterface):
    def __init__(self) -> None:
        super().__init__()

    def get_pattern_for_guess(self, guess):
        stdin_pattern = input('Enter received pattern (V-Green, ?-Yellow, X-Grey): ')
        while not GuessPattern.validate_pattern(stdin_pattern):
            logger.error('Incorrect pattern. Use only five \'VX?\' characters.')
            stdin_pattern = input('Enter received pattern (V-Green, ?-Yellow, X-Grey): ')

        return GuessPattern(stdin_pattern, guess, init_from_str=True)


class WordleTurn:
    def __init__(self, guess, pattern) -> None:
        self.guess = guess
        self.pattern = pattern
