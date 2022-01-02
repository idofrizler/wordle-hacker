import re
from collections import defaultdict

import requests

ENGLISH_DICTIONARY_URL = 'https://raw.githubusercontent.com/dwyl/english-words/master/words.txt'


def read_english_dictionary():
    resp = requests.get(ENGLISH_DICTIONARY_URL)
    words = resp.text.splitlines()

    r = re.compile("^([a-z]|[A-Z]){5}$")
    five_letter_words = list(filter(r.match, words))
    lowered_five_letter_words = [word.lower() for word in five_letter_words]

    return lowered_five_letter_words


def find_most_common_letters_no_repetitions(words_list):
    dict = defaultdict(int)
    for word in words_list:
        for c in set([c for c in word]):
            dict[c] += 1

    most_common = sorted(dict.items(), key=lambda item: item[1])
    return most_common[-5:]


def find_most_common_letters(words_list):
    dict = defaultdict(int)
    for word in words_list:
        for i in range(0, 5):
            dict[word[i]] += 1

    most_common = sorted(dict.items(), key=lambda item: item[1])
    return most_common[-5:]


def create_five_letter_set_mapping(five_letter_words):
    dict = defaultdict(list)
    for word in five_letter_words:
        word_set = ''.join(sorted(set([c for c in word])))
        dict[word_set].append(word)

    return dict


def find_best_mapping(five_letter_set_mapping, most_common_letters):
    most_common_letters_keys = [t[0] for t in most_common_letters]
    word_set = ''.join(sorted(set([c for c in most_common_letters_keys])))

    match = five_letter_set_mapping.get(word_set, [])
    return match


def main():
    five_letter_words = read_english_dictionary()
    print('Found {} letters'.format(len(five_letter_words)))

    most_common_letters = find_most_common_letters_no_repetitions(five_letter_words)
    print('Most common letters: {}'.format(most_common_letters))

    five_letter_set_mapping = create_five_letter_set_mapping(five_letter_words)
    best_mapping = find_best_mapping(five_letter_set_mapping, most_common_letters)
    print('Best mapping is: {}'.format(best_mapping))


if __name__ == "__main__":
    main()
