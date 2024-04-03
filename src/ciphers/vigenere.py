import tkinter as tk

from tabulate import tabulate

from analysis import utility as util
from analysis.frequency_data import (
    letter_frequencies as exp_letter,
    bigram_frequencies as exp_bi,
    trigram_frequencies as exp_tri,
)
from ciphers.caesar import decode as c_decode


# --------------------------------------------------------------------------------
# ENCODING FUNCTION
# --------------------------------------------------------------------------------
def encode(plain_text, key, update_terminal_callback):
    """
    Encode a plaintext using a Vigenère cipher.

    Args:
    - plain_text (str): The text to be encoded.
    - key (str): The cipher key.
    - update_terminal_callback (function): Callback function for UI updates.

    Returns:
    - str: The encoded ciphertext.
    """
    plain_text = util.prepare_text(plain_text)

    key_index = 0
    cipher_text = ''

    for char in plain_text:
        if char.isalpha():
            shift = ord(key[key_index].upper()) - ord('A')
            new_char = chr((ord(char) - ord('A') + shift) % 26 + ord('A'))
            cipher_text += new_char
            key_index = (key_index + 1) % len(key)

    return cipher_text


# --------------------------------------------------------------------------------
# DECODING FUNCTION
# --------------------------------------------------------------------------------
def decode(cipher_text, key, update_terminal_callback):
    """
    Decode a ciphertext using a Vigenère cipher.

    Args:
    - cipher_text (str): The text to be decoded.
    - key (str): The cipher key.
    - update_terminal_callback (function): Callback function for UI updates.

    Returns:
    - str: The decoded plaintext.
    """
    cipher_text = util.prepare_text(cipher_text)

    key_index = 0
    plaintext = ""

    for char in cipher_text:
        if char.isalpha():
            shift = ord(key[key_index].upper()) - ord('A')
            new_char = chr((ord(char) - ord('A') - shift) % 26 + ord('A'))
            plaintext += new_char
            key_index = (key_index + 1) % len(key)

    return plaintext


# --------------------------------------------------------------------------------
# CRYPTANALYSIS FUNCTION
# --------------------------------------------------------------------------------
def cryptanalyse(cipher_text, max_key_length, key_guess, shift_guess, update_terminal_callback, output_text, update_status_callback):
    """
    Perform cryptanalysis on a given ciphertext with a Vigenère cipher.

    Args:
    - cipher_text (str): The ciphertext to analyze.
    - max_key_length (int): Maximum length of the key to consider.
    - update_terminal_callback (function): Callback function for terminal updates.
    - output_text (tk.Text): The Text widget to display the analysis results.
    - update_status_callback (function): Callback function for status updates.
    """
    KEY_LENGTHS_GUESSES = key_guess
    SHIFT_LENGTH_GUESSES = shift_guess
    cipher_text = util.prepare_text(cipher_text)

    def calculate_ic(column_text):
        """Calculate the Index of Coincidence (IC) for a column of text."""
        freq = [0] * 26
        for char in column_text:
            if char.isalpha():
                freq[ord(char) - ord('A')] += 1
        IC_sum = sum(f * (f - 1) for f in freq)
        return IC_sum / (len(column_text) * (len(column_text) - 1)) if len(column_text) > 1 else 0

    def create_matrix(n, text):
        """Segment the cipher text into columns based on a given key length."""
        return [text[i::n] for i in range(n)]

    import itertools

    def generate_all_possible_keys(all_stream_shifts, all_possible_keys, update_terminal_callback,
                                   update_status_callback):
        """
        Generate all possible keys from the top shift guesses for each stream.

        Modifies the all_possible_keys list in place by appending new keys.
        """
        update_terminal_callback("Generating Keyset...")
        alphabet = 'ABCDEFGHIJKLMNOPQRSTUVWXYZ'

        shift_combinations = [list(map(lambda x: x[0], stream_shifts)) for stream_shifts in all_stream_shifts]
        total_combinations = 1
        for shifts in shift_combinations:
            total_combinations *= len(shifts)

        count = 0
        for combination in itertools.product(*shift_combinations):
            update_status_callback(f"Generating: {count} keys out of: {total_combinations}")

            key = ''.join([alphabet[shift] for shift in combination])
            all_possible_keys.append(key)
            count += 1

        update_terminal_callback("Done! Generated " + str(len(all_possible_keys)) + " keys!")

    # Estimate Key Length
    update_terminal_callback("Estimating Key Length...")
    data = [[i, 0] for i in range(1, max_key_length + 1)]
    for key_length in range(1, max_key_length + 1):
        matrix = create_matrix(key_length, cipher_text)
        ic_values = [calculate_ic(column) for column in matrix]
        average_ic = sum(ic_values) / len(ic_values)
        data[key_length - 1][1] = average_ic

    sorted_data = sorted(data, key=lambda row: abs(row[1] - 0.0686))[:KEY_LENGTHS_GUESSES]
    update_terminal_callback("Done! : " + str(sorted_data[0][0]))

    # Perform frequency analysis for each stream
    all_possible_keys = []
    for key_length, _ in sorted_data:
        matrix = create_matrix(key_length, cipher_text)
        all_stream_shifts = []

        for stream_index, stream in enumerate(matrix):
            shift_scores = []
            for shift in range(26):
                decrypted_stream = c_decode(stream, shift, update_terminal_callback)
                letter_frequencies = util.generate_frequency_data(decrypted_stream)
                chi_squared = util.compute_chi_squared(letter_frequencies[0], exp_letter, len(decrypted_stream))
                shift_scores.append((shift, chi_squared))

            top_shifts = sorted(shift_scores, key=lambda x: x[1])[:SHIFT_LENGTH_GUESSES]
            all_stream_shifts.append(top_shifts)

    generate_all_possible_keys(all_stream_shifts, all_possible_keys, update_terminal_callback, update_status_callback)

    update_terminal_callback("Decoding with possible keys...")
    results = vigenere_chi_cryptanalysis(cipher_text, all_possible_keys, exp_letter, exp_bi, exp_tri,
                                         update_status_callback)

    # Now, finalize cryptanalysis by displaying results and tables for top keys
    output_str = finalize_cryptanalysis(cipher_text, results, update_terminal_callback)

    # Finally, update the GUI with the overall results
    output_text.delete("1.0", tk.END)
    output_text.insert(tk.END, output_str)


def vigenere_chi_cryptanalysis(text, all_possible_keys, exp_letter, exp_bi, exp_tri, update_status_callback):
    """
    Analyze the given text with all possible keys and calculate chi-squared scores.

    Args:
    - text (str): The text to be analyzed.
    - all_possible_keys (list): All possible keys generated from cryptanalysis.
    - exp_letter (dict), exp_bi (dict), exp_tri (dict): Expected frequency distributions.

    Returns:
    - list: Sorted list of tuples with analysis results for each key.
    """
    results = []
    total_keys = len(all_possible_keys)

    for count, key in enumerate(all_possible_keys, start=1):
        update_status_callback(f"Decoding: {count} out of: {total_keys}")
        decoded_text = decode(text, key, update_status_callback)
        letter_freqs, bigram_freqs, trigram_freqs = util.generate_frequency_data(decoded_text)

        chi_letter = util.compute_chi_squared(letter_freqs, exp_letter, len(decoded_text))
        chi_bi = util.compute_chi_squared(bigram_freqs, exp_bi, len(decoded_text))
        chi_tri = util.compute_chi_squared(trigram_freqs, exp_tri, len(decoded_text))

        results.append((key, chi_letter, chi_bi, chi_tri, decoded_text))

    results.sort(key=lambda x: x[3])
    return results


def display_vigenere_decryption_table(ciphertext, decrypted_text, key, update_terminal_callback):
    """
    Display a table showing the decryption process for the first key length + 3 characters of the Vigenère cipher.

    Args:
    - ciphertext (str): The original encrypted text.
    - decrypted_text (str): The decrypted text.
    - key (str): The key used for decryption.
    - update_terminal_callback (function): Callback function to display the message.
    """
    # Prepare the data for the table
    data = []
    key_length = len(key)
    display_length = min(len(decrypted_text), key_length + 3)

    for i in range(display_length):
        encrypted_char = ciphertext[i]
        decrypted_char = decrypted_text[i]
        key_char = key[i % key_length]
        shift = ord(key_char.upper()) - ord('A')  # Assuming uppercase key

        data.append([encrypted_char, f"-{shift}", decrypted_char])

    # Generate the table string
    table_str = tabulate(data, headers=["Encrypted Char", "Shift", "Decrypted Char"], tablefmt="outline")

    # Display the table
    display_message = f"Key: {key}\n{table_str}\n" + "+" * 50
    update_terminal_callback(display_message)


def finalize_cryptanalysis(ciphertext, results, update_terminal_callback):
    """
    Display decryption tables for the top key guesses based on the results of cryptanalysis.

    Args:
    - ciphertext (str): The original encrypted text.
    - results (list): The sorted list of tuples with analysis results for each key.
    - update_terminal_callback (function): Callback function to display messages.
    """
    output_str = "Top 3 guesses based on Chi-Squared Letters Score:\n"
    for i in range(min(3, len(results))):
        key, chi_letter, chi_bi, chi_tri, decoded_text = results[i]
        # The decryption table display should be based on each specific key found in results
        key_length = len(key)  # Determine key length for display
        display_vigenere_decryption_table(ciphertext, decoded_text[:key_length + 0], key, update_terminal_callback)
        output_str += f"\nKey: {key}\nChi-Squared Score: {chi_letter}\nDecoded Text Preview: {decoded_text[:100]}...\n"

    return output_str
