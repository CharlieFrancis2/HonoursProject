from analysis import utility as util


def encode(plain_text, key):
    # Convert to uppercase and remove leading/trailing whitespaces
    plain_text = util.prepare_text(plain_text)
    cipher_text = ''

    for char in plain_text:
        # Check if the character is an alphabet letter
        if char.isalpha():
            # Shift the character and handle wrap-around
            new_char = chr((ord(char) - ord('A') + key) % 26 + ord('A'))
            cipher_text += new_char
        # Skip over spaces and non-alphabetic characters
        else:
            continue

    return cipher_text


def decode(cipher_text, key):
    # Convert to uppercase and remove leading/trailing whitespaces
    cipher_text = util.prepare_text(cipher_text)
    plaintext = ""

    for char in cipher_text:
        # Check if the character is an alphabet letter
        if char.isalpha():
            # Shift the character back and handle wrap-around
            new_char = chr((ord(char) - ord('A') - key) % 26 + ord('A'))
            plaintext += new_char
        else:
            # If it's not an alphabet letter skip over it
            plaintext += char

    return plaintext

