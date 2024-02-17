from tabulate import tabulate

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


def cryptanalyse(text):
    english_ic = 0.0686
    data = []
    for i in range(26):
        decoded_text = decode(text, i)
        ic_value = util.compute_ic(decoded_text)
        data.append((i, ic_value))  # Store the shift and its IC value as a tuple

    # Sort by IC values and print table
    sorted_matrix = sorted(data, key=lambda row: abs(row[1] - english_ic))
    headers = ["Shift Amount", "IC Value"]
    table = tabulate(sorted_matrix, headers, tablefmt="grid")
    print(table)