from string import ascii_uppercase
from functools import reduce
from itertools import product
from collections import Counter
from re import compile as re_compile

import vigenere_cipher
import freq_analysis
import detect_english

INPUT_FILE = 'plaintext.txt'
OUTPUT_FILE = 'hacked_message.txt'

NUM_MOST_FREQ_LETTERS = 4
MAX_KEY_LENGTH = 16
NONLETTERS_PATTERN = re_compile('[^A-Z]')

def repeating_sequences(message):
    message = NONLETTERS_PATTERN.sub('', message.upper())
    ret = {}
    for length in range(3, 6):
        for start in range(len(message) - length):
            seq = message[start : start + length]
            for i in range(start + length, len(message) - length):
                if message[i : i + length] == seq:
                    if seq not in ret:
                        ret[seq] = []
                    ret[seq].append(i - start)
    return ret

def factors(num):
    return set(reduce(list.__add__, ([i, num // i] for i in range(1, int(num ** 0.5) + 1) if num % i == 0)))

def most_common_factors(seq_factors):
    factors = [item for sublist in seq_factors.values() for item in sublist]
    factor_counts = dict(Counter(filter(lambda x: x <= MAX_KEY_LENGTH, factors)))
    return sorted([(k, v) for k, v in factor_counts.items()], key=lambda x: x[1], reverse=True)

def examine_key_lengths(ciphertext):
    seq_spacings = repeating_sequences(ciphertext)
    seq_factors = {k: [item for sublist in [list(factors(f)) for f in v] for item in sublist] for k, v in seq_spacings.items()}
    factors_by_count = most_common_factors(seq_factors)
    return (x[0] for x in factors_by_count)

def every_nth_letter(nth, length, message):
    return NONLETTERS_PATTERN.sub('', message.upper())[nth - 1 :: length]

def hack_with_length(ciphertext, length):
    ciphertext = ciphertext.upper()
    all_freq_scores = []

    for nth in range(1, length + 1):
        nth_letters = every_nth_letter(nth, length, ciphertext)
        freq_scores = []

        for possible_key in ascii_uppercase:
            decrypted_text = vigenere_cipher.decrypt_message(possible_key, nth_letters)
            key_freq_match = (possible_key, freq_analysis.english_freq_match_score(decrypted_text))
            freq_scores.append(key_freq_match)

        freq_scores.sort(key=lambda x: x[1], reverse=True)
        all_freq_scores.append(freq_scores[:NUM_MOST_FREQ_LETTERS])

    for indexes in product(range(NUM_MOST_FREQ_LETTERS), repeat=length):
        possible_key = reduce(lambda acc, x: acc + all_freq_scores[x][indexes[x]][0], range(length), '')
        decrypted_text = vigenere_cipher.decrypt_message(possible_key, ciphertext)
        if not detect_english.is_english(decrypted_text):
            continue

        print(f'Возможный ключ: {possible_key}\n')
        print(f'{decrypted_text[:200]}\n')
        print('Нажмите Enter, чтобы продолжить взлом, или Q, чтобы завершить работу:')

        if input('$ ').strip().upper().startswith('Q'):
            return decrypted_text
    return None

def hack_vigenere(ciphertext):
    key_lengths = examine_key_lengths(ciphertext)
    for length in key_lengths:
        print(f'Попытка взлома с ключом длиной {length} ({NUM_MOST_FREQ_LETTERS ** length} возм. комб.)...')
        if (hacked_message := hack_with_length(ciphertext, length)) is not None:
            return hacked_message

    print('Не удалось подобрать правильный ключ. Начинается брут-форс...')
    for length in range(1, MAX_KEY_LENGTH + 1):
        if length not in key_lengths:
            print(f'Попытка взлома с ключом длиной {length} ({NUM_MOST_FREQ_LETTERS ** length} возм. комб.)...')
            if (hacked_message := hack_with_length(ciphertext, length)) is not None:
                return hacked_message
    return None

with open(INPUT_FILE, encoding='utf-8') as f:
    ciphertext = f.read()

hacked_message = hack_vigenere(ciphertext)
if hacked_message is None:
    print('Не удалось взломать сообщение!')
    exit()

print(f'Запись взломанного сообщения в файл {OUTPUT_FILE}...')
with open(OUTPUT_FILE, 'w', encoding='utf-8') as f:
    f.write(hacked_message)
print('Успешно!')
exit()