from params import UNUSED_CHARS, DEFAULT_CHARSET
from secure_pwd_gen_api import new_password
from collatzcipher import format_key
import random
import hashlib


HASHING_ITERATIONS = 512000


def sha256_string(my_string):
    return hashlib.sha256(my_string.encode('utf-8')).hexdigest()

def sha512_string(my_string):
    return hashlib.sha512(my_string.encode('utf-8')).hexdigest()

def hash_password(my_string): # using general function so that it can be easly changed when the algorithm becomes obsolote
    return sha512_string(my_string)

def hash_fingerprint(my_string):
    return sha256_string(my_string)


def gen_salt():
    return new_password(32, DEFAULT_CHARSET) # 256 bits salt

def hash_and_salt(password, salt):
    # salting and mixing
    if len(password) > 4:
        password = password[0] + salt[0] + password[1:3] + salt[1] + password[3:] + salt[2:]
    else:
        password += salt

    hashed = hash_password(password)
    
    # avoiding bruteforce
    for i in range(HASHING_ITERATIONS):
        hashed = hash_password(f"{hashed}{i}")

    return hashed

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

def gen_key_with_seed(nbytes):
    charset, split_char, null_chars = pseudo_random_make_charset_and_null_chars(DEFAULT_CHARSET, UNUSED_CHARS)
    key_obj = {
        'charset': charset,
        'key': hex(random.randint(int('1'+(2*nbytes-1)*'0',16), int(2*nbytes*'f',16)))[2:],
        'split_char': split_char,
        'null_chars': null_chars
    }

    return key_obj


def generate_seeded_key(password, salt = '', nbytes = 500):
    if salt == '':
        salt = gen_salt()
        
    secured_seed = hash_and_salt(password, salt)

    random.seed(secured_seed)

    key = gen_key_with_seed(nbytes)
    
    key_fingerprint = hash_fingerprint(format_key(key))

    return {
        "key": key,
        "salt": salt,
        "fingerprint": key_fingerprint
    }

def regen_key_with_seed(password, salt, nbytes, fingerprint):
    secured_seed = hash_and_salt(password, salt)

    random.seed(secured_seed)

    key = gen_key_with_seed(nbytes)
    
    gen_fingerprint = hash_fingerprint(format_key(key))

    return gen_key_with_seed(nbytes) if gen_fingerprint == fingerprint else False

def generate_seedphrase_key(seedphrase, nbytes = 500):
    assert len(seedphrase) > 10, "Seedphrase is too short. Create a stronger one !"

    salt, password = seedphrase[:5], seedphrase[5:]

    return generate_seeded_key(password, salt, nbytes)