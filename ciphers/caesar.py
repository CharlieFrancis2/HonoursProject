from analysis import utility as util
import pandas as pd


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
            cipher_text += char

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


def chi_cryptanalysis(text, exp_letter, exp_bi, exp_tri):
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

    # Print top 5 guesses along with their decoded texts
    print("Top 5 guesses based on Chi-Squared Letters Score:")
    for i in range(min(5, len(results))):  # Ensure not to exceed the number of results
        key, chi_letter, chi_bi, chi_tri, decoded_text = results[i]
        print(f"\nKey: {key}, Chi-Squared Letter: {chi_letter}, Chi-Squared Bigrams: {chi_bi}, Chi-Squared Trigrams: {chi_tri}")
        print(f"Decoded Text Preview: {decoded_text[:100]}...")  # Preview of the decoded text