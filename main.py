import ciphers.hill as hill

key = hill.generate_key(5)
print("Key: ")
print(key)

plaintext = "helloworld"
print("Plaintext: ")
print(plaintext)

ciphertext = hill.encode(plaintext, key)
print("Ciphertext: ")
print(ciphertext)

decoded_text = hill.decode(ciphertext, key)
print("Decoded Plaintext")
print(decoded_text)








