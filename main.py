import ciphers.hill as hill
import analysis.utility as util
import numpy as np


class Terminal:
    @staticmethod
    def output(message):
        print("Output: " + message)

    @staticmethod
    def debug(message):
        print("Debug: " + message)


def read_and_prepare_text(file_path):
    plaintext = util.read_from_file(file_path)
    if plaintext:
        return util.prepare_text(plaintext)
    else:
        return None


def matrix_to_string(matrix):
    """Convert a NumPy matrix to a string with spaces separating the elements."""
    return ' '.join(map(str, matrix.flatten()))


def extract_and_trim(plaintext, start_index, desired_length, key_size):
    """Extract and trim the plaintext to ensure it contains only full blocks for the matrix."""
    block_size = key_size ** 2
    end_index = start_index + desired_length
    if end_index > len(plaintext):
        end_index = len(plaintext)

    trimmed_text = plaintext[start_index:end_index]
    # Ensure that the trimmed text contains only complete blocks
    complete_blocks = len(trimmed_text) // block_size * block_size
    return trimmed_text[:complete_blocks]


def perform_cryptanalysis(known_text, cipher_text, key_size, start_index, Terminal):
    if len(known_text) < key_size**2:
        Terminal.output("Insufficient known plaintext length for analysis.")
        return

    # Ensure the entire segment for analysis does not exceed the ciphertext length
    if start_index + len(known_text) > len(cipher_text):
        Terminal.output("Known text alignment exceeds cipher text length.")
        return

    # Extract the corresponding ciphertext segment
    cipher_segment = cipher_text[start_index:start_index + len(known_text)]

    # Performing cryptanalysis
    Terminal.output("Starting cryptanalysis...")
    valid_keys = hill.cryptanalyse(known_text, cipher_segment, key_size, Terminal.output, Terminal.debug)

    # Output results
    if valid_keys:
        for key_matrix in valid_keys:
            key_string = matrix_to_string(np.array(key_matrix))
            Terminal.output(f"Found matching key: {key_string}")
    else:
        Terminal.output("No valid keys found.")


def main():
    key_size = 2  # Size of the key matrix (e.g., 2x2)
    start_index = 0  # Example start index in the ciphertext

    # Read and prepare plaintext
    plaintext = read_and_prepare_text("texts/hobbit.txt")
    if plaintext is None:
        Terminal.output("Failed to read or prepare plaintext.")
        return

    # Extract and trim the known plaintext
    known_plaintext = extract_and_trim(plaintext, start_index, 300, key_size)
    if not known_plaintext:
        Terminal.output("Failed to extract sufficient plaintext for encryption.")
        return

    # Generate and validate a key, then encrypt the plaintext
    key_matrix = hill.generate_key(key_size)
    Terminal.output("Key Matrix: " + str(key_matrix))
    ciphertext = hill.encode(plaintext, key_matrix, Terminal.debug)
    Terminal.debug("Ciphertext generated.")

    # Perform cryptanalysis
    perform_cryptanalysis(known_plaintext, ciphertext, key_size, start_index, Terminal)


if __name__ == "__main__":
    main()
