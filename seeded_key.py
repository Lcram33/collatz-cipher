from params import UNUSED_CHARS, DEFAULT_CHARSET
from secure_pwd_gen_api import new_passphrase, load_wordlist
from collatzcipher import format_key
import random
import hashlib

def print_fewer_lines(str_input):
    lines = str_input.split('\n')
    if len(lines) > 7:
        splitted = lines[:3] + [f"[skipped {len(lines)-6} lines]"] + lines[-3:]
        print('\n'.join(splitted))
    else:
        print(str_input)

def sha256_string(my_string):
    return hashlib.sha256(my_string.encode('utf-8')).hexdigest()

def pseudo_random_shuffle(str_input: str):
    l = len(str_input)
    str_input = list(str_input)
    str_output = ""

    for i in range(l):
        ind = random.randint(0,len(str_input)-1)
        str_output += str_input[ind]
        del str_input[ind]

    return str_output

def pseudo_randomly_split(str_input):
    shuffled = pseudo_random_shuffle(str_input)
    s = random.randint(0,len(shuffled)-1)

    return shuffled[:s], shuffled[-1], shuffled[s:len(shuffled)-1]

def pseudo_random_make_charset_and_null_chars(charset, unused_chars):
    to_add_to_charset, split_char, null_chars = pseudo_randomly_split(unused_chars)
    charset += to_add_to_charset

    return pseudo_random_shuffle(charset), split_char, null_chars

def gen_key_with_seed(nbytes = 500):
    charset, split_char, null_chars = pseudo_random_make_charset_and_null_chars(DEFAULT_CHARSET, UNUSED_CHARS)
    key_obj = {
        'charset': charset,
        'key': hex(random.randint(int('1'+(2*nbytes-1)*'0',16), int(2*nbytes*'f',16)))[2:],
        'split_char': split_char,
        'null_chars': null_chars
    }

    return key_obj


def print_passphrase_and_generate(nbytes, seedphrase):
    wordlist = load_wordlist('wordlist.json')

    number_of_words = 12
    sep = ' '
    phrase_seed = seedphrase if seedphrase != '' else new_passphrase(wordlist, number_of_words, sep)

    if seedphrase == '':
        print("Your seed phrase is the following, please DO take note of it, DON'T share it with anyone unless you want them to have your key :")
        print(phrase_seed)

    random.seed(phrase_seed)
    key = gen_key_with_seed(nbytes)
    str_key = format_key(key)
    print("Here is the fingerprint (sha256) of you key : " + sha256_string(str_key))

    return str_key

def test_seeded_key():
    wordlist = load_wordlist('wordlist.json')

    number_of_words = 12
    sep = ' '
    phrase_seed = "atonable decent visiting daringly backyard aloft backrest connected reseller gratitude detail direness" #for testing, uncomment next line to generate one
    #phrase_seed = new_passphrase(wordlist, number_of_words, sep)

    print("Your seed phrase is the following, please DO take note of it, DON'T share it with anyone unless you want them to have your key :")
    print(phrase_seed)

    random.seed(phrase_seed)

    key = gen_key_with_seed()
    str_key = format_key(key)
    print_fewer_lines(str_key)

    print("Here is the fingerprint (sha256) of you key : " + sha256_string(str_key)) #with the example provided, should be 9a316fa17e8b8734fe9c27cf2031fde784e6fad9e837270761ae4b505a75bff8