from collatzcipher import *
from seeded_key import *
from math import log


def fact(n):
    return 1 if n == 0 else n * fact(n - 1)

nbytes = 100 #WARNING : testing only for readability of the key (you should set a higher value !)

number_of_hex_keys = int(nbytes * 2 * 'f', 16) - int('1' + (nbytes * 2 - 1) * '0', 16)
number_of_unused_chars_spliting_possibilities = 2 ** (len(UNUSED_CHARS) - 2) - 1 #comes from https://math.stackexchange.com/questions/3340723/how-many-ways-to-partition-n-elements-into-two-nonempty-subsets + we don't count the split char.
charset_shuffle_possibilities = fact(max_shift)

number_of_possible_keys = charset_shuffle_possibilities * number_of_hex_keys * number_of_unused_chars_spliting_possibilities


calculus = f"""
A bit of math !

The number of possible keys ({nbytes} bits for the token_hex and the current charset & unused chars) should be around (feel free to correct if you spot an error) :
10^{round(log(number_of_possible_keys, 10))}, an equivalent of {round(log(number_of_possible_keys, 2))} bits.
"""

print(calculus)


message = """This is a first test sentence.
Or is it ?
Meh.
The day is shinny."""

print(f"Message is : {message}")
print()


key = gen_key(nbytes)

str_key = """-----BEGIN COLLATTZCIPHER KEY BLOCK-----
eyJjaGFyc2V0IjogIjNcdTAwZjRcdTAwZWUhc1x1MDBjOVd8MVx1MDBjYUBFfXJi
T1x1MDBlYXdHXiluQVhDPVx1MDNiNjdkXHUwMzk0VFx1MDBlOFx1MDBlMDZTTlZv
TCUuSFx1MDBlN2UoeFx1MDBjZVA0ODx6XHUwMGUyRGxoY2YkXG5hdHtNIFpKanVC
VTJcdTAwYzddUlF+KnltNT9ZLVwiXHUwMGU5OUlLXHUwMGVmYC8jdjpGcWsnJmdf
LDtpW1x1MDBmOVx1MDBjMDArcD4iLCAia2V5IjogIjJjYjE3MjY1NmU5YTMxZjcx
ZjNjYTFiOGRlMmIxMDA4M2QzODQ5MWUzNWU3YmJlZTliYTEyMDM5ZjQwMzQyOGNm
MDNlNmI3ZWI0MDFlOWE2ZGNhODZhNzNjNjRkOTUyYmM1ZGQ0ODU5ZDRmMGFjNzM2
MWFmYWU0YzVkZDk4Y2QyZDYxZjM1ZDVkMTY2OWYwMTZmODI1YjVmNjMyNWEyZDU3
NDNlN2FkZDI3MTExYzUyNWY2NmZiYTBkMjAwOTU4YmJlY2JhMGYwIiwgInNwbGl0
X2NoYXIiOiAiXHUwM2I1IiwgIm51bGxfY2hhcnMiOiAiXHUwM2I0XHUwMzk4XHUw
M2IxXHUwM2I3XHUwM2IyXHUwMzkzIn0=
-----END COLLATTZCIPHER KEY BLOCK-----"""

#you can either use the generated key or use the one provided above as an example !
#str_key = format_key(key)

#converting key from text key
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