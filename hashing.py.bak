import hashlib
import bcrypt


# Bcrypt can adapt to increase of calculus power. This value should be increased as time go on.
BCRYPT_COST_FACTOR = 14


def gen_salt():
    return bcrypt.gensalt(BCRYPT_COST_FACTOR).decode('utf-8')

def sha256_string(my_string):
    return hashlib.sha256(my_string.encode('utf-8')).hexdigest()

def sha256_file(file_path):
    with open(file_path, 'rb') as f:
        return hashlib.sha256(f.read()).hexdigest()

def sha512_string(my_string):
    return hashlib.sha512(my_string.encode('utf-8')).hexdigest()

def bcrypt_string(password, salt):
    hashed_password = bcrypt.hashpw(password.encode('utf-8'), salt.encode('utf-8'))

    return hashed_password.decode('utf-8')


def hash_password_legacy(password, salt):
    # number of iterations of SHA512 to slow down a bit bruteforce. bcrypt is better, use when possible !
    HASHING_ITERATIONS = 600000 # DO NOT CHANGE as it would break determinism for previously generated keys.

    # salting and mixing
    if len(password) > 4:
        password = password[0] + salt[0] + password[1:3] + salt[1] + password[3:] + salt[2:]
    else:
        password += salt

    hashed = sha512_string(password)
    
    # avoiding bruteforce
    for i in range(HASHING_ITERATIONS):
        hashed = sha512_string(f"{hashed}{i}")

    return hashed

def hash_password(password, salt):
    def mix(a, b):
        return ''.join([char1 + char2 for char1, char2 in zip(a, b)])
    
    bcrypt_hash = bcrypt_string(password, salt)
    
    # the use of SHA512 here is so the result look more random, we just use bcrypt to slow down a potential attacker
    h_part1 = sha512_string(bcrypt_hash + salt)
    h_part2 = sha512_string(bcrypt_hash)

    return mix(h_part1, h_part2)

def hash_fingerprint(my_string):
    return sha256_string(my_string)