import ciphers.caesar as caesar

plain_text = str(input("What is your plaintext that you'd like to encode?"))
shift = int(input("What shift value would you like?"))

print(plain_text)
print("Encoded text:")
ciphertext = caesar.encode(plain_text, shift)
print(ciphertext)
print("Decoded text:")
print(caesar.decode(ciphertext, shift))