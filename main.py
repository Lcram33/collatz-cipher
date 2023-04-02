#!/bin/python3

import typer
import os
import json
import getpass
from datetime import datetime
from secure_pwd_gen_api import load_wordlist, new_passphrase
from collatzcipher import *
from seeded_key import *
from params import *


PATH = os.path.expanduser('~') + "/.collciph/"


def file_bytes_to_bas64(path):
    with open(path, 'rb') as f:
        b64_string = base64.b64encode(f.read())

    return b64_string.decode('utf-8')

def base64_to_file(path, b64_string):
    b64_bytes = b64_string.encode('ascii')
    bytes_to_write = base64.b64decode(b64_bytes)

    with open(path, 'wb') as f:
        f.write(bytes_to_write)    

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

def load_key(fgp):
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
        result = regen_key_with_seed(password, data["salt"], data["nbytes"], data["fingerprint"])
        if not result:
            print("Wrong password.")
        else:
            return result
    else:
        return data["key"]
    
    return False


app = typer.Typer()

@app.command(help="Generate a key of 2*nbytes digits in hexadecimal, and stores it locally. WITHOUT PASSWORD, IT IS STORED IN CLEAR.")
def genkey(nbytes: int = 500, name: str = '', desc: str = '', password: bool = False):
    if password:
        password = getpass.getpass(prompt="Password : ")
        result = generate_seeded_key(password, nbytes=nbytes)
        data = {
            "name": name,
            "desc": desc,
            "date": datetime.now().strftime("%Y-%m-%d"),
            "salt": result["salt"],
            "nbytes": nbytes,
            "fingerprint": result["fingerprint"]
        }
        fgp = result["fingerprint"]
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
        wordlist = load_wordlist('wordlist.json')

        number_of_words = 12
        sep = ' '
        seedphrase = new_passphrase(wordlist, number_of_words, sep)
    
        print("Seed phrase :")
        print(seedphrase)

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

@app.command(help="Encrypts the string with the provided key.")
def enc(key: str, message: str):
    key = load_key(key)
    if not key:
        print("Unable to load key. Exiting.")
        return

    print(encrypt_str(message, key))    

@app.command(help="Decrypts the string with the provided key.")
def dec(key: str, message: str):
    key = load_key(key)
    if not key:
        print("Unable to load key. Exiting.")
        return

    print(decrypt_str(message, key)) 

@app.command(help="Encrypts the file with the provided key.")
def encfile(key: str, infile: str, encname: bool = False):
    key = load_key(key)
    if not key:
        print("Unable to load key. Exiting.")
        return
    
    try:
        str_data = file_bytes_to_bas64(infile)
    except Exception as e:
        print(f"Error while loading input file : {e}")
        return

    if encname:
        outfile = gen_noise(LATIN_LETTERS + DIGITS)[:15] + '.czcenc'
        str_data = json.dumps({
            "filename": infile,
            "data": str_data
        })
    else:
        outfile = infile + '.czcenc'

    enciphered = encrypt_str(str_data, key)

    try:
        with open(outfile, 'w') as f:
            f.write(enciphered)        
    except Exception as e:
        print(f"Error while writing data : {e}")

@app.command(help="Decrypts the file with the provided key.")
def decfile(key: str, infile: str):
    key = load_key(key)
    if not key:
        print("Unable to load key. Exiting.")
        return
    
    try:
        with open(infile, 'r') as f:
            str_data = f.read()
    except Exception as e:
        print(f"Error while loading input file : {e}")
        return

    deciphered = decrypt_str(str_data, key)

    try:
        json_data = json.loads(deciphered)
        outfile, deciphered = json_data["filename"], json_data["data"]
    except Exception:
        outfile = infile.removesuffix(".czcenc")

    try:
        with open(outfile, 'w') as f:
            base64_to_file(outfile, deciphered)        
    except Exception as e:
        print(f"Error while writing data : {e}")

@app.command(help="Displays all keys properties.")
def l():
    """
    List keys.
    """

    if not os.path.exists(PATH):
        os.mkdir(PATH)

    files = [x for x in os.listdir(PATH) if os.path.isfile(os.path.join(PATH,x))]

    for file in files:
        print_key_data(os.path.join(PATH,file))

@app.command(help="print the key formatted to base64 so you can share it with someone. Not recommended, it is better to send a salt key file !")
def export(key: str):
    key = load_key(key)
    if not key:
        print("Unable to load key. Exiting.")
        return
    
    print(format_key(key))


if __name__ == "__main__":
    app()