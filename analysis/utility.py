import os
import string


def read_from_file(file_path):
    """
    Reads and returns the content of a text file.

    Args:
        file_path (str): The path to the file to be read.

    Returns:
        str: The content of the file as a string. Returns None if the file does not exist.

    This function checks if the specified file exists using os.path.exists.
    If the file exists, it opens the file in read mode with UTF-8 encoding to ensure proper handling of special characters,
    reads the file content, then returns the content as a string.
    """
    if not os.path.exists(file_path):
        print(f"File not found: {file_path}")
        return None
    with open(file_path, 'r', encoding='utf-8') as file:
        return file.read()


def write_to_file(file_path, text):
    """
    Writes given text to a file specified by file_path.

    Args:
        file_path (str): The path to the file where the text will be written.
        text (str): The text to be written to the file.

    This function opens the specified file in write mode and writes the provided text to the file.
    If the file does not exist, it will be created.
    """
    with open(file_path, 'w') as file:
        file.write(text)


def prepare_text(text):
    """
    Prepares text by replacing special characters, removing punctuation, and converting to uppercase.

    Args:
        text (str): The input text to be processed.

    Returns:
        str: The processed text with special characters replaced, punctuation removed, and converted to uppercase.

    This function first replaces special characters like smart quotes with their ASCII equivalents.
    Then, it removes all punctuation characters using a translation table created with str.maketrans.
    Finally, it converts all characters in the text to uppercase.
    """
    # Define a translation table to replace smart quotes and other special characters.
    special_chars = {
        ord('‘'): "'", ord('’'): "'",  # Smart single quotes
        ord('“'): '"', ord('”'): '"',  # Smart double quotes
        ord('—'): '-',  # Em dash
        ord('…'): '...',  # Ellipsis
    }
    text = text.translate(special_chars)
    text = text.translate(str.maketrans('', '', string.punctuation))
    text = text.upper()
    return text


def frequency_analysis(text):
    """
    Performs frequency analysis on the text, counting the occurrence of each alphabetic character.

    Args:
        text (str): The input text to analyze.

    Returns:
        list: A list of 26 integers representing the frequency of each letter (A-Z) in the text.

    This function prepares the text by removing non-alphabetic characters and converting to uppercase,
    then counts the frequency of each letter in the text, storing the counts in a list of length 26.
    """
    text = prepare_text(text)
    freq = [0] * 26
    for char in text:
        if char.isalpha():
            index = ord(char) - ord('A')
            freq[index] += 1
    return freq


def compute_ic(text):
    """
    Computes the Index of Coincidence (IC) of the given text.

    Args:
        text (str): The input text for which to calculate the IC.

    Returns:
        float: The Index of Coincidence of the text.

    This function calculates the IC based on the frequency of each letter in the text,
    which is a measure used in cryptanalysis to determine the likelihood of certain cryptographic properties.
    """
    freq = frequency_analysis(text)
    n = sum(freq)
    IC_sum = sum(f * (f - 1) for f in freq)
    IC = IC_sum / (n * (n - 1)) if n > 1 else 0
    return IC


def gcd(a, b):
    """
    Computes the greatest common divisor (GCD) of two numbers using Euclid's algorithm.

    Args:
        a (int): The first number.
        b (int): The second number.

    Returns:
        int: The GCD of a and b.
    """
    while b:
        a, b = b, a % b
    return a


def mod_inverse(a, m):
    """
    Finds the modular inverse of a under modulo m.

    Args:
        a (int): The number to find the modular inverse for.
        m (int): The modulus.

    Returns:
        int or None: The modular inverse of a under modulo m if it exists, otherwise None.

    This function is particularly useful in cryptographic algorithms where the need to find an inverse under a modular operation arises.
    """
    if gcd(a, m) != 1:
        return None  # No mod inverse if a and m are not coprime
    else:
        return pow(a, -1, m)


def most_common_character(text):
    """
    Identifies the most common character in the text after processing.

    Args:
        text (str): The input text to analyze.

    Returns:
        str: The most common character in the processed text.

    This function performs a frequency analysis on the prepared text to find the most frequently occurring alphabetic character.
    """
    text = prepare_text(text)
    chars = frequency_analysis(text)
    most_common = [0] * 10
    for i in range(10):
        highest_index = chars.index(max(chars))
        chars.remove(max(chars))
        most_common[i] = chr(ord('A') + highest_index)

    return most_common


def generate_frequency_data(text):
    text = prepare_text(text)  # Normalize text

    # Initialize counters
    letter_counts = {letter: 0 for letter in string.ascii_uppercase}
    bigram_counts = {}
    trigram_counts = {}

    # Count letters
    for letter in text:
        if letter in letter_counts:
            letter_counts[letter] += 1

    # Count bigrams
    for i in range(len(text) - 1):
        bigram = text[i:i + 2]
        if bigram.isalpha():
            bigram_counts[bigram] = bigram_counts.get(bigram, 0) + 1

    # Count trigrams
    for i in range(len(text) - 2):
        trigram = text[i:i + 3]
        if trigram.isalpha():
            trigram_counts[trigram] = trigram_counts.get(trigram, 0) + 1

    # Convert counts to frequencies
    total_letters = sum(letter_counts.values())
    letter_frequencies = {letter: (count / total_letters) * 100 for letter, count in letter_counts.items()}

    total_bigrams = sum(bigram_counts.values())
    bigram_frequencies = {bigram: (count / total_bigrams) * 100 for bigram, count in bigram_counts.items()}

    total_trigrams = sum(trigram_counts.values())
    trigram_frequencies = {trigram: (count / total_trigrams) * 100 for trigram, count in trigram_counts.items()}

    return letter_frequencies, bigram_frequencies, trigram_frequencies


def compute_chi_squared(observed, expected, text_length):
    chi_squared = 0
    for key in expected:
        observed_freq = observed.get(key, 0)
        expected_freq = expected[key] * text_length / 100  # Convert expected percentage to count
        chi_squared += ((observed_freq - expected_freq) ** 2) / expected_freq if expected_freq > 0 else 0

    # Normalize by text length
    normalized_chi_squared = chi_squared / text_length
    return normalized_chi_squared

