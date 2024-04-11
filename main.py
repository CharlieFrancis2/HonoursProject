import ciphers.hill as hill
import analysis.utility as util
import numpy as np
import ciphers.hill as hill


class Terminal:
    @staticmethod
    def output(message):
        print("Output: " + message)

    @staticmethod
    def debug(message):
        print("Debug: " + message)


def main():
    key_size = 2  # Size of the key matrix (e.g., 2x2)
    start_index = 0  # Example start index in the ciphertext

    # Read and prepare plaintext
    plaintext = hill.read_and_prepare_text("texts/hobbit.txt")
    if plaintext is None:
        Terminal.output("Failed to read or prepare plaintext.")
        return

    # Extract and trim the known plaintext
    known_plaintext = hill.extract_and_trim(plaintext, start_index, key_size)
    if not known_plaintext:
        Terminal.output("Failed to extract sufficient plaintext for encryption.")
        return

    # Generate and validate a key, then encrypt the plaintext
    key_matrix = hill.generate_key(key_size)
    Terminal.output("Key Matrix: " + str(key_matrix))
    ciphertext = hill.encode(plaintext, key_matrix, Terminal.debug)
    Terminal.debug("Ciphertext generated.")

    # Perform cryptanalysis
    hill.cryptanalyse(known_plaintext, ciphertext, key_size, start_index, Terminal.output, Terminal.debug)


if __name__ == "__main__":
    main()
