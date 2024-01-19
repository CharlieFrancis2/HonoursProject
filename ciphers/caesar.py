def encode(plain_text, shift):
    # Convert to lowercase and remove leading/trailing whitespaces
    plain_text = plain_text.lower().strip()
    cipher_text = ""

    for char in plain_text:
        # Check if the character is an alphabet letter
        if char.isalpha():
            # Shift the character and handle wrap-around
            new_char = chr((ord(char) - ord('a') + shift) % 26 + ord('a'))
            cipher_text += new_char
        else:
            # If it's not an alphabet letter skip over it
            pass

    return cipher_text


def decode(cipher_text, shift):
    # Convert to lowercase and remove leading/trailing whitespaces
    cipher_text = cipher_text.lower().strip()
    plaintext = ""

    for char in cipher_text:
        # Check if the character is an alphabet letter
        if char.isalpha():
            # Shift the character and handle wrap-around
            new_char = chr((ord(char) - ord('a') - shift) % 26 + ord('a'))
            plaintext += new_char
        else:
            # If it's not an alphabet letter skip over it
            plaintext += char

    return plaintext
