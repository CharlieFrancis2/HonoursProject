from analysis import utility as util
import tkinter as tk
from tabulate import tabulate

from tabulate import tabulate


def encode(plain_text, key, update_terminal_callback):
    # Convert to uppercase and remove leading/trailing whitespaces
    plain_text = util.prepare_text(plain_text)
    cipher_text = ''

    # Prepare data for the table, limited to first 10 characters
    data = []
    for i, char in enumerate(plain_text):
        if char.isalpha():
            shift_value = (ord(char) - ord('A') + key) % 26
            new_char = chr(shift_value + ord('A'))
        else:
            new_char = char

        cipher_text += new_char

        # Add to table only if within the first 10 characters
        if i < 10:
            if char.isalpha():
                data.append([char, f"+{key}", new_char])
            else:
                data.append([char, "-", char])

    # Generate table string using 'plain' format for better alignment, but only for the first 10 characters
    if data:  # Check if there's anything to display (in case the text is very short)
        table_str = tabulate(data, headers=["Char", "Shift", "Result"], tablefmt="plain")
        display_message = f"Encoding with key: {key}\n{table_str}"
    else:
        display_message = "Encoding process (text too short for detailed display)"

    # Send the display message to the GUI
    update_terminal_callback(display_message)

    # Return the full encoded text
    return cipher_text


def decode(cipher_text, key, update_terminal_callback):
    # Convert to uppercase and remove leading/trailing whitespaces
    cipher_text = util.prepare_text(cipher_text)
    plaintext = ''

    # Prepare data for the table, limited to first 10 characters
    data = []
    for i, char in enumerate(cipher_text):
        if char.isalpha():
            shift_value = (ord(char) - ord('A') - key) % 26
            new_char = chr(shift_value + ord('A'))
        else:
            new_char = char

        plaintext += new_char

        # Add to table only if within the first 10 characters
        if i < 10:
            if char.isalpha():
                data.append([char, f"-{key}", new_char])
            else:
                data.append([char, "-", char])

    # Generate table string using 'plain' format for better alignment, but only for the first 10 characters
    if data:  # Check if there's anything to display (in case the text is very short)
        table_str = tabulate(data, headers=["Char", "Shift", "Result"], tablefmt="plain")
        display_message = f"Decoding with key: {key}\n{table_str}"
    else:
        display_message = "Decoding process (text too short for detailed display)"

    # Send the display message to the GUI
    update_terminal_callback(display_message)

    # Return the full decoded text
    return plaintext


def chi_cryptanalysis(text, exp_letter, exp_bi, exp_tri, output_text, update_terminal_callback):
    results = []

    for key in range(26):
        decoded_text = decode(text, key, update_terminal_callback)
        letter_freqs, bigram_freqs, trigram_freqs = util.generate_frequency_data(decoded_text)

        chi_letter = util.compute_chi_squared(letter_freqs, exp_letter, len(decoded_text))
        chi_bi = util.compute_chi_squared(bigram_freqs, exp_bi, len(decoded_text))
        chi_tri = util.compute_chi_squared(trigram_freqs, exp_tri, len(decoded_text))

        # Append results, including decoded text for later reference
        results.append((key, chi_letter, chi_bi, chi_tri, decoded_text))

    # Sort the results by the Chi-Squared Letters score primarily
    results.sort(key=lambda x: x[1])

    # Initialize output string for Tkinter Text widget
    output_str = "Top 3 guesses based on Chi-Squared Letters Score:\n"
    for i in range(min(3, len(results))):  # Ensure not to exceed the number of results
        key, chi_letter, chi_bi, chi_tri, decoded_text = results[i]
        output_str += f"\nKey: {key}\n"
        output_str += f"Decoded Text Preview: {decoded_text[:100]}...\n"  # Preview of the decoded text

    # Clear previous output and display new results
    output_text.delete("1.0", tk.END)  # Clear existing text
    output_text.insert(tk.END, output_str)  # Insert new output string
