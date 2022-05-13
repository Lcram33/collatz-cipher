#extracted from the string library : string.printable, with some minor changes. You can add yours ! Be careful with the \ char, however,
#and some other chars that may be used by Python, causing some errors/unexpected behaviour.
DEFAULT_CHARSET = """0123456789abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ
ùéèêàâôîïçÉ !"#$%&'()*+,-./:;<=>?@[]^_`{|}~"""


#just used to confuse cryptanalysts :)
UNUSED_CHARS = "αβΓΔδεζηΘ"