import typer
from collatzcipher import *
from seeded_key import *
from params import *


def file_bytes_to_bas64(path):
    with open(path, 'rb') as f:
        b64_string = base64.b64encode(f.read())

    return b64_string.decode('utf-8')

def base64_to_file(path, b64_string):
    b64_bytes = b64_string.encode('ascii')
    bytes_to_write = base64.b64decode(b64_bytes)

    with open(path, 'wb') as f:
        f.write(bytes_to_write)


app = typer.Typer()

@app.command(help="Generate a cipher key with a collatz key of 2*nbytes digits in hexadecimal. Print the key if no path provided. WARNING : overwrites the file.")
def genkey(nbytes: int = 500, path: str = ''):
    key = format_key(gen_key(nbytes))

    if path == '':
        print(key)
    else:
        try:

            with open(path, 'w') as f:
                f.write(key)

        except Exception as e:
            print(f"Error while writing file : {e}")

@app.command(help="Generate a cipher key with a seed phrase.")
def seededkey(seedphrase: str = '', nbytes: int = 500, path: str = ''):
    key = print_passphrase_and_generate(nbytes, seedphrase)

    if path == '':
        print(key)
    else:
        try:

            with open(path, 'w') as f:
                f.write(key)

        except Exception as e:
            print(f"Error while writing file : {e}")

@app.command(help="Encrypts the string with the provided key.")
def encrypt(keyfile: str, infile: str, outfile: str):
    try:
        with open(keyfile, 'r') as f:
            key = f.read()
    except Exception as e:
        print(f"Error while loading key : {e}")
    
    try:
        with open(infile, 'r') as f:
            message = f.read()
    except Exception as e:
        print(f"Error while loading message : {e}")
    
    try:
        with open(outfile, 'w') as f:
            enciphered = encrypt_str(message, to_key_object(key))
            f.write(enciphered)
    except Exception as e:
        print(f"Error while writing encrypted message : {e}")

@app.command(help="Decrypts the string with the provided key.")
def decrypt(keyfile: str, infile: str, outfile: str):
    try:
        with open(keyfile, 'r') as f:
            key = f.read()
    except Exception as e:
        print(f"Error while loading key : {e}")
    
    try:
        with open(infile, 'r') as f:
            enciphered = f.read()
    except Exception as e:
        print(f"Error while loading encrypted message : {e}")
    
    try:
        with open(outfile, 'w') as f:
            message = decrypt_str(enciphered, to_key_object(key))
            f.write(message)
    except Exception as e:
        print(f"Error while writing message : {e}")

@app.command(help="Encrypts the file with the provided key.")
def encryptfile(keyfile: str, infile: str, encrypt_name: bool = False, armor: bool = False):
    try:
        with open(keyfile, 'r') as f:
            key = f.read()
    except Exception as e:
        print(f"Error while loading key : {e}")
    
    try:
        str_data = file_bytes_to_bas64(infile)
    except Exception as e:
        print(f"Error while loading input file : {e}")

    try:   
        if encrypt_name:
            outfile = gen_noise(LATIN_LETTERS + DIGITS)[:15] + '.czcenc'
            str_data = json.dumps({
                "filename": infile,
                "data": str_data
            })
        else:
            outfile = infile + '.czcenc'

        enciphered = encrypt_str(str_data, to_key_object(key))

        if armor:
            with open(outfile, 'w') as f:
                f.write(enciphered)
        else:
            words = ['-----BEGIN COLLATTZCIPHER MESSAGE-----', '-----END COLLATTZCIPHER MESSAGE-----', '\n']
            for word in words:
                enciphered = enciphered.replace(word, '')

            base64_to_file(outfile, enciphered)
    except Exception as e:
        print(f"Error while writing data : {e}")

@app.command(help="Decrypts the file with the provided key.")
def decryptfile(input, output, key, armor: bool = True):
    print("to do")


if __name__ == "__main__":
    app()