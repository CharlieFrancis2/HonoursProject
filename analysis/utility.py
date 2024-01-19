# Function to read text from a file
import os


def read_from_file(file_path):
    if not os.path.exists(file_path):
        print(f"File not found: {file_path}")
        return None
    with open(file_path, 'r') as file:
        return file.read()


def write_to_file(file_path, text):
    with open(file_path, 'w') as file:
        file.write(text)


def frequency_analysis(text):
    # Make sure cipher_text is in uppercase
    text = text.upper()
    # Create list of frequencies
    freq = [0] * 26

    # Count Frequencies
    for char in text:
        match char:
            case 'A':
                freq[0] += 1
            case 'B':
                freq[1] += 1
            case 'C':
                freq[2] += 1
            case 'D':
                freq[3] += 1
            case 'E':
                freq[4] += 1
            case 'F':
                freq[5] += 1
            case 'G':
                freq[6] += 1
            case 'H':
                freq[7] += 1
            case 'I':
                freq[8] += 1
            case 'J':
                freq[9] += 1
            case 'K':
                freq[10] += 1
            case 'L':
                freq[11] += 1
            case 'M':
                freq[12] += 1
            case 'N':
                freq[13] += 1
            case 'O':
                freq[14] += 1
            case 'P':
                freq[15] += 1
            case 'Q':
                freq[16] += 1
            case 'R':
                freq[17] += 1
            case 'S':
                freq[18] += 1
            case 'T':
                freq[19] += 1
            case 'U':
                freq[20] += 1
            case 'V':
                freq[21] += 1
            case 'W':
                freq[22] += 1
            case 'X':
                freq[23] += 1
            case 'Y':
                freq[24] += 1
            case 'Z':
                freq[25] += 1

        return freq
