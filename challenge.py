"""
Want to try to break my cipher ?
Find the original message ! Output is below the program, I did the following : python3 challenge.py >> challenge.py
As proof, send me the original message by email, and how you found it.

Hint :
- The key was made with nbytes = 100 and the default params provided in params.py.
- The message is 2 sentences long, in English.
"""

from solution import STR_KEY, MESSAGE
from collatzcipher import *

key = to_key_object(STR_KEY)
#key = gen_key(100)
#print(format_key(key))

cipher = encrypt_str(MESSAGE, key)
print(f"Encrypted message is :")
print(cipher)
print()

print("Decryption...")
deciphered = decrypt_str(cipher, key)
print(f"Match with original message ? {'YES' if deciphered == MESSAGE else 'NO'}")

"""
Encrypted message is :
-----BEGIN COLLATTZCIPHER MESSAGE-----
ZM6Uc8OnzrVaL860bc60SWYjTcOHRM63Qc63dzVreM6YezzOtUPDiVnOlDnOlEnO
tGxpw4lww6nOmGzOtkbOsc6TM86yYsO5zrJDw6JqzrdRaGvOlCZnLyBFQmPOtTjO
tSvOsjJvzpM2zpgzzrRmdCTOsmgzzrdjK862dc6yZc63SiF6fM6UZc6yZzZ7zrZ3
b8OuzpR2TVLOslkgUi12Ic62ODLOtUPOtXgqzrbDgHRrw67OmDIrJCpSzpMjzrVW
w6lUzrRkSmYrUCbOtibOtkdzU862YXHOmC1STcOJzpMuZM6Ydy7Ok3TOtzrOtVXO
tk9GzrVbzrZRzrbDr3zOlFsyWDXOtVJmZM60SkJ+zpRyzpQyzrd+eGMvzrExzphx
O0EzO861W23OtWVoQs61RMO5cWLOlCPOtU/Ot0l0SnvOk27OkznOtTRWzpNJw6lZ
ac6TQ860dc60d8OvzpjDqM60b86yw4fDoM6yUs63w4DOtjbOtznOlG0=
-----END COLLATTZCIPHER MESSAGE-----

Decryption...
Match with original message ? YES
"""
