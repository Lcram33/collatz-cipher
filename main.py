#!/bin/python3

import typer
import os
import json
import getpass
import zlib
from datetime import datetime

from secure_pwd_gen_api import new_passphrase, password_entropy
from wordlist import wl_bip39
from collatzcipher import *
import collatzcipherv2
from seeded_key import *
from params import *
from hashing import sha256_file, sha256_string


PATH = os.path.expanduser('~') + "/.collciph/"
integrity_algs_string = {
    "sha256": sha256_string
}
integrity_algs_file = {
    "sha256": sha256_file
}


def file_bytes_to_compressed_base64(path):
    with open(path, 'rb') as f:
        compressed_data = zlib.compress(f.read(), level=9)

    b64_string = base64.b64encode(compressed_data).decode('utf-8')
    
    return b64_string

def compressed_base64_to_file(path, compressed_b64_string):
    b64_bytes = compressed_b64_string.encode('utf-8')
    compressed_data = base64.b64decode(b64_bytes)

    decompressed_data = zlib.decompress(compressed_data)

    with open(path, 'wb') as f:
        f.write(decompressed_data)

def print_key_data(path):
    try:
        with open(path, 'r') as f:
            data = json.load(f)
    except Exception as e:
        print(f"Error while reading file : {e}")
        return
    
    print(f"""
{"key" if "key" in data else "salt"}   collatz-cipher{data["nbytes"]} {data["date"]}
    {data["fingerprint"].upper()}
uid         {"[unknown]" if data["name"] == '' else data["name"]}
{'' if data["desc"] == '' else f'desc         {data["desc"]}'}
    """)

def load_key(fgp, v2: bool = False):
    path = PATH + fgp + ".key"
    
    if not os.path.exists(path):
        print("Error : key does not exists.")
        return False

    try:
        with open(path, 'r') as f:
            data = json.load(f)
    except Exception as e:
        print(f"Error while loading key : {e}")
        return False

    if "salt" in data:
        password = getpass.getpass(prompt="Password : ")
        result = generate_seeded_key(password, data["salt"], data["nbytes"], v2)

        if result["fingerprint"] != data["fingerprint"]:
            print("Wrong password.")
        else:
            return result["key"]
    else:
        return data["key"]
    
    return False


app = typer.Typer()

@app.command(help=f"Generate a key and store it locally (under {PATH}). WITHOUT PASSWORD, IT IS STORED IN CLEAR.")
def gen(nbytes: int = 500, name: str = '', desc: str = '', password: bool = False):
    if password:
        password = getpass.getpass(prompt="Password : ")
        if password_entropy(password) < 100:
            if input("Password is weak. Continue ? (y/n) ") != 'y':
                return

        password_confirm = getpass.getpass(prompt="Confirm password : ")
        if password != password_confirm:
            print("Passwords don't match.")
            return

        result = generate_seeded_key(password, nbytes=nbytes)
        fgp = result["fingerprint"]
        data = {
            "name": name,
            "desc": desc,
            "date": datetime.now().strftime("%Y-%m-%d"),
            "salt": result["salt"],
            "nbytes": nbytes,
            "fingerprint": fgp
        }
    else:
        key = gen_key(nbytes)
        fgp = hash_fingerprint(format_key(key))
        data = {
            "name": name,
            "desc": desc,
            "date": datetime.now().strftime("%Y-%m-%d"),
            "key": key,
            "nbytes": nbytes,
            "fingerprint": fgp
        }

    if not os.path.exists(PATH):
        os.mkdir(PATH)
    
    path = PATH + fgp.upper() + ".key"

    try:
        with open(path, 'w+') as f:
            json.dump(data, f)
        
        print_key_data(path)
    except Exception as e:
        print(f"Error while writing file : {e}")

@app.command(help="Generate a cipher key with a seed phrase.")
def seededkey(nbytes: int = 500, name: str = '', desc: str = '', input: bool = False):
    seedphrase = ''
    
    if input:
        seedphrase = getpass.getpass("Seedphrase : ")

    if seedphrase == '':
        number_of_words = 24
        sep = ' '
        seedphrase = new_passphrase(wl_bip39, number_of_words, sep)
    
        print("Seed phrase :")
        print(seedphrase)
    else:
        if password_entropy(seedphrase) < 100:
            if input("Seedphrase is weak. Continue ? (y/n) ") != 'y':
                return
        
        seedphrase_confirm = getpass.getpass("Confirm seedphrase : ")
        if seedphrase != seedphrase_confirm:
            print("Seedphrases do not match.")
            return

    res = generate_seedphrase_key(seedphrase, nbytes)
    fgp = res["fingerprint"]
    
    path = PATH + fgp.upper() + ".key"
    data = {
        "name": name,
        "desc": desc,
        "date": datetime.now().strftime("%Y-%m-%d"),
        "key": res["key"],
        "nbytes": nbytes,
        "fingerprint": fgp
    }

    if not os.path.exists(PATH):
        os.mkdir(PATH)

    try:
        with open(path, 'w+') as f:
            json.dump(data, f)
        
        print_key_data(path)
    except Exception as e:
        print(f"Error while writing file : {e}")

@app.command(help="Encrypts the input stream with the provided key.")
def enc(key: str, armor: bool = False, v2: bool = False):
    key = load_key(key, v2)
    if not key:
        print("Unable to load key. Exiting.")
        return
    
    print("Enter/Paste your content. Ctrl-D or Ctrl-Z ( windows ) to save it (on an empty line !).")
    contents = []
    while True:
        try:
            line = input()
        except EOFError:
            break
        contents.append(line)
    str_data = '\n'.join(contents)

    if str_data == '':
        print("No data to encrypt.")
        return

    new_data = {}
    new_data["data"] = str_data
    new_data["hash"] = sha256_string(str_data)
    new_data["algorithm"] = "sha256"
    str_data = json.dumps(new_data)

    if v2:
        enciphered = collatzcipherv2.encrypt_str(str_data, key, armor)
    else:
        enciphered = encrypt_str(str_data, key, armor)

    print()
    print("Here is the encrypted message :")

    if armor: print(enciphered)
    else:
        print(os.get_terminal_size()[0] * '-')
        print(enciphered)
        print(os.get_terminal_size()[0] * '-')

@app.command(help="Decrypts the input stream with the provided key.")
def dec(key: str, armor: bool = False, v2: bool = False):
    key = load_key(key, v2)
    if not key:
        print("Unable to load key. Exiting.")
        return
    
    print("Enter/Paste your content. Ctrl-D or Ctrl-Z ( windows ) to save it.")
    contents = []
    while True:
        try:
            line = input()
        except EOFError:
            break
        contents.append(line)
    str_data = '\n'.join(contents)

    if str_data == '':
        print("No data to decrypt.")
        return

    armor = "BEGIN COLLATTZCIPHER MESSAGE" in str_data
    if v2:
        deciphered = collatzcipherv2.decrypt_str(str_data, key, armor)
    else:
        deciphered = decrypt_str(str_data, key, armor)

    print()
    try:
        json_data = json.loads(deciphered)
        if "algorithm" in json_data and "hash" in json_data:
            if json_data["algorithm"] in integrity_algs_string:
                integrity_alg = integrity_algs_string[json_data["algorithm"]]
                if json_data["hash"] == integrity_alg(json_data["data"]):
                    print("-- Data integrity check passed --")
                else:
                    print("-- Warning : Data integrity check failed ! The data might have been corrupted --")

            deciphered = json_data["data"]
    except Exception:
        pass

    print("Here is the decrypted message :")
    print(os.get_terminal_size()[0] * '-')
    print(deciphered)
    print(os.get_terminal_size()[0] * '-')

@app.command(help="Encrypts the file with the provided key.")
def encf(key: str, infile: str, encname: bool = False, armor: bool = False, v2: bool = False):
    key = load_key(key, v2)
    if not key:
        print("Unable to load key. Exiting.")
        return
    
    try:
        str_data = file_bytes_to_compressed_base64(infile)
    except Exception as e:
        print(f"Error while loading input file : {e}")
        return

    new_data = {}
    new_data["data"] = str_data
    new_data["hash"] = sha256_file(infile)
    new_data["algorithm"] = "sha256"
    if encname:
        outfile = gen_noise(LATIN_LETTERS + DIGITS, '!')[:15] + '.czcenc'
        new_data["filename"] = infile
    else:
        outfile = infile + '.czcenc'
    str_data = json.dumps(new_data)

    if v2:
        enciphered = collatzcipherv2.encrypt_str(str_data, key, armor)
    else:
        enciphered = encrypt_str(str_data, key, armor)

    try:
        with open(outfile, 'w') as f:
            f.write(enciphered)        
    except Exception as e:
        print(f"Error while writing data : {e}")

@app.command(help="Decrypts the file with the provided key.")
def decf(key: str, infile: str, v2: bool = False):
    key = load_key(key, v2)
    if not key:
        print("Unable to load key. Exiting.")
        return
    
    try:
        with open(infile, 'r') as f:
            str_data = f.read()
    except Exception as e:
        print(f"Error while loading input file : {e}")
        return

    armor = "BEGIN COLLATTZCIPHER MESSAGE" in str_data
    if v2:
        deciphered = collatzcipherv2.decrypt_str(str_data, key, armor)
    else:
        deciphered = decrypt_str(str_data, key, armor)

    outfile = infile.removesuffix(".czcenc")
    hash = None
    algorithm = None
    try:
        json_data = json.loads(deciphered)
        deciphered = json_data["data"]
        algorithm = json_data["algorithm"]
        hash = json_data["hash"]
        outfile = json_data["filename"]
    except Exception:
        pass

    try:
        compressed_base64_to_file(outfile, deciphered)        
    except Exception as e:
        print(f"Error while writing data : {e}")
    
    if algorithm in integrity_algs_file:
        integrity_alg = integrity_algs_file[algorithm]
        if hash == integrity_alg(outfile):
            print("-- Data integrity check passed --")
        else:
            print("-- Warning : Data integrity check failed ! The data might have been corrupted --")

@app.command(name="list", help="Print all keys properties.")
def _list():
    if not os.path.exists(PATH):
        os.mkdir(PATH)

    files = [x for x in os.listdir(PATH) if os.path.isfile(os.path.join(PATH,x))]

    for file in files:
        print_key_data(os.path.join(PATH,file))

@app.command(help="Print the key formatted to base64 so you can share it with someone. Not recommended, it is better to send a salt key file, or share a seed !")
def export(key: str, v2: bool = False):
    print("WARNING")
    print("The key will be exported IN CLEAR. Which means that anyone getting access to it will be able to decyrpt any message encrypted with it !")
    print(f"If you created the key with a password, you can safely share the file of the key : {PATH + key + '.key'}")

    if input("Do you want to export the key ? (it will be printed in the terminal) (y/n) : ") != 'y': return

    key = load_key(key, v2)
    if not key:
        print("Unable to load key. Exiting.")
        return
    
    print(format_key(key))

@app.command(name="import", help="Import the key formatted to base64 in the file given as argument.")
def _import(infile: str, name: str = '', desc: str = ''):
    try:
        with open(infile, 'r') as f:
            str_key = f.read()
    except Exception as e:
        print("Cannot open file : " + str(e))
        return
    
    key = to_key_object(str_key)
    if key is None:
        print("Invalid data.")
        return
    
    fgp = hash_fingerprint(format_key(key))
    nbytes = len(key["key"]) // 2
    data = {
        "name": name,
        "desc": desc,
        "date": datetime.now().strftime("%Y-%m-%d"),
        "key": key,
        "nbytes": nbytes,
        "fingerprint": fgp
    }

    if not os.path.exists(PATH):
        os.mkdir(PATH)
    
    path = PATH + fgp.upper() + ".key"

    try:
        with open(path, 'w+') as f:
            json.dump(data, f)
        
        print_key_data(path)
    except Exception as e:
        print(f"Error while writing file : {e}")

@app.command(help="Delete the key from the system.")
def delete(key: str):
    path = PATH + key + ".key"
    
    if not os.path.exists(path):
        print("Error : key does not exists.")
        return False
    
    if input("Delte this key ? This can't be undone ! (y/n) ") != 'y':
        print("Cancelled.")
        return
    
    try:
        os.remove(path)
    except Exception as e:
        print("Cannot delete key : " + str(e))

@app.command(help="Checks if the key can be loaded. Useful to check if you remember your password.")
def check(key: str, v2: bool = False):
    key = load_key(key, v2)
    if key:
        print("Key loaded successfully !")


if __name__ == "__main__":
    app()