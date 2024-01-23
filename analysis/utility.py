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

    # Return should be outside the loop
    return freq


def compute_ic(text):
    # Calculate IC value
    IC_sum = 0
    frequency = frequency_analysis(text)
    n = sum(frequency)  # Total number of alphabetic characters

    for f in frequency:
        IC_sum += f * (f - 1)

    # Avoid division by zero
    if n > 1:
        IC = IC_sum / (n * (n - 1))
    else:
        IC = 0

    return IC
