# Those paramaters was used to generate the key for the challenge.
# Use this one and NOT params.py (was updated since !!)
# Also make sure to use collatzcipher-v1.0.py instead of collatzcipher.py
# To be sure, you can rely on this commit (first one with the challenge) : https://github.com/Lcram33/collatz-cipher/commit/3d06dfa3d013d09b85a2fcd71d35c69610811db5


#extracted from the string library : string.printable, with some minor changes. You can add yours ! Be careful with the \ char, however,
#and some other chars that may be used by Python, causing some errors/unexpected behaviour.
DIGITS = "0123456789"
LATIN_LETTERS = "ABCDEFGHIJKLMNOPQRSTUVWXYZ"
OTHER_CHARS = """ !"#$%&'()*+,-./:;<=>?@[]^_`{|}~
ùéèêàâôîïçÉÀÊÎÇ"""

DEFAULT_CHARSET = OTHER_CHARS + LATIN_LETTERS + LATIN_LETTERS.lower() + DIGITS


#just used to confuse cryptanalysts :)
UNUSED_CHARS = "αβΓΔδεζηΘ"