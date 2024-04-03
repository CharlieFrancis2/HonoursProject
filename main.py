import ciphers.hill as hill
import analysis.utility as util
import numpy as np
from itertools import permutations


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
    # return key_matrix


def brute_force_key(original_key_components, ciphertext, known_text, term):
    # Generate all permutations of the key components
    all_permutations = list(permutations(original_key_components))

    for perm in all_permutations:
        # Reconstruct the key matrix from the current permutation
        key_matrix = np.array(perm).reshape(2, 2)

        # Attempt to decode the ciphertext with the current key matrix
        decoded_text = hill.decode(ciphertext, key_matrix, Terminal)

        # Check if the known plaintext is in the decoded text
        if known_text in decoded_text:
            print(f"Success! Found key: {key_matrix}")
            return key_matrix

    print("Failed to find the correct key.")
    return None


# Updated perform_cryptanalysis function to include the new logic
def perform_cryptanalysis(known_text, cipher_text, key_size, original_key_matrix, Terminal):
    valid_keys = hill.cryptanalyse(known_text, cipher_text, key_size, Terminal.output, Terminal.debug)

    # Store found keys with their positions to avoid duplicates
    found_keys = {}

    for key_matrix, position in valid_keys:
        # Re-transpose the found key matrix based on its start position and block size
        retransposed_key_matrix = retranspose_key(np.array(key_matrix), position, key_size)

        # Decode with the found key
        test = hill.decode(cipher_text, retransposed_key_matrix, Terminal)

        # Use find() method to check if known_text is in test and get its starting position
        found_index = test.find(known_text)
        if found_index != -1:
            retransposed_key_string = matrix_to_string(retransposed_key_matrix)
            # If the key hasn't been found before, add it to the dictionary
            if retransposed_key_string not in found_keys:
                Terminal.output(
                    f"Found matching key with known text starting at index {found_index} in decoded text. Key: {retransposed_key_matrix}")
                found_keys[retransposed_key_string] = position
        else:
            retransposed_key_string = matrix_to_string(retransposed_key_matrix)
            Terminal.output(f"Key at position {position} does not match the original. Key: {retransposed_key_string}")

    # Print all unique found keys and their positions
    if found_keys:
        for key_string, position in found_keys.items():
            print(f"Found matching key at position {position}. Key: {key_string}")
    else:
        print("No Matching key found")


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
    #
    # plaintext = "In a hole in the ground there lived a hobbit. Not a nasty,dirty, wet hole, filled with the ends of worms and an oozysmell, nor yet a dry, bare, sandy hole with nothing in it tosit down on or to eat: it was a hobbit-hole, and that means comfort."
    # plaintext = util.prepare_text(plaintext)

    # Encryption
    ciphertext = hill.encode(plaintext, key_matrix, Terminal.debug)
    Terminal.output("Ciphertext: " + ciphertext[:20])

    # Cryptanalysis
    Terminal.output("Starting Cryptanalysis...")
    perform_cryptanalysis(plaintext[1:], ciphertext, key_size, key_matrix, Terminal)


if __name__ == "__main__":
    main()
