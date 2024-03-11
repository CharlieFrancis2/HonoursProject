
import itertools
from analysis.frequency_data import (letter_frequencies as exp_letter, bigram_frequencies as exp_bi, trigram_frequencies as exp_tri)
from analysis import utility as util
from ciphers.caesar import decode as c_decode
import tkinter as tk



def encode(plain_text, key, update_terminal_callback):
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


def decode(cipher_text, key, update_terminal_callback):
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


def cryptanalyse(cipher_text, max_key_length, update_terminal_callback, output_text, update_status_callback):
    KEY_LENGTHS_GUESSES = 1
    SHIFT_LENGTH_GUESSES = 2

    cipher_text = util.prepare_text(cipher_text)

    # Function to calculate the Index of Coincidence (IC)
    def calculate_ic(column_text):
        freq = [0] * 26
        for char in column_text:
            if char.isalpha():
                freq[ord(char) - ord('A')] += 1
        IC_sum = sum(f * (f - 1) for f in freq)
        return IC_sum / (len(column_text) * (len(column_text) - 1)) if len(column_text) > 1 else 0

    # Function to segment the cipher text into columns
    def create_matrix(n, text):
        return [text[i::n] for i in range(n)]

    def generate_all_possible_keys(all_stream_shifts, all_possible_keys):
        """
        Generate all possible keys in letter format from the top 3 shift guesses for each stream.

        Args:
        - all_stream_shifts (list of lists): Each sublist contains tuples of (shift, score) for a stream.
        - all_possible_keys (list): List to append generated keys in letter format.

        This function modifies all_possible_keys in place by appending new keys to it.
        """
        # Define the alphabet for shift-to-letter conversion
        update_terminal_callback("Generating Keyset...")
        alphabet = 'ABCDEFGHIJKLMNOPQRSTUVWXYZ'

        # Extract just the shifts from each stream's top guesses
        shift_combinations = [list(map(lambda x: x[0], stream_shifts)) for stream_shifts in all_stream_shifts]

        # Generate all possible combinations of shifts
        for combination in itertools.product(*shift_combinations):
            # Convert each shift in the combination to its corresponding letter and form a key string
            key = ''.join([alphabet[shift] for shift in combination])
            all_possible_keys.append(key)  # Append each generated key in letter format to the main list

        update_terminal_callback("Done! Generated " + str(len(all_possible_keys)) + " keys!")

    # Estimate Key Length
    update_terminal_callback("Estimating Key Length...")
    data = [[i, 0] for i in range(1, max_key_length + 1)]
    for key_length in range(1, max_key_length + 1):
        matrix = create_matrix(key_length, cipher_text)
        ic_values = [calculate_ic(column) for column in matrix]
        average_ic = sum(ic_values) / len(ic_values)
        data[key_length - 1][1] = average_ic

    # -----------------------------------------------------------------------------------------------------------------
    # SORT BY IC VALUES AND CHOOSE HOW MANY TO SAVE (1)
    sorted_data = sorted(data, key=lambda row: abs(row[1] - 0.0686))[:KEY_LENGTHS_GUESSES]  # Top 3 key lengths
    update_terminal_callback("Done! : " + str(sorted_data[0][0]))
    # -----------------------------------------------------------------------------------------------------------------

    # Step 2: Detailed Frequency Analysis for Each Stream
    # loop through key lengths

    all_possible_keys = []

    for key_length, _ in sorted_data:
        matrix = create_matrix(key_length, cipher_text)
        all_stream_shifts = []  # To save top 3 shifts for each stream

        for stream_index, stream in enumerate(matrix):
            shift_scores = []
            for shift in range(26):  # Test each possible shift
                decrypted_stream = c_decode(stream, shift)
                letter_frequencies = util.generate_frequency_data(decrypted_stream)
                chi_squared = util.compute_chi_squared(letter_frequencies[0], exp_letter, len(decrypted_stream))
                # Assuming letter_frequencies[0] is correct
                shift_scores.append((shift, chi_squared))

            # ---------------------------------------------------------------------------------------------------------
            top_shifts = sorted(shift_scores, key=lambda x: x[1])[:SHIFT_LENGTH_GUESSES]
            # SAVE TOP SHIFT AMOUNTS
            # ---------------------------------------------------------------------------------------------------------
            # print(f"Stream {stream_index}: Top Shifts: {top_shifts}")  # Debugging line to check shifts
            all_stream_shifts.append(top_shifts)

    # Step 3: Use all_stream_shifts for each stream to proceed with generating key combinations in the next steps
    generate_all_possible_keys(all_stream_shifts, all_possible_keys)

    def vigenere_chi_cryptanalysis(text, all_possible_keys, exp_letter, exp_bi, exp_tri):
        results = []
        total_keys = len(all_possible_keys)

        for count, key in enumerate(all_possible_keys, start=1):
            update_status_callback(f"Decoding: {count} out of: {total_keys}")
            decoded_text = decode(text, key)  # Adjusted for Vigenère decryption
            letter_freqs, bigram_freqs, trigram_freqs = util.generate_frequency_data(decoded_text)

            chi_letter = util.compute_chi_squared(letter_freqs, exp_letter, len(decoded_text))
            chi_bi = util.compute_chi_squared(bigram_freqs, exp_bi, len(decoded_text))
            chi_tri = util.compute_chi_squared(trigram_freqs, exp_tri, len(decoded_text))

            results.append((key, chi_letter, chi_bi, chi_tri, decoded_text))

        results.sort(key=lambda x: x[3])  # Sort the results by the Chi-Squared Letters score primarily

        return results

    # Perform cryptanalysis
    results = vigenere_chi_cryptanalysis(cipher_text, all_possible_keys, exp_letter, exp_bi, exp_tri)

    # Initialize output string for Tkinter Text widget
    output_str = "Top 3 guesses based on Chi-Squared Letters Score:\n"
    for i in range(min(3, len(results))):  # Ensure not to exceed the number of results
        key, chi_letter, chi_bi, chi_tri, decoded_text = results[i]
        output_str += f"\nKey: {key}\n"
        output_str += f"Decoded Text Preview: {decoded_text[:100]}...\n"  # Preview of the decoded text

    # Clear previous output and display new results
    output_text.delete("1.0", tk.END)  # Clear existing text
    output_text.insert(tk.END, output_str)  # Insert new output string


