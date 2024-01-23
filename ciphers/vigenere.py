from analysis import utility as util


def encode(plain_text, key):
    # Convert to uppercase and remove leading/trailing whitespaces
    plain_text = util.prepare_text(plain_text)

    key_index = 0
    cipher_text = ''

    for char in plain_text:
        # Check if the character is an alphabet letter
        if char.isalpha():
            # Calculate the shift based on the key character and handle wrap-around
            # Convert the key character from 'A'-'Z' to 0-25
            shift = ord(key[key_index].upper()) - ord('A')
            new_char = chr((ord(char) - ord('A') + shift) % 26 + ord('A'))
            cipher_text += new_char

            # Update the key index to use the next key character
            key_index = (key_index + 1) % len(key)
        # Skip over spaces and non-alphabetic characters
        else:
            continue

    return cipher_text


def decode(cipher_text, key):
    # Convert to uppercase and remove leading/trailing whitespaces
    cipher_text = util.prepare_text(cipher_text)

    key_index = 0
    plaintext = ""

    for char in cipher_text:
        # Check if the character is an alphabet letter
        if char.isalpha():
            # Calculate the shift based on the key character and handle wrap-around
            # Convert the key character from 'A'-'Z' to 0-25
            shift = ord(key[key_index].upper()) - ord('A')
            new_char = chr((ord(char) - ord('A') - shift) % 26 + ord('A'))
            plaintext += new_char

            # Update the key index to use the next key character
            key_index = (key_index + 1) % len(key)
        else:
            pass

    return plaintext
