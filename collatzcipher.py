import secrets
import json
import base64

from params_default import DEFAULT_CHARSET, UNUSED_CHARS


max_shift = len(DEFAULT_CHARSET)

def my_base64_encoder(str_input):
    return base64.b64encode(bytes(str_input, 'utf-8')).decode('utf-8')

def my_base64_decoder(str_input):
    return base64.b64decode(bytes(str_input, 'utf-8')).decode('utf-8')

def align(str_input, k):
    str_output = ''
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

def gen_noise(charset):
    noise = ''
    for i in range(random_between(100, 1000)):
        noise += secrets.choice(charset)
    return noise


def randomly_split(str_input):
    shuffled = shuffle(str_input)
    s = secrets.randbelow(len(shuffled))

    return shuffled[:s], shuffled[s:]

def make_charset_and_null_chars(charset, unused_chars):
    to_add_to_charset, null_chars = randomly_split(unused_chars)
    charset += to_add_to_charset

    return shuffle(charset), null_chars

def gen_key(nbytes = 800):
    charset, null_chars = make_charset_and_null_chars(DEFAULT_CHARSET, UNUSED_CHARS)
    key_obj = {
        'charset': charset,
        'key': secrets.token_hex(nbytes),
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

def encode(char, charset, int_subkey):
    try:
        result = charset.index(char) + 1
    except ValueError:
        print("Missing char in chars var : " + char)

    result += int_subkey
    if result > max_shift:
        result %= max_shift

    return charset[result-1]

def decode(char, charset, int_subkey):
    try:
        result = charset.index(char) + 1
    except ValueError:
        print(f"Missing char in chars var : {char} (ord : {ord(char)})")

    result = result - int_subkey % max_shift
    if result < 0:
        result += max_shift

    return charset[result - 1]

def randomly_confuse_the_cryptanalyst(null_chars):
    if secrets.randbelow(100) < 10:
        return secrets.choice(null_chars)
    else:
        return ''

def encrypt_str(plaintext, key_object):
    global max_shift
    max_shift = len(key_object['charset'])

    plaintext = gen_noise(key_object['charset']) + 'BEGINREALMESSAGE' + plaintext + 'ENDREALMESSAGE' + gen_noise(key_object['charset'])
    keys = modified_collatz_sequence(int(key_object['key'], 16), len(plaintext))
    unformated_ciphertext = ''

    for i in range(len(plaintext)):
        unformated_ciphertext += (encode(plaintext[i], key_object['charset'], keys[i]) + randomly_confuse_the_cryptanalyst(key_object['null_chars']))

    return format_message(unformated_ciphertext)

def decrypt_str(formated_ciphertext, key_object):
    global max_shift
    max_shift = len(key_object['charset'])
    
    ciphertext = remove_null_chars(unformat_message(formated_ciphertext), key_object['null_chars'])
    keys = modified_collatz_sequence(int(key_object['key'], 16), len(ciphertext))
    plaintext = ''

    for i in range(len(ciphertext)):
        plaintext += decode(ciphertext[i], key_object['charset'], keys[i])

    try:
        return plaintext.split('BEGINREALMESSAGE')[1].split('ENDREALMESSAGE')[0]
    except Exception:
        return plaintext
