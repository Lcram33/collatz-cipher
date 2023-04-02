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

    return b64_string.decode('utf8')

def base64_to_file(path, b64_string):
    b64_bytes = b64_string.encode('utf8')
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

@app.command(help=f"Generate a key and store it locally (under {PATH}). WITHOUT PASSWORD, IT IS STORED IN CLEAR.")
def gen(nbytes: int = 500, name: str = '', desc: str = '', password: bool = False):
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

@app.command(help="Encrypts the file with the provided key.")
def enc(key: str, infile: str, encname: bool = False, armor: bool = False):
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
        outfile = gen_noise(LATIN_LETTERS + DIGITS, '!')[:15] + '.czcenc'
        str_data = json.dumps({
            "filename": infile,
            "data": str_data
        })
    else:
        outfile = infile + '.czcenc'

    enciphered = encrypt_str(str_data, key, armor)

    try:
        with open(outfile, 'w') as f:
            f.write(enciphered)        
    except Exception as e:
        print(f"Error while writing data : {e}")

@app.command(help="Decrypts the file with the provided key.")
def dec(key: str, infile: str, armor: bool = False):
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

    deciphered = decrypt_str(str_data, key, armor)

    try:
        json_data = json.loads(deciphered)
        outfile, deciphered = json_data["filename"], json_data["data"]
    except Exception:
        outfile = infile.removesuffix(".czcenc")

    try:
        base64_to_file(outfile, deciphered)        
    except Exception as e:
        print(f"Error while writing data : {e}")

@app.command(help="Print all keys properties.")
def list():
    if not os.path.exists(PATH):
        os.mkdir(PATH)

    files = [x for x in os.listdir(PATH) if os.path.isfile(os.path.join(PATH,x))]

    for file in files:
        print_key_data(os.path.join(PATH,file))

@app.command(help="Print the key formatted to base64 so you can share it with someone. Not recommended, it is better to send a salt key file, or share a seed !")
def export(key: str):
    print("WARNING")
    print("The key will be exported IN CLEAR. Which means that anyone getting access to it will be able to decyrpt any message encrypted with it !")
    print(f"If you created the key with a password, you can safely share the file of the key : {PATH + key + '.key'}")

    if input("Do you want to export the key ? (it will be printed in the terminal) (y/n) : ") != 'y': return

    key = load_key(key)
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


if __name__ == "__main__":
    app()