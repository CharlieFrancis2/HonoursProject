import itertools
import tkinter as tk
from tabulate import tabulate
from functools import reduce
import operator

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
    Encode plaintext using a Vigenère cipher.
    This involves repeating the key to match the length of the plaintext,
    and shifting each letter of the plaintext by the corresponding letter in the key.

    Args:
        plain_text (str): The text to be encoded.
        key (str): The cipher key.
        update_terminal_callback (function): Callback function for UI updates.

    Returns:
        str: The encoded ciphertext.
    """
    # Prepare the plaintext by removing non-alphabetic characters and converting to uppercase
    plain_text = util.prepare_text(plain_text)
    cipher_text = ''  # Initialize the output variable for the encoded text
    key_index = 0  # Initialize key index to cycle through each character of the key

    for char in plain_text:
        if char.isalpha():  # Process only alphabetic characters
            # Calculate the shift amount from the current character in the key
            shift = ord(key[key_index].upper()) - ord('A')
            # Shift the plaintext character within the bounds of uppercase English letters
            new_char = chr((ord(char) - ord('A') + shift) % 26 + ord('A'))
            cipher_text += new_char  # Append the shifted character to the output ciphertext
            key_index = (key_index + 1) % len(
                key)  # Move to the next character in the key, wrapping around if necessary

    return cipher_text  # Return the fully encoded text


# --------------------------------------------------------------------------------
# DECODING FUNCTION
# --------------------------------------------------------------------------------
def decode(cipher_text, key, update_terminal_callback):
    """
    Decode ciphertext using a Vigenère cipher.
    This reverses the encoding process by using the negative shift associated with each letter of the key.

    Args:
        cipher_text (str): The text to be decoded.
        key (str): The cipher key.
        update_terminal_callback (function): Callback function for UI updates.

    Returns:
        str: The decoded plaintext.
    """
    # Prepare the ciphertext for decoding
    cipher_text = util.prepare_text(cipher_text)
    plaintext = ''  # Initialize the output variable for the decoded text
    key_index = 0  # Initialize key index to cycle through each character of the key

    for char in cipher_text:
        if char.isalpha():  # Process only alphabetic characters
            # Calculate the negative shift amount from the current character in the key
            shift = ord(key[key_index].upper()) - ord('A')
            # Reverse the shift applied during encryption
            new_char = chr((ord(char) - ord('A') - shift) % 26 + ord('A'))
            plaintext += new_char  # Append the reversed character to the output plaintext
            key_index = (key_index + 1) % len(
                key)  # Move to the next character in the key, wrapping around if necessary

    return plaintext  # Return the fully decoded text


# --------------------------------------------------------------------------------
# CRYPTANALYSIS FUNCTION
# --------------------------------------------------------------------------------
def cryptanalyse(cipher_text, max_key_length, key_guess, shift_guess, update_terminal_callback, output_text,
                 update_status_callback):
    """
    Perform cryptanalysis on a given ciphertext using a Vigenère cipher.
    This involves estimating the key length and possible keys to attempt decrypting the ciphertext.

    Args:
        cipher_text (str): The ciphertext to analyze.
        max_key_length (int): Maximum length of the key to consider.
        key_guess (int): Number of key length guesses to try.
        shift_guess (int): Number of shift guesses per key length.
        update_terminal_callback (function): Callback function for terminal updates.
        output_text (tk.Text): The Text widget to display the analysis results.
        update_status_callback (function): Callback function for status updates.
    """
    # Prepare the ciphertext by normalizing it
    cipher_text = util.prepare_text(cipher_text)

    # Function to calculate the Index of Coincidence (IC) for a column of text
    def calculate_ic(column_text):
        freq = [0] * 26  # Frequency array for each letter A-Z
        for char in column_text:
            if char.isalpha():
                freq[ord(char) - ord('A')] += 1
        # Compute the IC using the formula IC = Σ(ni(ni-1)) / (N(N-1))
        IC_sum = sum(f * (f - 1) for f in freq)
        return IC_sum / (len(column_text) * (len(column_text) - 1)) if len(column_text) > 1 else 0

    # Function to create a matrix of text columns based on the assumed key length
    def create_matrix(n, text):
        return [text[i::n] for i in range(n)]

    # Function to generate all possible keys from the shift combinations found in cryptanalysis
    def generate_all_possible_keys(all_stream_shifts, all_possible_keys, update_terminal_callback,
                                   update_status_callback):
        update_terminal_callback("Generating a Keyset...")
        alphabet = 'ABCDEFGHIJKLMNOPQRSTUVWXYZ'
        shift_combinations = [list(map(lambda x: x[0], stream_shifts)) for stream_shifts in all_stream_shifts]
        total_combinations = reduce(operator.mul, [len(shifts) for shifts in shift_combinations], 1)
        update_status_callback(f"Total Combinations: {total_combinations}")

        for count, combination in enumerate(itertools.product(*shift_combinations)):
            key = ''.join(alphabet[shift] for shift in combination)
            all_possible_keys.append(key)
            if count % 1000 == 0:
                update_status_callback(f"Generated {count} of {total_combinations} keys")
        update_terminal_callback("Done! Generated all possible keys for this key length.")

    # Estimate the most likely key lengths based on the Index of Coincidence
    update_terminal_callback("Estimating Key Length...")
    data = [[i, 0] for i in range(1, max_key_length + 1)]
    for key_length in range(1, max_key_length + 1):
        matrix = create_matrix(key_length, cipher_text)
        ic_values = [calculate_ic(column) for column in matrix]
        average_ic = sum(ic_values) / len(ic_values) if ic_values else 0
        data[key_length - 1][1] = average_ic

    sorted_data = sorted(data, key=lambda row: abs(row[1] - 0.0686))[:key_guess]
    update_terminal_callback("Key Length Estimation Complete")
    table_str = tabulate(sorted_data, headers=["Key Length", "IC Value"], tablefmt="outline")
    update_terminal_callback(table_str)

    # Analyze each key length guess to find possible shifts for each stream of characters
    all_possible_keys = []
    for key_length, _ in sorted_data:
        matrix = create_matrix(key_length, cipher_text)
        all_stream_shifts = []
        for stream_index, stream in enumerate(matrix):
            shift_scores = []
            for shift in range(26):
                decrypted_stream = c_decode(stream, shift, lambda x: None)  # Decode using each possible shift
                letter_frequencies = util.generate_frequency_data(decrypted_stream)
                chi_squared = util.compute_chi_squared(letter_frequencies[0], exp_letter, len(decrypted_stream))
                shift_scores.append((shift, chi_squared))
            top_shifts = sorted(shift_scores, key=lambda x: x[1])[:shift_guess]
            all_stream_shifts.append(top_shifts)

        generate_all_possible_keys(all_stream_shifts, all_possible_keys, update_terminal_callback,
                                   update_status_callback)

    update_terminal_callback(f"Generated {len(all_possible_keys)} keys!")

    # Use the possible keys to attempt decrypting the ciphertext and analyze results
    results = vigenere_chi_cryptanalysis(cipher_text, all_possible_keys, exp_letter, exp_bi, exp_tri,
                                         update_status_callback)

    # Display results and final decryption tables for top key guesses
    return finalize_cryptanalysis(cipher_text, results, update_terminal_callback)


def vigenere_chi_cryptanalysis(text, all_possible_keys, exp_letter, exp_bi, exp_tri, update_status_callback):
    """
    Perform a detailed chi-squared analysis of the given text with all possible keys generated.
    This method assesses how closely the decoded text for each key matches the expected frequency distributions.

    Args:
        text (str): The ciphertext to be analyzed.
        all_possible_keys (list): List of all possible decryption keys.
        exp_letter (dict), exp_bi (dict), exp_tri (dict): Expected frequency distributions for letters, bigrams, and trigrams.
        update_status_callback (function): Callback to update status in the UI.

    Returns:
        list: A sorted list containing tuples of (key, chi-squared scores, decoded text) ranked by chi-squared values.
    """
    results = []
    total_keys = len(all_possible_keys)  # Total number of keys to analyze

    for count, key in enumerate(all_possible_keys, start=1):
        update_status_callback(f"Decoding: {count} of {total_keys}")  # Update the UI with progress
        decoded_text = decode(text, key,
                              lambda x: None)  # Decode the text using the current key without updating the terminal
        # Generate frequency data for the decoded text
        letter_freqs, bigram_freqs, trigram_freqs = util.generate_frequency_data(decoded_text)

        # Calculate chi-squared values for letters, bigrams, and trigrams
        chi_letter = util.compute_chi_squared(letter_freqs, exp_letter, len(decoded_text))
        chi_bi = util.compute_chi_squared(bigram_freqs, exp_bi, len(decoded_text))
        chi_tri = util.compute_chi_squared(trigram_freqs, exp_tri, len(decoded_text))

        # Store the results along with the key and decoded text
        results.append((key, chi_letter, chi_bi, chi_tri, decoded_text))

    # Sort the results by the chi-squared score for trigrams, which generally gives a good measure of text structure
    results.sort(key=lambda x: x[3])
    return results  # Return the sorted results


def display_vigenere_decryption_table(ciphertext, decrypted_text, key, update_terminal_callback):
    """
    Display a detailed table showing the decryption process using a specific key, character by character.

    Args:
        ciphertext (str): The original encrypted text.
        decrypted_text (str): The decrypted text based on the chosen key.
        key (str): The decryption key used.
        update_terminal_callback (function): Callback to update the terminal with the decryption table.

    This function displays a detailed side-by-side comparison of ciphertext characters, the shift used,
    and the resulting plaintext characters.
    """
    # Prepare data for the table showing a few characters from the decryption process
    data = []
    key_length = len(key)  # Length of the decryption key
    display_length = min(len(decrypted_text), key_length + 3)  # Limit the display to key length plus a few characters

    for i in range(display_length):
        encrypted_char = ciphertext[i]  # Encrypted character
        decrypted_char = decrypted_text[i]  # Decrypted character
        key_char = key[i % key_length]  # Current key character (cycled through the key)
        shift = ord(key_char.upper()) - ord('A')  # Calculate shift used for this character

        data.append([encrypted_char, f"-{shift}", decrypted_char])  # Append the comparison to the data list

    # Create a tabulated string of the data
    table_str = tabulate(data, headers=["Encrypted Char", "Shift", "Decrypted Char"], tablefmt="outline")

    # Formulate the complete message to display
    display_message = f"Key: {key}\n{table_str}\n" + "+" * 50
    update_terminal_callback(display_message)  # Update the terminal with the decryption table


def finalize_cryptanalysis(ciphertext, results, update_terminal_callback):
    """
    Finalize the cryptanalysis process by displaying the results for the best decryption keys.

    Args:
        ciphertext (str): The original encrypted text.
        results (list): Sorted list of analysis results, including keys and their respective chi-squared scores.
        update_terminal_callback (function): Callback to display the final cryptanalysis results.

    This function displays the top three decryption results based on the chi-squared analysis.
    """
    output_str = "Top 3 guesses based on Chi-Squared Letters Score:\n"
    # Iterate over the top three results (or fewer if less available)
    for i in range(min(3, len(results))):
        key, chi_letter, chi_bi, chi_tri, decoded_text = results[i]
        display_vigenere_decryption_table(ciphertext, decoded_text[:len(key) + 0], key,
                                          update_terminal_callback)  # Display the decryption table for each key
        # Append the results to the output string for display
        output_str += f"\nKey: {key}\nChi-Squared Score: {chi_letter}\nDecoded Text Preview: {decoded_text[:100]}...\n"

    return output_str  # Return the formatted output string with the top guesses
