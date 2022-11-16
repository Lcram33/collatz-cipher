from collatzcipher import *
from seeded_key import *
from math import log


def fact(n):
    return 1 if n == 0 else n * fact(n - 1)

nbytes = 100 #WARNING : testing only for readability of the key (you should set a higher value ! Looks decent in terms of speed until ~1000 on a modern computer.)

number_of_hex_keys = int(nbytes * 2 * 'f', 16) - int('1' + (nbytes * 2 - 1) * '0', 16)
number_of_unused_chars_spliting_possibilities = 2 ** (len(UNUSED_CHARS) - 2) - 1 #we don't count the split char.
charset_shuffle_possibilities = fact(max_shift)

number_of_possible_keys = charset_shuffle_possibilities * number_of_hex_keys * number_of_unused_chars_spliting_possibilities


calculus = f"""
A bit of math !

The number of possible keys ({nbytes} bits for the token_hex and the current charset & unused chars) should be around (feel free to correct if you spot an error) :
10^{round(log(number_of_possible_keys, 10))}, an equivalent of {round(log(number_of_possible_keys, 2))} bits.
I estimate that there are 10^{round(log(2 * sum(len(DEFAULT_CHARSET) ** k for k in range(15, 75)), 10))} encrypted message with the same message and key.
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
print(str_key)
print()


cipher = encrypt_str(message, key)
deciphered = decrypt_str(cipher, key)

print(f"Encrypted message is :")
print(cipher)
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