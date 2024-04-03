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


def keys_are_equal(key_matrix_1, key_matrix_2):
    return np.array_equal(key_matrix_1, key_matrix_2)


def matrix_to_string(matrix):
    """Convert a NumPy matrix to a string with spaces separating the elements."""
    return ' '.join(map(str, matrix.flatten()))


def retranspose_key(key_matrix, position, block_size):
    """Re-transpose the key matrix based on its start position and block size."""
    # This is a placeholder function. You'll need to implement the logic
    # that correctly retransposes the key based on your specific requirements.
    # The following line is just a placeholder and likely doesn't reflect the
    # actual logic you need.
    return np.transpose(key_matrix)  # Adjust this to match your transposition logic


# Updated perform_cryptanalysis function to include the new logic
def perform_cryptanalysis(known_text, cipher_text, key_size, original_key_matrix):
    valid_keys = hill.cryptanalyse(known_text, cipher_text, key_size, Terminal.output, Terminal.debug)

    # Convert the original key matrix to a string for comparison
    original_key_string = matrix_to_string(original_key_matrix)

    found_keys = []

    for key_matrix, position in valid_keys:
        # Re-transpose the found key matrix based on its start position and block size
        retransposed_key_matrix = retranspose_key(np.array(key_matrix), position, key_size)

        #  TODO: Switch comparison to comparing decoded ciphertext to known plaintext
        #   -------------------------------------------------------------------------
        #
        # Convert the re-transposed key matrix to a string for comparison
        retransposed_key_string = matrix_to_string(retransposed_key_matrix)

        if retransposed_key_string == original_key_string:
            Terminal.output(f"Found matching key at position {position}. Key: {retransposed_key_matrix}")
            found_keys.append([retransposed_key_string, position])
        else:
            Terminal.output(f"Key at position {position} does not match the original. Key: {retransposed_key_string}")

    print(f"Found matching key at position {found_keys[0][1]}. Key: {found_keys[0][0]}")



def main():
    key_size = 2

    # Generate and validate key
    key = hill.generate_key(key_size)
    valid, key_matrix = util.validate_and_convert_hill_key(key)
    Terminal.debug("Generated Key: " + str(key_matrix))
    if not valid:
        Terminal.output("Key validation failed.")
        return

    # Read and prepare plaintext
    plaintext = read_and_prepare_text("texts/hobbit.txt")
    if plaintext is None:
        Terminal.output("Failed to read or prepare plaintext.")
        return

    # Encryption
    ciphertext = hill.encode(plaintext, key_matrix, Terminal.debug)
    Terminal.output("Ciphertext: " + ciphertext[:20])

    # Cryptanalysis
    Terminal.output("Starting Cryptanalysis...")
    perform_cryptanalysis(plaintext[300:], ciphertext, key_size, key_matrix)


if __name__ == "__main__":
    main()
