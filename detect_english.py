from string import ascii_letters
from functools import reduce

DICTIONARY_FILE = 'dictionary.txt'

def load_dictionary():
    words = {}
    with open(DICTIONARY_FILE) as dictionaryFile:
        for word in dictionaryFile.read().splitlines():
            words[word] = None
    return words

ENGLISH_WORDS = load_dictionary()

def remove_non_letters(message):
    letters = filter(lambda x: x in ascii_letters + ' \t\n', message)
    return ''.join(letters)

def english_count(message):
    possible_words = remove_non_letters(message.upper()).split()
    words_count = len(possible_words)

    if words_count == 0:
        return 0.0

    matches = reduce(lambda acc, x: acc + 1 if x in ENGLISH_WORDS else acc, possible_words, 0)
    return matches / words_count

def is_english(message, word_percentage=20, letter_percentage=85):
    enough_words = english_count(message) * 100 >= word_percentage
    num_letters = len(remove_non_letters(message))
    enough_letters = num_letters / len(message) * 100 >= letter_percentage
    return enough_words and enough_letters