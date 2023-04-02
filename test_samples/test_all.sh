#!/bin/bash

key=DE5F047A3503634E1CF0A515115E788B1023C4A53C9EEAC267A586E444F8A3E6 # generate a key and put its fingerprint here

echo Encrypting everything...

../main.py enc $key abitoftext.txt --armor
../main.py enc $key m9sYK.jpg
../main.py enc $key bitcoin.pdf
ls -lh

echo Decrypting everything...

mv abitoftext.txt abitoftext.txt.old
mv m9sYK.jpg m9sYK.jpg.old
mv bitcoin.pdf bitcoin.pdf.old

../main.py dec $key abitoftext.txt.czcenc --armor
../main.py dec $key m9sYK.jpg.czcenc
../main.py dec $key bitcoin.pdf.czcenc

echo Check sums :

md5sum --check MD5SUMS

rm *.old *.czcenc