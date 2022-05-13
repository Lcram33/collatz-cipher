from params_default import UNUSED_CHARS, DEFAULT_CHARSET
from secure_pwd_gen_api import new_passphrase, load_wordlist
from collatzcipher import format_key
import random


def shuffle(str_input: str):
    l = len(str_input)
    str_input = list(str_input)
    str_output = ""

    for i in range(l):
        ind = random.randint(0,len(str_input)-1)
        str_output += str_input[ind]
        del str_input[ind]

    return str_output

def randomly_split(str_input):
    shuffled = shuffle(str_input)
    s = random.randint(0,len(shuffled)-1)

    return shuffled[:s], shuffled[s:]

def make_charset_and_null_chars(charset, unused_chars):
    to_add_to_charset, null_chars = randomly_split(unused_chars)
    charset += to_add_to_charset

    return shuffle(charset), null_chars

def gen_key_with_seed(phrase_seed, nbytes = 800):
    random.seed(phrase_seed)

    charset, null_chars = make_charset_and_null_chars(DEFAULT_CHARSET, UNUSED_CHARS)
    key_obj = {
        'charset': charset,
        'key': hex(random.randint(int('1'+(2*nbytes-1)*'0',16), int(2*nbytes*'f',16)))[2:],
        'null_chars': null_chars
    }

    return key_obj


wordlist = load_wordlist('wordlist.json')
phrase_seed = new_passphrase(wordlist, 12, ' ')

print("Your seed phrase is the following, please DO take note of it, DON'T share it with anyone unless you want them to have your key :")
print(phrase_seed)

key = gen_key_with_seed(phrase_seed)
str_key = format_key(key)
print(str_key)