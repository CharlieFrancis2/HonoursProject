from tabulate import tabulate
from analysis import utility as util


# --------------------------------------------------------------------------------
# ENCODE FUNCTION
# --------------------------------------------------------------------------------
def encode(plain_text, key, update_terminal_callback):
    """
    Encode plaintext using a Caesar cipher and display the encoding process.

    Args:
        plain_text (str): The text to be encoded.
        key (int): The cipher key (shift value).
        update_terminal_callback (function): Callback function to update GUI.

    Returns:
        str: The encoded ciphertext.

    This function prepares the plain text for encoding, performs the encoding
    by shifting each alphabetical character by the specified key, and displays
    the encoding process step by step using a callback. The function handles
    up to the first 10 characters for detailed display in tabular format.
    """
    # First, normalize the input text by removing non-standard characters and formatting
    plain_text = util.prepare_text(plain_text)
    cipher_text = ''

    # Initialize an empty list to hold data for visualization
    data = []
    count = 0  # Counter to limit detailed display to the first 10 characters

    # Iterate over each character in the prepared plaintext
    for i, char in enumerate(plain_text):
        if char.isalpha():  # Check if the character is an alphabetical character
            # Calculate the new character position using Caesar cipher formula
            shift_value = (ord(char) - ord('A') + key) % 26
            new_char = chr(shift_value + ord('A'))
            if count < 10:  # Append data for display if within the first 10 characters
                data.append([char, f"+{key}", new_char])
        else:
            # For non-alphabetical characters, keep them unchanged
            new_char = char
        cipher_text += new_char  # Append the new character to the output ciphertext
        count += 1  # Increment the counter

    # Generate a tabulated string of the data for visualization if available
    table_str = tabulate(data, headers=["Char", "Shift", "Result"], tablefmt="plain") if data else ""
    # Prepare the full message to be displayed including the table and a separator
    display_message = f"Encoding with key: {key}\n{table_str}\n" + "+" * 50
    # Call the provided callback function to display the encoding process in the GUI
    update_terminal_callback(display_message if table_str else "Encoding process (text too short for detailed display)")

    return cipher_text  # Return the final encoded ciphertext


# --------------------------------------------------------------------------------
# DECODE FUNCTION
# --------------------------------------------------------------------------------
def decode(cipher_text, key, update_terminal_callback):
    """
    Decode ciphertext using a Caesar cipher and display the decoding process.

    Args:
        cipher_text (str): The text to be decoded.
        key (int): The cipher key (shift value).
        update_terminal_callback (function): Callback function to update GUI.

    Returns:
        str: The decoded plaintext.

    This function prepares the cipher text for decoding, performs the decoding
    by shifting each alphabetical character backwards by the specified key, and
    displays the decoding process step by step using a callback. The function
    handles up to the first 10 characters for detailed display in tabular format.
    """
    # Normalize the input text similarly as in encoding
    cipher_text = util.prepare_text(cipher_text)
    plaintext = ''

    # Initialize an empty list for visualization data, and a counter
    data = []
    count = 0  # Counter for limiting the detailed display

    # Process each character in the normalized cipher text
    for i, char in enumerate(cipher_text):
        if char.isalpha():  # Ensure the character is alphabetical
            # Calculate the original character position using reverse Caesar cipher formula
            shift_value = (ord(char) - ord('A') - key) % 26
            new_char = chr(shift_value + ord('A'))
            if count < 10:  # Collect data for display for the first 10 characters
                data.append([char, f"-{key}", new_char])
        else:
            # Non-alphabetical characters remain unchanged
            new_char = char
        plaintext += new_char  # Build the decoded plaintext
        count += 1  # Increment the counter for detailed display

    # Create a tabulated string from the data if available
    table_str = tabulate(data, headers=["Char", "Shift", "Result"], tablefmt="plain") if data else ""
    # Prepare the full display message including the tabulated data and separators
    display_message = f"Decoding with key: {key}\n{table_str}\n" + "+" * 50
    # Use the callback to display the decoding process
    update_terminal_callback(
        display_message if table_str else "Decoding process (text too short for detailed display)")

    return plaintext  # Return the fully decoded plaintext


# --------------------------------------------------------------------------------
# CHI-SQUARE CRYPTANALYSIS FUNCTION
# --------------------------------------------------------------------------------
def chi_cryptanalysis(text, exp_letter, exp_bi, exp_tri):
    """
    Perform a Chi-Square Cryptanalysis on the given text using Caesar cipher.

    Args:
        text (str): The text to analyze.
        exp_letter (dict): Expected letter frequencies.
        exp_bi (dict): Expected bigram frequencies.
        exp_tri (dict): Expected trigram frequencies.
        update_terminal_callback (function): Callback function to update GUI.

    Returns:
        str: Summary of cryptanalysis results.

    This function analyzes the given text using Chi-Square testing to estimate
    the most likely Caesar cipher keys based on letter, bigram, and trigram
    frequency distributions. It presents the top 3 guesses based on Chi-Squared
    scores for letters.
    """
    results = []  # Initialize a list to store results for each key

    # Iterate over all possible Caesar cipher keys (0-25)
    for key in range(26):
        # Decode the text with the current key using a dummy callback to suppress output
        decoded_text = decode(text, key, lambda x: None)
        # Calculate frequency data for the decoded text
        letter_freqs, bigram_freqs, trigram_freqs = util.generate_frequency_data(decoded_text)

        # Compute Chi-Squared scores for letter, bigram, and trigram frequencies
        chi_letter = util.compute_chi_squared(letter_freqs, exp_letter, len(decoded_text))
        chi_bi = util.compute_chi_squared(bigram_freqs, exp_bi, len(decoded_text))
        chi_tri = util.compute_chi_squared(trigram_freqs, exp_tri, len(decoded_text))

        # Append the results including the key and the computed scores
        results.append((key, chi_letter, chi_bi, chi_tri, decoded_text))

    # Sort results by the Chi-Squared score for letters, ascending
    results.sort(key=lambda x: x[1])

    # Prepare the output string showing the top 3 results
    output_str = "Top 3 guesses based on Chi-Squared Letters Score:\n"
    for i in range(min(3, len(results))):  # Limit to the top 3 guesses
        key, chi_letter, chi_bi, chi_tri, decoded_text = results[i]
        # Format and append each result to the output string
        output_str += f"\nKey: {key}\nDecoded Text Preview: {decoded_text[:100]}...\n"

    return output_str  # Return the summary of cryptanalysis results
