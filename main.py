import time
from ciphers.vigenere import decode as vigenere_decode,  cryptanalyse as vigenere_cryptanalyse, encode as v_encode
from analysis import utility as u
import tkinter as tk

# Assume 'cipher_text' contains the encrypted text of "The Hobbit"
plain = u.read_from_file('texts/hobbit.txt')
# plain = "Hello my name is charlie"

cipher = v_encode(plain, 'abcdefg')
output_text = ''

vigenere_cryptanalyse(cipher, 15)





