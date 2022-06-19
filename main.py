from collatzcipher import *


def fact(n):
    return 1 if n == 0 else n * fact(n - 1)

charset_shuffle_possibilities = fact(max_shift)

nbytes = 500
number_of_hex_keys = (int(nbytes * 2 * 'f', 16) - int('1' + (nbytes * 2 - 1) * '0', 16))

number_of_unused_chars_spliting_possibilities = fact(len(UNUSED_CHARS)) * len(UNUSED_CHARS)

calculus = f"""
A bit of math !

The number of possible keys ({nbytes} bits for the token_hex and the current charset & unused chars) should be around (feel free to correct if you spot an error) :
10^{len(str(charset_shuffle_possibilities * number_of_hex_keys * number_of_unused_chars_spliting_possibilities))-1}
"""

print(calculus)


message = """This is a first test sentence.
Or is it ?
Meh.
The day is shinny."""

print(f"Message is : {message}")
print()


key = gen_key()

str_key = """-----BEGIN COLLATTZCIPHER KEY BLOCK-----
eyJjaGFyc2V0IjogIlx1MDBmNFhBcHd8Uj1GOGNcdTAwZWVhT1Y5KXRcIjQmSnhu
W2YjMm1cdTAwZWZFbENkUFxucm9nLWk1V1x1MDBlOHVUQlx1MDBlN14hM1x1MDBj
OWBVLGJTcVx1MDBlYWt9PDdMLzEoJFoqejAnezZJK1ldXHUwMGUyLlx1MDBlMEhc
dTAwZTk6JU4gdlx1MDBmOUdEPjtRamVLfk15X3M/QGgiLCAia2V5IjogImQ2MjYx
NDk1NzVkMGY2MGQ3ZTE2ODMxZTUwYWVjMDEwMTBmOWJiZmQzYThiMDRmZGI5MzMw
MDRiMmE5YmYxMWE1OTAwNzRjODQ2ZWUzMzYzZjgxYWExNjZhMzJiMWQ1NDE2Nzg0
MDI4YTVlM2FhZmQ3MmNkYTRlYjM4OWQzNGEyNjZmMDM0MTFjOWU4MzU2ZWFhMjlm
NjI0ZjQxZWRlYTM5NTRkYWM0ZDNiZDZmMmRmNTk3NzFiZmYzNjExMTY4ZWE1ZTEw
ZGFjMTYyNDg4ZTliMGUzYjQ4NGM0NzI4NjNhOWVjODg5ZDYyMmRlMTgyM2VhZmEx
NGIzMGNiY2EwNmJlYjNjMGU4ZGRjNDY1MjJiMmU5MThhMGVjNGI3ZmEwNTlmZTRl
YjQ3OWNlNTE0YjRlOWI1NmJlNGU5OWI3OTI4ZjdlMjlkYmJjNWY4Mjg5NmEzOGI4
OGJlYjUwZWVhM2U5MjM2ZDE0YzkyZjA3YmI4MDZlZTZkNjQxMzk5YTgyNTA0NzVk
MjVmZWFjM2RmMmI3NDc2NWM2NDIyNTJmMjE1OTQyNGI3YjI3ZjE3ODIyMjMzNWE0
NmIxNGM4YzUwNGUyMmRmZjAxODE2OGE1NzU4NjAyNmVlY2Y2MDc5MGE5ZDk5ZDEw
YjhjZWZjMjQ0NDU1Njk4ZmJjYWM2NGMyMTVkYWI2YjU1MzAxNjFmNDNlNzM2MGY4
ZDYxNzAyZTYzOGRlMGRmMDExMGIxMjYwMzMwOTIzOGE1ZWU0YjU1ZDU2Mjg4NDJi
YTc2YjdhNmRmMDQ4NWU4NzVmODRjYzNjOGQ1ZDhkNmRiOTBmODMzODk3Mzk3NTU3
YmMyYWU4YTZhOTg2MjFlN2QxMGRkMmM1ZTg1ZDBlNjQwZTU2NzgwZWExM2ZmZjQ1
NDc4YTU2N2E1OWI3NDdmNjE0OGQxNGI2YWJjNTQ0NzllMjM2NWFkODUwNzU3YWI4
MzI2ODY5YjkwY2VmOGFhOTI1ZTk3OTgzMWVjNzE3YzI5ZWNiNjdjYmIzZTBhYjBk
NTA1ZWQyZGI3N2IzOWNkNTY0YTRiZjkwMjI1NjM1MjFiNzFmOTkzNjU3MDliYzMx
ZjI4MTcwYjlhMzA1N2RjMWJkMTliMWRlMTRlZmUwYjIxZGIxOTc1NDE2MzQzY2Fk
YzkxMjcxMzIxNTZkZDdmMGRiN2E4YzgxMGY2ZTI2YWNiOGFhZGQ5M2EyY2I0MDkx
OTlhODM0MDdiMWJhZWM2YWYwNzI1ZTE2NTM0YzNmM2M5YTEwM2YyYjNmMzEwMTA4
YTRiYWIzODI3ODgyZWI4OTM0ZDdjZTQwNGEzMTkwZmQyNmQiLCAibnVsbF9jaGFy
cyI6ICJcdTAzOThcdTAzYjdcdTAzOTNcdTAzYjFcdTAzYjZcdTAzYjVcdTAzOTRc
dTAzYjRcdTAzYjIifQ==
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
