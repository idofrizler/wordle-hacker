from WordleBot import WordleBot
from WordleDictionary import WordleDictionary
from multiprocessing import Pool

from WordleGame import WordleGame

POOL_SIZE = 20


def play_wordle(word):
    game = WordleGame(word)
    wordle_bot = WordleBot(game)
    wordle_bot.play_game()

    if game.is_successful():
        print('Guessed correctly the word "{}" in {} turns'.format(game.last_guess().guess, game.turns_played()))
    else:
        print('Game over. Correct word is "{}"'.format(word))

    if game.is_successful():
        return (word, 1, game.turns_played())
    return (word, 0, 0)


def play_all_words():
    input_words = WordleDictionary()

    p = Pool(POOL_SIZE)
    pool_output = p.map(play_wordle, input_words.words)

    successful_games = sum([output[1] for output in pool_output])
    total_turns_in_successful_games = sum([output[2] for output in pool_output])
    failed_words = [output[0] for output in pool_output if not output[1]]
    print('Total games: {}\nSuccessful games: {}\nAverage turns when successful: {}'.format(len(input_words.words), successful_games, float(total_turns_in_successful_games)/successful_games))
    print('Failed words: {}'.format(failed_words))


if __name__ == '__main__':
    play_all_words()
    # play_wordle('CASES')
