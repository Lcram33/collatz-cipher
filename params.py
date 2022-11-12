#extracted from the string library : string.printable, with some minor changes. You can add yours ! Be careful with the \ char, however,
#and some other chars that may be used by Python, causing some errors/unexpected behaviour.
DIGITS = "0123456789"
LATIN_LETTERS = "ABCDEFGHIJKLMNOPQRSTUVWXYZ"
OTHER_CHARS = """ !"#$%&'()*+,-./:;<=>?@[]^_`{|}~
ùéèêàâôîïçÉÀÊÎÇ"""

DEFAULT_CHARSET = OTHER_CHARS + LATIN_LETTERS + LATIN_LETTERS.lower() + DIGITS


#just used to confuse cryptanalysts :)
UNUSED_CHARS = "αβΓΔδεζηΘ"