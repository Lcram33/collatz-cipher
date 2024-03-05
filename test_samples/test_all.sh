#!/bin/bash

# Change this with the ID of a key that you generated.
key=127AFACCAB6D493DFD2EF636665EA437931B603E583FEEB305A01C05AF66835A

echo Encrypting everything...

../main.py encf $key abitoftext.txt
../main.py encf $key m9sYK.jpg --armor
../main.py encf $key bitcoin.pdf

echo
ls -lh

echo
echo Lines :
wc -l *

echo
echo Chars :
wc -m *

echo
echo Decrypting everything...

rm abitoftext.txt m9sYK.jpg bitcoin.pdf

../main.py decf $key abitoftext.txt.czcenc
../main.py decf $key m9sYK.jpg.czcenc
../main.py decf $key bitcoin.pdf.czcenc

echo
echo Check sums :

md5sum --check MD5SUMS

rm *.czcenc