from collatzcipher import *


def fact(n):
    return 1 if n == 0 else n * fact(n - 1)

charset_shuffle_possibilities = fact(max_shift)

nbytes = 100 #WARNING : testing only for readability of the key (you should set a higher value !)
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


key = gen_key(nbytes)

str_key = """-----BEGIN COLLATTZCIPHER KEY BLOCK-----
eyJjaGFyc2V0IjogIkR+XHUwMzkzXHUwMGUyV3ZIN1x1MDBlMDVmSXM4XHUwM2I0
TH0/MWkreFYjXHUwMGU3bl5aJVx1MDBjOXlcdTAzYjJQNkVVLCdOKV9He3cvXHUw
Mzk4Rl1CYVtwfGhcdTAwZWFgPlx1MDBlOW9ydVJAXHUwMGU4NFwiXHUwMGY5azNU
XHUwMGVlSy16ZVNYOTIgZ1FiY1lNbFx1MDBmNCZBME90anE6KG1cdTAwZWYuOyFk
Q1x1MDNiNUpcbio8JD0iLCAia2V5IjogIjYwNmJhNzY3ZjIzMzQwZDEzOWNmZWMy
ZmM5YmJlNTBlOTY2M2M0NDA5YmMwNWYxZDk5NDgzYjlhOWIzOWZhOGRkNmFhODky
ODdmZTRhMDNiODFlZWUwNGJmMjkwZDQ0MjAzMDNjYjZiODUzM2U5Y2U4MjNhNTUw
MGJiZWE2YzQzYjc5NjkwMjEzMTEyYjYxY2I1M2YxZGVmY2FiZmM4MzFlM2YzYTk5
ZTdhOTNlMWIzNjA4ZDdkYjMzYzkyNjcyMTUwNTEyNzdlMzY1ZDRkODU2ODk0ZGQw
MjMzNDgwOGQ4MDk3MTEwNmFiMmVmNWI3NzllZTEwNTQwNTBlMDZkZGYyNjQzNzRk
YTIyM2NhYjhkMGE3NWEzMWYxZTI4YzRmZDM2YTljZDVhNjBlOTk2ZjJiMjQ5YTU3
NzRhOTljMDA4NDJhM2EwMzRlMDZjZDEwNjRjMGYzMGQ2ZDFiZGVlYmRhYTI4NzNl
MGViN2NkZTAwNzBhYWViYTQwMDg5MTk5NTJhYjY0MThiY2JiODdlMjNiNTEwMGFk
ODA3MDkyYjBkZTI3YmIzMWVkNzA0ZTE5NDE3OWRkODBiODhlZDI1NGU1ZjJiYjZm
MmNhZmY4OTZhMTY4NzE4ZmEyNjM3NGY4MDA4NzU0NzExM2Y4YmZjM2NhN2NiYmM3
ZjI1OGQ3Nzc0ZDQyZmMwNzAxODY1MTQ4OGE1YWI0NmJlYTY2NzMyYzc5ZDg5YmEz
ZGUzZjdhNmQyNjViOWUyODgwMmU0NGM4MWUwNmM1MGRiZTYxYmVlNWI5OGNmNWJm
NmM2YjhlMjRkMzdmNTgxMGYxOTA5ZGYxZWUxZTM5NjViNmU3OWVmYzU0YTQyNmNh
NTk1YTgwM2EzZDM5MmE1ZGE1ZDc3YTViNTgyNWRkMWExZTczYWIzNzk2NjdlZDg4
ODc0NDExMzY2NzJlM2VjZjY2NTE2NTAwYmY2NTJkNzJkMDhlOTk4NjEyNTRkMDdj
ZGYxMTg0ZDhkNDY2YjkyYjE3MTAxYTg4NzI2MGFjMGFmZmFiOGU1Y2NjZmNjYTcz
MDNlODBkYjljMDU2ZTRjZmIzNDVkOWRlM2RlYzEyNjJkYTQ2OGM1OWUyMTQ5YjVk
NTcxN2RjNTBhOGY5ZTE3MTY5MDgxYjBmOWZmY2M4YTBkZjVmYjU4NjFlYTA4ZGYx
ZDI5ODBmZWQ1M2IwNWQ2NGQ5ZmI5MDc4NDQwZmEzNTYxNWUxNmY3ODJiMGMyOGE2
ZDc0NDMzZDlhZjBlMzA1N2UyZTQ5NTUxNzY1ZTk5NzYyNjQzZTNkNzM4OTljN2Jl
ZDEzNGY2MTFiOWNjNDZmYjUyMTc4OGU2Mjc0YTAzZmZmYTRjNzBkZDAzZmI1NzNl
NDUyYjIzNzgzM2EyZTY4ZTczZTNjMmFjNjdhNTQyOGM0MTQ3YTIzNjczMzIzMGQ3
ZmFlMTY2OGRlMzdlZTA4MTI4ZjZhNTQwOGM3MGEwZjg2ODJiNjBlN2M1ZmNlMjNi
N2JlYzA1NTU1MzJiZjVhYWFmMTg1OGEyMTI3ODAxMmZkM2ZiMjI4MzlhNDE4YmEz
MjA2MThkOGExZTJlMTZiNDhkYjAwOTU2N2FlYTU3OWVhZDNjZTRiNzg1ZDk5ZDI3
YWM3MGY5ZDZmY2ZjNGQ2OGZmMjNkODUzMzBkZDY4N2UzYmE5NGJiOTlmMzk3ZjVl
YTkyNzk1N2YzYmI0M2IyZjMzYjg2NjczOGViNGU1MmEyZGQ5ZjhmNzk4YzZhNjZl
YjIyYTFhNmE0YmFlZmU1OThhZmIxOGNjNmM0NGVkYzExNzhjODNhNWNmYTIxN2Qx
YmI3YzI3ZmU3OGYxZjgwNjgwY2JlNWRmMzc3ZDgzZTIyNDk2YTg1NDUwYTg2MDk3
ZjBhMTA3ZDAxYjg0YjE3MTU5YWVhZjY2ODIyZjcwZTJlNjc5YmQzNDdhMGZkZjk2
YzRkOTBkZGQxMmIyZDllNjcyNWU2YjVlNmI1MDkyZDk3MTU3ZGU5NTNkNjRiZjFm
NGY2ZWMxMWU4MzY0N2ZhMmJiYmEzZWQ1MjdmMGViNjMzNDI0YjZmNDNlNjg0MjMy
NTVhOWJkNjU4M2M2NWUzZDk5YzhkNThhMmEyMWJlZjYyYzY4ZWY2YmUiLCAic3Bs
aXRfY2hhciI6ICJcdTAzYjEiLCAibnVsbF9jaGFycyI6ICJcdTAzYjZcdTAzYjdc
dTAzOTQifQ==
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
