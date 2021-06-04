from string import ascii_lowercase, ascii_uppercase
from dataclasses import dataclass

@dataclass
class Alphabet:
    letters: str

    @property
    def size(self):
        return len(self.letters)

    @property
    def index(self):
        return self.letters.index

class Vigenere:
    def __init__(self, plaintext):
        self.text = plaintext
        self.init_alphabets()

    def init_alphabets(self):
        self.alphabets = [
            Alphabet(self.__russian_alphabet()),
            Alphabet(self.__russian_alphabet(uppercase=True)),
            Alphabet(ascii_lowercase),
            Alphabet(ascii_uppercase),
        ]

    def encrypt(self, key):
        self.text = self.__str_multi_shift(key)
        return self.text

    def decrypt(self, key):
        self.text = self.__str_multi_shift(key, decrypt=True)
        return self.text

    def __str_multi_shift(self, keystr, decrypt=False):
        text_size = len(self.text)
        key_wrapped = iter((keystr * (text_size // len(keystr) + 1))[:text_size])
        return ''.join(map(lambda x: self._chr_shift(x, key_wrapped, decrypt), self.text))

    def _chr_shift(self, char, key_wrapped, decrypt=False):
        alphabet = self.__find_alphabet(char)
        if alphabet is None:
            return char

        key = next(key_wrapped)
        if not key in alphabet.letters:
            temp_key = key.lower() if key.isupper() else key.upper()
            temp = self.__find_alphabet(temp_key)
            if temp is None:
                print(f'Текст и ключ используют символы разного алфавита: {char}')
                return char
            key = temp_key

        shift = alphabet.index(key)
        if decrypt == True:
            shift = alphabet.size - shift
        return self.__chr_shift(alphabet, char, shift)

    def __find_alphabet(self, char):
        return next((x for x in self.alphabets if char in x.letters), None)

    @staticmethod
    def __chr_shift(alphabet, char, shift):
        shift %= alphabet.size
        shifted = alphabet.letters[shift:] + alphabet.letters[:shift]
        transition = char.maketrans(alphabet.letters, shifted)
        return char.translate(transition)

    @staticmethod
    def __russian_alphabet(uppercase=False):
        letters = list(map(chr, range(ord('а'), ord('я') + 1)))
        letters.insert(letters.index('е') + 1, 'ё')
        ret = ''.join(letters)
        return ret if not uppercase else ret.upper()

def encrypt_message(key, message):
    vigenere = Vigenere(message)
    return vigenere.encrypt(key)

def decrypt_message(key, message):
    vigenere = Vigenere(message)
    return vigenere.decrypt(key)