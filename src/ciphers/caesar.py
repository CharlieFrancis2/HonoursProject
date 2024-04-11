import tkinter as tk
from analysis import utility as util
from tabulate import tabulate


# Define a default no-op callback function for non-GUI usage

# --------------------------------------------------------------------------------
# ENCODE FUNCTION
# --------------------------------------------------------------------------------
def encode(plain_text, key, update_terminal_callback):
    """
    Encode plaintext using a Caesar cipher and display the encoding process.

    Args:
    - plain_text (str): The text to be encoded.
    - key (int): The cipher key (shift value).
    - update_terminal_callback (function): Callback function to update GUI.

    Returns:
    - str: The encoded ciphertext.
    """
    plain_text = util.prepare_text(plain_text)
    cipher_text = ''

    # Data for the visualization table
    data = []
    count  = 0
    for i, char in enumerate(plain_text):  # Limit to first 10 characters
        if char.isalpha():
            shift_value = (ord(char) - ord('A') + key) % 26
            new_char = chr(shift_value + ord('A'))
            if count < 10:
                data.append([char, f"+{key}", new_char])
        else:
            new_char = char
        cipher_text += new_char
        count += 1

    # Display process in the terminal callback
    table_str = tabulate(data, headers=["Char", "Shift", "Result"], tablefmt="plain") if data else ""
    display_message = f"Encoding with key: {key}\n{table_str}\n" + "+" * 50
    update_terminal_callback(display_message if table_str else "Encoding process (text too short for detailed display)")

    return cipher_text


# --------------------------------------------------------------------------------
# DECODE FUNCTION
# --------------------------------------------------------------------------------
def decode(cipher_text, key, update_terminal_callback):
    """
    Decode ciphertext using a Caesar cipher and display the decoding process.

    Args:
    - cipher_text (str): The text to be decoded.
    - key (int): The cipher key (shift value).
    - update_terminal_callback (function): Callback function to update GUI.

    Returns:
    - str: The decoded plaintext.
    """
    cipher_text = util.prepare_text(cipher_text)
    plaintext = ''

    # Data for the visualization table
    data = []
    count = 0
    for i, char in enumerate(cipher_text):  # Limit to first 10 characters
        if char.isalpha():
            shift_value = (ord(char) - ord('A') - key) % 26
            new_char = chr(shift_value + ord('A'))
            if count < 10:
                data.append([char, f"-{key}", new_char])
        else:
            new_char = char
        plaintext += new_char
        count += 1

    # Display process in the terminal callback
    table_str = tabulate(data, headers=["Char", "Shift", "Result"], tablefmt="plain") if data else ""
    display_message = f"Decoding with key: {key}\n{table_str}\n" + "+" * 50
    update_terminal_callback(
        display_message if table_str else "Decoding process (text too short for detailed display)")

    return plaintext


# --------------------------------------------------------------------------------
# CHI-SQUARE CRYPTANALYSIS FUNCTION
# --------------------------------------------------------------------------------
def chi_cryptanalysis(text, exp_letter, exp_bi, exp_tri, update_terminal, output_text, update_status):
    """
    Perform a Chi-Square Cryptanalysis on the given text using Caesar cipher.

    Args:
    - text (str): The text to analyze.
    - exp_letter (dict): Expected letter frequencies.
    - exp_bi (dict): Expected bigram frequencies.
    - exp_tri (dict): Expected trigram frequencies.
    - output_text (tk.Text): The Tkinter Text widget for output.
    - update_terminal_callback (function): Callback function to update GUI.

    Results are displayed in the provided Text widget.
    """
    results = []

    for key in range(26):
        decoded_text = decode(text, key, lambda x: None)  # Use a dummy callback to suppress output
        letter_freqs, bigram_freqs, trigram_freqs = util.generate_frequency_data(decoded_text)

        chi_letter = util.compute_chi_squared(letter_freqs, exp_letter, len(decoded_text))
        chi_bi = util.compute_chi_squared(bigram_freqs, exp_bi, len(decoded_text))
        chi_tri = util.compute_chi_squared(trigram_freqs, exp_tri, len(decoded_text))

        results.append((key, chi_letter, chi_bi, chi_tri, decoded_text))

    results.sort(key=lambda x: x[1])  # Sort by Chi-Squared score

    # Prepare output string
    output_str = "Top 3 guesses based on Chi-Squared Letters Score:\n"
    for i in range(min(3, len(results))):
        key, chi_letter, chi_bi, chi_tri, decoded_text = results[i]
        output_str += f"\nKey: {key}\nDecoded Text Preview: {decoded_text[:100]}...\n"

    return output_str
