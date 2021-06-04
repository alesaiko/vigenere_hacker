from string import ascii_uppercase

LETTER_FREQ = {'E': 12.70, 'T': 9.06, 'A': 8.17, 'O': 7.51, 'I': 6.97, 'N': 6.75, 'S': 6.33, 'H': 6.09, 'R': 5.99, 'D': 4.25, 'L': 4.03, 'C': 2.78,
               'U': 2.76, 'M': 2.41, 'W': 2.36, 'F': 2.23, 'G': 2.02, 'Y': 1.97, 'P': 1.93, 'B': 1.29, 'V': 0.98, 'K': 0.77, 'J': 0.15, 'X': 0.15, 'Q': 0.10, 'Z': 0.07}
ETAOIN = 'ETAOINSHRDLCUMWFGYPBVKJXQZ'

def letters_count(message):
    return {k: message.upper().count(k) for k, _ in dict.fromkeys(ascii_uppercase, 0).items()}

def frequency_order(message):
    letters_freq = letters_count(message)
    freq_letters = {}

    for letter in ascii_uppercase:
        if (key := letters_freq[letter]) not in freq_letters:
            freq_letters[key] = []
        freq_letters[key].append(letter)

    for k, v in freq_letters.items():
        freq_letters[k].sort(key=ETAOIN.find, reverse=True)
        freq_letters[k] = ''.join(v)

    freq_pairs = list(freq_letters.items())
    freq_pairs.sort(key=lambda x: x[0], reverse=True)

    freq_order = map(lambda x: x[1], freq_pairs)
    return ''.join(freq_order)

def english_freq_match_score(message):
    freq_order = frequency_order(message)
    match_score = 0

    for common_letter in ETAOIN[:6]:
        if common_letter in freq_order[:6]:
            match_score += 1

    for uncommon_letter in ETAOIN[-6:]:
        if uncommon_letter in freq_order[-6:]:
            match_score += 1

    return match_score