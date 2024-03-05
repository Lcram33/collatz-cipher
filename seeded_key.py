from params import UNUSED_CHARS, DEFAULT_CHARSET
from collatzcipher import format_key
from hashing import *

import base64
import random


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
    charset += split_char

    return pseudo_random_shuffle(charset), split_char, null_chars

def gen_key_with_seed(nbytes):
    charset, split_char, null_chars = pseudo_random_make_charset_and_null_chars(DEFAULT_CHARSET, UNUSED_CHARS)
    key_obj = {
        'charset': charset,
        'key': hex(random.randint(int('1'+(2*nbytes-1)*'0',16), int(2*nbytes*'f',16)))[2:],
        'split_char': split_char,
        'null_chars': null_chars
    }

    return key_obj


def generate_seeded_key(password, salt = '', nbytes = 500, legacy = False):
    if salt == '':
        salt = gen_salt()
    
    if legacy:
        secured_seed = hash_password_legacy(password, salt)
    else:
        secured_seed = hash_password(password, salt)

    random.seed(secured_seed)

    key = gen_key_with_seed(nbytes)
    
    key_fingerprint = hash_fingerprint(format_key(key))

    return {
        "key": key,
        "salt": salt,
        "fingerprint": key_fingerprint
    }

def generate_seedphrase_key(seedphrase, nbytes = 500):
    assert len(seedphrase) > 10, "Seedphrase is too short. Create a stronger one !"

    salt, password = seedphrase[:5], seedphrase[5:]

    return generate_seeded_key(password, salt, nbytes, legacy=True)