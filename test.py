#!/bin/python3

from collatzcipher import *
from seeded_key import *
from math import log
from secure_pwd_gen_api import new_passphrase, load_wordlist


def print_fewer_lines(str_input):
    lines = str_input.split('\n')
    if len(lines) > 7:
        splitted = lines[:3] + [f"[skipped {len(lines)-6} lines]"] + lines[-3:]
        print('\n'.join(splitted))
    else:
        print(str_input)

def test_seeded_key():
    wordlist = load_wordlist('wordlist.json')

    number_of_words = 12
    sep = ' '
    phrase_seed = "atonable decent visiting daringly backyard aloft backrest connected reseller gratitude detail direness" #for testing, uncomment next line to generate one
    #phrase_seed = new_passphrase(wordlist, number_of_words, sep)

    print("TESTING SEEDED KEY")
    print("Seed phrase :")
    print(phrase_seed)

    res = generate_seedphrase_key(phrase_seed)

    str_key = format_key(res["key"])
    fgp = res["fingerprint"]

    print()
    print("Generated key :")
    print_fewer_lines(str_key)

    # with the provided passphrase, should be 3c5084525df83f0d757848605468ee428da575a349d89c029a60646c9667f583.
    print(f"Here is the fingerprint (sha256) of you key : {fgp}. Re-checking : {fgp == hash_fingerprint(str_key)}")


def fact(n):
    return 1 if n == 0 else n * fact(n - 1)

nbytes = 100 #WARNING : testing only for readability of the key (you should set a higher value ! Looks decent in terms of speed until ~1000 on a modern computer.)

number_of_hex_keys = int(nbytes * 2 * 'f', 16) - int('1' + (nbytes * 2 - 1) * '0', 16)
number_of_unused_chars_spliting_possibilities = 2 ** (len(UNUSED_CHARS) - 2) - 1 #we don't count the split char.
charset_shuffle_possibilities = fact(max_shift)
number_of_alphabets = len(collatz_sequence(int('1' + (nbytes * 2 - 1) * '0', 16)))
number_of_possible_keys = charset_shuffle_possibilities * number_of_hex_keys * number_of_unused_chars_spliting_possibilities


calculus = f"""
A bit of math !

The number of possible keys ({nbytes} bits for the token_hex and the current charset & unused chars) should be around (feel free to correct if you spot an error) :
10^{round(log(number_of_possible_keys, 10))}, an equivalent of {round(log(number_of_possible_keys, 2))} bits.
I estimate that there are 10^{round(log(2 * sum(len(DEFAULT_CHARSET) ** k for k in range(15, 75)), 10))} encrypted messages with the same message and key.
Also, there should be {number_of_alphabets} alphabets (this is a polyalphabetic cipher).
See readme for more details.
"""

print(calculus)


message = """This is a first test sentence.
Or is it ?
Meh.
The day is shinny.
Let's test weird stuff : $É\\²"""

print(f"Message is : {message}")
print()


key = gen_key(nbytes)

str_key = format_key(key)

#converting key from text key (testing)
key = to_key_object(str_key)

print("The key is : ")
print_fewer_lines(str_key)
print()


cipher = encrypt_str(message, key)
deciphered = decrypt_str(cipher, key)

print(f"Encrypted message is :")
print_fewer_lines(cipher)
print()

print(f"Decrypted message is :")
print(deciphered)
print(f"Match with original message ? {'YES' if deciphered == message else 'NO'}")


print()
print()
print("what the enciphered message looks like :")
print(unformat_message(cipher))

print()
print()
print("what the key looks like :")
print(key)

print()
print()
test_seeded_key()
