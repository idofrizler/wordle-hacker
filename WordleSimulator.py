import argparse
import copy
from itertools import repeat

from DictionaryFetcher import DictionaryFetcher
from EntropyWordleBot import EntropyWordleBot
from LoggerFactory import LoggerFactory
from multiprocessing import Pool
# from multiprocessing.pool import ThreadPool as Pool

from WordleGame import BenchmarkWordleGame, InteractiveWordleGame

POOL_SIZE = 30
logger = LoggerFactory.get_logger()


def play_wordle(word, puzzle_words, valid_words, hard_mode):
    game = BenchmarkWordleGame(word, hard_mode)
    bot = EntropyWordleBot(game, puzzle_words, valid_words)
    bot.play_game()

    if game.is_successful():
        logger.info('Guessed correctly the word "{}" in {} turns'.format(game.last_guess().guess, game.turns_played()))
    else:
        logger.info('Game over. Correct word is "{}"'.format(word))

    if game.is_successful():
        return (word, 1, game.turns_played())
    return (word, 0, 0)


def pack_global_params(dictionary_fetcher, hard_mode):
    puzzle_words = copy.deepcopy(dictionary_fetcher.puzzle_words)
    valid_words = copy.deepcopy(dictionary_fetcher.valid_words)
    input_words = puzzle_words  # ['GRAZE']

    return zip(input_words, repeat(puzzle_words), repeat(valid_words), repeat(hard_mode))


def benchmark_all_words(hard_mode):
    p = Pool(POOL_SIZE)

    dictionary_fetcher = DictionaryFetcher()
    global_params = pack_global_params(dictionary_fetcher, hard_mode)
    pool_output = p.starmap(play_wordle, global_params)

    successful_games = sum([output[1] for output in pool_output])
    total_turns_in_successful_games = sum([output[2] for output in pool_output])
    failed_words = [output[0] for output in pool_output if not output[1]]
    logger.info('Total games: {}\n{}Successful games: {}\n{}Average turns when successful: {}'.format(
        len(dictionary_fetcher.puzzle_words), ' '*26, successful_games, ' '*26,
        float(total_turns_in_successful_games) / successful_games))
    logger.info('Failed words: {}'.format(failed_words))


parser = argparse.ArgumentParser(description='Choose a flow to be run')
parser.add_argument('--interactive', action='store_true', help='interactively play a Wordle game with the bot')
parser.add_argument('--hard_mode', action='store_true', help='activate "Hard Mode"')
parser.add_argument('--benchmark', action='store_true', help='benchmark the bot on all words in dictionary')


def play_word_with_bot(hard_mode):
    dictionary_fetcher = DictionaryFetcher()
    game = InteractiveWordleGame(hard_mode)
    bot = EntropyWordleBot(game, dictionary_fetcher.puzzle_words, dictionary_fetcher.valid_words)
    bot.play_game()
    if game.is_successful():
        logger.info('Guessed correctly the word "{}" in {} turns'.format(game.last_guess().guess, game.turns_played()))
    else:
        logger.info('Game over.')


if __name__ == '__main__':
    args = parser.parse_args()
    if args.interactive:
        play_word_with_bot(args.hard_mode)
    if args.benchmark:
        benchmark_all_words(args.hard_mode)
