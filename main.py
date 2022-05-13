from collatzcipher import *


message = """This is a first test sentence.
Or is it ?
Meh.
The day is shinny."""

print(f"Message is : {message}")
print()

key = gen_key(500)
str_key = format_key(key)

#testing converting back key from text key
#key = to_key_object(str_key)

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
