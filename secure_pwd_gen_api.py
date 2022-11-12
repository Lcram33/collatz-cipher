import secrets
import json


#in case the random library has to be changed
def random_range(min, max):
    new = 0
    while new < min:
        new = secrets.randbelow(max)

    return new


def random_int(max):
    return secrets.randbelow(max)


def random_choice(items):
    return secrets.choice(items)


def permutation(items):
    l = len(items)
    items_list = list(items)
    output = list()

    for i in range(l):
        ind = random_int(len(items_list))
        output.append(items_list[ind])
        del items_list[ind]

    return "".join(output) if type(items) == str else output




#passwords
def new_password(size, chars):
    newpass = ""
    chars = permutation(chars)

    for i in range(size):
        newpass += random_choice(chars)

    return newpass


def new_passords(sizes, chars):
    passwords = list()
    for i in range(len(sizes)):
        passwords.append(new_password(sizes[i], chars))

    return passwords


#passphrases (picking random words)
def load_wordlist(path):
    #making this function in case another method/file format is needed. See perf_test.py for raw import.
    data = None
    with open(path, 'r') as f:
        data = json.load(f)
    return data


def new_passphrase(wordlist, number_of_words, separator):
    wordlist = permutation(wordlist)
    return separator.join([random_choice(wordlist) for i in range(number_of_words)])

def new_passphrases(wordlist, number_of_words, separator, amount):
    passphrases = list()
    for i in range(amount):
        passphrases.append(new_passphrase(wordlist, number_of_words, separator))

    return passphrases
