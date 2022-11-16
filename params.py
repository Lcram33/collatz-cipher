#extracted from the string library : string.printable, with some minor changes. You can add yours !
DIGITS = "0123456789"
LATIN_LETTERS = "ABCDEFGHIJKLMNOPQRSTUVWXYZ"
ACCENTS = "éèêëàâäôöîïùûçñœ"
CURRENCIES = "$£¥€"
OTHER_CHARS = """ \\!"#%&'()*+,-./:;<=>?@[]^_`{|}~
µ¤§²¨«»°"""

DEFAULT_CHARSET = LATIN_LETTERS + LATIN_LETTERS.lower() + ACCENTS + ACCENTS.upper() + DIGITS + CURRENCIES + OTHER_CHARS


#just used to confuse cryptanalysts :)
UNUSED_CHARS = "αβΓΔδεζηΘπΦφΨΩωλμνξΣ"