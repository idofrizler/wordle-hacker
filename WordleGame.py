from WordleBot import WordleBot
from WordleDictionary import WordleDictionary
from WordleTurn import WordleTurn, GuessPattern
from multiprocessing import Pool

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

    def play_turn(self, wordle_bot):
        assert not self.is_over()

        guess = wordle_bot.make_guess()
        guess_pattern = GuessPattern(self.secret_word, guess)
        print('Guess is:   {}\nPattern is: {}'.format(guess, guess_pattern.print_pattern()))

        turn = WordleTurn(guess, guess_pattern)
        self.turns.append(turn)
        wordle_bot.update_dictionary_after_turn(turn)


def play_wordle(word):
    game = WordleGame(word)
    wordle_bot = WordleBot()
    while not game.is_over():
        game.play_turn(wordle_bot)

    if game.is_successful():
        print('Guessed correctly the word "{}" in {} turns'.format(game.last_guess().guess, game.turns_played()))
    else:
        print('Game over. Correct word is "{}"'.format(word))

    if game.is_successful():
        return (word, 1, game.turns_played())
    return (word, 0, 0)


def play_all_words():
    input_words = WordleDictionary()

    p = Pool(10)
    pool_output = p.map(play_wordle, input_words.words)

    successful_games = sum([output[1] for output in pool_output])
    total_turns_in_successful_games = sum([output[2] for output in pool_output])
    failed_words = [output[0] for output in pool_output if not output[1]]
    print('Total games: {}\nSuccessful games: {}\nAverage turns when successful: {}'.format(len(input_words.words), successful_games, float(total_turns_in_successful_games)/successful_games))
    print('Failed words: {}'.format(failed_words))


if __name__ == '__main__':
    # play_all_words()
    play_wordle('HOUND')
