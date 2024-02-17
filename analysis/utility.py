# Function to read text from a file
import os
import string


def read_from_file(file_path):
    if not os.path.exists(file_path):
        print(f"File not found: {file_path}")
        return None
    with open(file_path, 'r') as file:
        return file.read()


def write_to_file(file_path, text):
    with open(file_path, 'w') as file:
        file.write(text)


def prepare_text(text):
    # Remove punctuation
    text = text.translate(str.maketrans('', '', string.punctuation))
    # Capitalize everything
    text = text.upper()
    return text


def frequency_analysis(text):
    # Make sure text is in uppercase
    text = prepare_text(text)
    # Create list of frequencies
    freq = [0] * 26
    # Count Frequencies
    for char in text:
        if char.isalpha():
            index = ord(char) - ord('A')
            freq[index] += 1
    # Return the frequencies
    return freq


def compute_ic(text):
    freq = frequency_analysis(text)
    n = sum(freq)  # Total number of alphabetic characters for accurate IC calculation

    # Calculate IC value
    IC_sum = 0

    for f in freq:
        IC_sum = IC_sum + (f * (f - 1))

    # Avoid division by zero
    if n > 1:
        IC = IC_sum / (n * (n - 1))
    else:
        IC = 0

    return IC

    # # Calculate IC value
    # IC_sum = 0
    #
    # for f in freq:
    #     IC_sum = IC_sum + (f * (f - 1))
    #
    # IC = IC_sum / (len(column_text) * (len(column_text) - 1))
    #
    # return IC


def gcd(a, b):
    while b:
        a, b = b, a % b
    return a


def mod_inverse(a, m):
    # Find modular inverse of a under modulo m, assuming m is prime
    # This function is used to check if the determinant has an inverse modulo 26
    # a and m are coprime if gcd(a, m) = 1
    if gcd(a, m) != 1:
        return None  # No mod inverse if a and m are not coprime
    else:
        return pow(a, -1, m)