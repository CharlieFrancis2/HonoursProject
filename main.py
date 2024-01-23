from ciphers.caesar import encode as caesar_encode, decode as caesar_decode
from ciphers.vigenere import encode as vigenere_encode, decode as vigenere_decode

plain_text = 'hello my name is charlie'
key1 = 'land'
key2 = 4

# Encoding with Vigenère cipher
cipher1 = vigenere_encode(plain_text, key1)
# Encoding with Caesar cipher
cipher2 = caesar_encode(plain_text, key2)

print("Vigenere Cipher:", cipher1)
print("Caesar Cipher:", cipher2)

# Decoding with Vigenère cipher
decoded1 = vigenere_decode(cipher1, key1)
# Decoding with Caesar cipher
decoded2 = caesar_decode(cipher2, key2)

print("Decoded Vigenere:", decoded1)
print("Decoded Caesar:", decoded2)


