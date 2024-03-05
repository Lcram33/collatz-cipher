import secrets
import math


def password_entropy(password):
    lowercase = set("abcdefghijklmnopqrstuvwxyz")
    uppercase = set("ABCDEFGHIJKLMNOPQRSTUVWXYZ")
    digits = set("0123456789")
    special_characters = set("!@#$%^&*()-_=+[]{}|;:'\",.<>/?`~")

    has_lower, has_upper, has_digit, has_special = False, False, False, False

    for char in password:
        if not has_lower and char in lowercase:
            has_lower = True
        elif not has_upper and char in uppercase:
            has_upper = True
        elif not has_digit and char in digits:
            has_digit = True
        elif not has_special and char in special_characters:
            has_special = True
        
        if has_lower and has_upper and has_digit and has_special:
            break

    N = (26 if has_lower else 0) + (26 if has_upper else 0) + (10 if has_digit else 0) + (len(special_characters) if has_special else 0)

    return len(password) * math.log2(max(N, 1))

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

def new_passphrase(wordlist, number_of_words, separator):
    wordlist = permutation(wordlist)
    return separator.join([random_choice(wordlist) for i in range(number_of_words)])