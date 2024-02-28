# TODO: Vigenère Cipher Cryptanalysis Program Outline:
#    Step 1: Estimate Key Length
#       Calculate and save the Index of Coincidence (IC) for key lengths up to the maximum (10).
#       Identify and save the top 3 key lengths based on their closeness to the expected IC of English.
#    Step 2: Detailed Frequency Analysis for Each Stream
#       For each of the top 3 key lengths:
#            Segment the cipher text into streams by this key length.
#            For each stream:
#               Perform detailed frequency analysis.
#                 Save the top 3 shift guesses for each stream.
#   Step 3: Generate Key Combinations
#        For each key length among the top 3:
#           Generate all possible keys by combining the top 3 shift guesses for each stream.
#           This results in a large number of possible keys (3^N for each key length, where N is the key length).
#   Step 4: Decrypt and Score Each Key Combination
#       For each possible key generated in the previous step:
#          Decrypt the cipher text using this key.
#          Score the decryption using a heuristic (e.g., chi-squared test for letter frequency).
#          Optionally, further analyze the text for "English-ness" by checking for common words or patterns.
#          Save the decryption score along with the key and the decrypted text.
#   Step 5: Rank and Select Top Guesses
#         Sort all decrypted texts by their scores.
#        Select the top 5 decryptions based on these scores.
#        Present these top 5 guesses, ensuring at least one is likely correct based on the scoring.
#   Additional Considerations:
#       - Efficiency: Given the potential for a large number of combinations, focus on optimizing the scoring and
#           decryption process. Parallel processing can help manage the computational load.
#       - Scoring Heuristics: Develop robust scoring heuristics that can accurately assess the likelihood of a
#           decryption being correct. This might include a combination of statistical tests and language analysis.
#       - Iterative Refinement: If initial guesses do not yield satisfactory results, consider refining your
#           approach by adjusting the criteria for selecting top key lengths or by enhancing the scoring mechanism.

from tabulate import tabulate

from analysis import utility as util

import tkinter as tk


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


def cryptanalyse(cipher_text, max_key_length):
    cipher_text = util.prepare_text(cipher_text)

    def calculate_ic(column_text):
        freq = [0] * 26
        for char in column_text:
            if char.isalpha():
                freq[ord(char) - ord('A')] += 1

        IC_sum = sum(f * (f - 1) for f in freq)
        if len(column_text) > 1:
            return IC_sum / (len(column_text) * (len(column_text) - 1))
        else:
            return 0

    def create_matrix(n, text):
        return [text[i::n] for i in range(n)]

    data = [[i, 0] for i in range(1, max_key_length + 1)]

    for key_length in range(1, max_key_length + 1):
        matrix = create_matrix(key_length, cipher_text)
        ic_values = [calculate_ic(column) for column in matrix]
        average_ic = sum(ic_values) / len(ic_values)
        data[key_length - 1][1] = average_ic

    # Sort by IC values to find the most likely key lengths
    sorted_data = sorted(data, key=lambda row: abs(row[1] - 0.0686))

    # Display the sorted IC values
    print(tabulate(sorted_data, headers=["Key Length", "IC Value"], tablefmt="grid"))

    def chi_cryptanalysis(text, exp_letter, exp_bi, exp_tri, output_text):
        results = []

        for key in range(26):
            decoded_text = decode(text, key)
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



