from WordleTurn import WordleTurn, GuessPattern

TOTAL_GUESSES = 6


class WordleGame:

    def __init__(self, word) -> None:
        self.secret_word = word
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
        return self.last_guess() is not None and self.last_guess().guess == self.secret_word

    def is_over(self):
        return self.guesses_left() <= 0 or self.is_successful()

    def play_turn(self, guess):
        assert not self.is_over()

        guess_pattern = GuessPattern(self.secret_word, guess)
        print('Guess is:   {}\nPattern is: {}'.format(guess, guess_pattern.print_pattern()))

        turn = WordleTurn(guess, guess_pattern)
        self.turns.append(turn)

        return turn
