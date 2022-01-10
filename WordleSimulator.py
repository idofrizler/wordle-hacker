import copy
from itertools import repeat

from DictionaryFetcher import DictionaryFetcher
from EntropyWordleBot import EntropyWordleBot
from LoggerFactory import LoggerFactory
from multiprocessing import Pool
# from multiprocessing.pool import ThreadPool as Pool

from WordleGame import WordleGame

POOL_SIZE = 10
logger = LoggerFactory.get_logger()


def play_wordle(word, puzzle_words, valid_words):
    game = WordleGame(word)
    bot = EntropyWordleBot(game, puzzle_words, valid_words)
    bot.play_game()

    if game.is_successful():
        logger.info('Guessed correctly the word "{}" in {} turns'.format(game.last_guess().guess, game.turns_played()))
    else:
        logger.info('Game over. Correct word is "{}"'.format(word))

    if game.is_successful():
        return (word, 1, game.turns_played())
    return (word, 0, 0)


def pack_global_params(dictionary_fetcher):
    puzzle_words = copy.deepcopy(dictionary_fetcher.puzzle_words)
    valid_words = copy.deepcopy(dictionary_fetcher.valid_words)
    input_words = puzzle_words  # ['GRAZE']

    return zip(input_words, repeat(puzzle_words), repeat(valid_words))


def play_all_words():
    p = Pool(POOL_SIZE)

    dictionary_fetcher = DictionaryFetcher()
    global_params = pack_global_params(dictionary_fetcher)
    pool_output = p.starmap(play_wordle, global_params)

    successful_games = sum([output[1] for output in pool_output])
    total_turns_in_successful_games = sum([output[2] for output in pool_output])
    failed_words = [output[0] for output in pool_output if not output[1]]
    logger.info('Total games: {}\n{}Successful games: {}\n{}Average turns when successful: {}'.format(
        len(dictionary_fetcher.puzzle_words), ' '*26, successful_games, ' '*26,
        float(total_turns_in_successful_games) / successful_games))
    logger.info('Failed words: {}'.format(failed_words))


if __name__ == '__main__':
    play_all_words()
