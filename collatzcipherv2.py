import secrets
import json
import base64

from params import DEFAULT_CHARSET, UNUSED_CHARS


MAX_NOISE_LENGHT = 200
confusing_threshold = 40 # in x % of the cases. Changes at each message.

max_shift = len(DEFAULT_CHARSET)

def set_max_shift(new):
    global max_shift
    max_shift = new


def my_base64_encoder(str_input):
    return base64.b64encode(bytes(str_input, 'utf-8')).decode('utf-8')

def my_base64_decoder(str_input):
    return base64.b64decode(bytes(str_input, 'utf-8')).decode('utf-8')

def align(str_input, k):
    str_output = ""
    for i in range(0, len(str_input), k):
        str_output += str_input[i:i+k] + '\n'
    
    return str_output

def format_key(key_object):
    converted = my_base64_encoder(json.dumps(key_object))
    key = align(converted, 64)
    
    return '-----BEGIN COLLATTZCIPHER KEY BLOCK-----\n' + key + '-----END COLLATTZCIPHER KEY BLOCK-----'

def format_message(unformated_ciphertext):
    converted = my_base64_encoder(unformated_ciphertext)
    ciphertext = align(converted, 64)

    return '-----BEGIN COLLATTZCIPHER MESSAGE-----\n' + ciphertext + '-----END COLLATTZCIPHER MESSAGE-----'

def unformat_message(formated_ciphertext):
    ciphertext = formated_ciphertext
    words = ['-----BEGIN COLLATTZCIPHER MESSAGE-----', '-----END COLLATTZCIPHER MESSAGE-----', '\n']
    for word in words:
        ciphertext = ciphertext.replace(word, '')

    return my_base64_decoder(ciphertext)


def shuffle(str_input: str):
    l = len(str_input)
    str_input = list(str_input)
    str_output = ""

    for i in range(l):
        ind = secrets.randbelow(len(str_input))
        str_output += str_input[ind]
        del str_input[ind]

    return str_output

def random_between(min, max):
    rand = secrets.randbelow(max+1)
    while rand < min:
        rand = secrets.randbelow(max+1)
    
    return rand

def gen_noise(charset, split_char):
    new_charset = list(charset)
    if split_char in charset: new_charset.remove(split_char) # so we do not get the split char ! Else the message is not deciphered.

    return ''.join(secrets.choice(new_charset) for i in range(secrets.randbelow(MAX_NOISE_LENGHT)))

def randomly_split(str_input):
    shuffled = shuffle(str_input)
    s = secrets.randbelow(len(shuffled))

    return shuffled[:s], shuffled[-1], shuffled[s:len(shuffled)-1]

def make_charset_and_null_chars(charset, unused_chars):
    to_add_to_charset, split_char, null_chars = randomly_split(unused_chars)
    charset += to_add_to_charset
    charset += split_char

    return shuffle(charset), split_char, null_chars

def gen_key(nbytes = 500):
    charset, split_char, null_chars = make_charset_and_null_chars(DEFAULT_CHARSET, UNUSED_CHARS)
    key_obj = {
        'charset': charset,
        'key': secrets.token_hex(nbytes),
        'split_char': split_char,
        'null_chars': null_chars
    }

    return key_obj

def to_key_object(str_key):
    str_key = str_key.replace('-----BEGIN COLLATTZCIPHER KEY BLOCK-----', '').replace('-----END COLLATTZCIPHER KEY BLOCK-----', '').replace('\n', '')
    try:
        key_obj = json.loads(my_base64_decoder(str_key))
        return key_obj
    except Exception:
        return None


def collatz_sequence(n):
    sequence = [n]
    while n != 1:
        n = 3 * n + 1 if n & 1 else n // 2
        sequence.append(n)
    
    return sequence

def modified_collatz_sequence(int_key, size):
    seq = collatz_sequence(int_key)
    output = [x % max_shift for x in seq if not x & 1]
    if len(output) < size:
        output = (size // len(output) + 1) * output
    
    return output[0:size]


def remove_null_chars(ciphertext, null_chars):
    for char in null_chars:
        ciphertext = ciphertext.replace(char, '')
    
    return ciphertext

def encode(char, charset, int_subkey, split_char):
    try:
        result = charset.index(char) + 1
    except ValueError:
        print("Missing char in charset : " + char)

    result += int_subkey
    if result > max_shift:
        result %= max_shift

    return charset[result - 1]

def decode(char, charset, int_subkey, split_char):
    try:
        result = charset.index(char) + 1
    except ValueError:
        print(f"Missing char in charset : {char} (ord : {ord(char)})")

    result = result - int_subkey
    if result < 0:
        result += max_shift

    return charset[result - 1]

def randomly_confuse_the_cryptanalyst(null_chars):
    if secrets.randbelow(100) < confusing_threshold:
        return '' if len(null_chars) == 0 else secrets.choice(null_chars)
    else:
        return ''

def encrypt_str(plaintext, key_object, armor = True):
    global confusing_threshold
    confusing_threshold = random_between(1, 100)

    set_max_shift(len(key_object['charset']))

    plaintext = gen_noise(key_object['charset'], key_object['split_char']) + key_object['split_char'] + plaintext.replace(key_object['split_char'], '') + key_object['split_char'] + gen_noise(key_object['charset'], key_object['split_char'])
    keys = modified_collatz_sequence(int(key_object['key'], 16), len(plaintext))
    unformated_ciphertext = ""

    for i in range(len(plaintext)):
        unformated_ciphertext += (encode(plaintext[i], key_object['charset'], keys[i], key_object['split_char']) + randomly_confuse_the_cryptanalyst(key_object['null_chars']))

    return format_message(unformated_ciphertext) if armor else unformated_ciphertext

def decrypt_str(ciphertext, key_object, armor = True):
    set_max_shift(len(key_object['charset']))
    
    if armor:
        ciphertext = unformat_message(ciphertext)

    ciphertext = remove_null_chars(ciphertext, key_object['null_chars'])
    keys = modified_collatz_sequence(int(key_object['key'], 16), len(ciphertext))
    plaintext = ""

    for i in range(len(ciphertext)):
        plaintext += decode(ciphertext[i], key_object['charset'], keys[i], key_object['split_char'])

    try:
        return plaintext.split(key_object['split_char'])[1]
    except Exception:
        print("SPLIT ERROR")
        return plaintext
