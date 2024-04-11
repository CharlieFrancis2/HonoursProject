import numpy as np
from numpy.random import randint
from math import gcd
from sympy import Matrix
from analysis import utility as util
from numpy.linalg import det


def matrix_mod_inv(matrix, modulus):
    """Returns the modular inverse of a matrix modulo the given modulus if it exists."""
    sympy_matrix = Matrix(matrix)
    try:
        inv_mod_matrix = sympy_matrix.inv_mod(modulus)
        return np.array(inv_mod_matrix).astype(int)
    except ValueError as e:
        print(f"Matrix inversion error: {e}")
        return None


def text_to_vector(text):
    return [ord(char) - ord('A') for char in text]


def vector_to_text(vector):
    return ''.join(chr(num + ord('A')) for num in vector)


def is_invertible(matrix):
    det = int(np.round(np.linalg.det(matrix)))
    return gcd(det, 26) == 1


def generate_key(n):
    while True:
        # Generate random matrix with values from 1 to 25 (inclusive)
        matrix = randint(1, 26, (n, n))
        if is_invertible(matrix):
            return matrix


def reshape_or_adjust_matrix(vector, blocksize):
    # Ensure the vector is a NumPy array before reshaping
    # print("Vector: " + str(vector))
    # print("Blocksize: " + str(blocksize))

    matrix_size = blocksize ** 2
    # print("Matrix Size: " + str(matrix_size))

    new_vector = vector[:matrix_size]
    # print("New Vector: " + str(new_vector))

    np_vector = np.array(new_vector)
    return np_vector.reshape((blocksize, blocksize))


def solve_linear_equation(A, B):
    # Solve AX = B for X
    A_inv = np.linalg.inv(A)
    return np.dot(A_inv, B)


def read_and_prepare_text(file_path):
    plaintext = util.read_from_file(file_path)
    if plaintext:
        return util.prepare_text(plaintext)
    else:
        return None


def matrix_to_string(matrix):
    """Convert a NumPy matrix to a string with spaces separating the elements."""
    return ' '.join(map(str, matrix.flatten()))


def extract_and_trim(plaintext, start_index, key_size):
    """Extract and trim the plaintext to ensure it contains only full blocks for the matrix."""
    block_size = key_size ** 2  # Block size derived from key matrix dimensions

    # Calculate the ending index by finding how many full blocks fit into the remaining text length
    end_index = len(plaintext)
    trimmed_length = (end_index - start_index) // block_size * block_size  # Maximum length in complete blocks

    trimmed_text = plaintext[start_index:start_index + trimmed_length]
    return trimmed_text


def encode(text, key_matrix, terminal_callbacl):
    """Encode text using the Hill cipher with a given key matrix."""
    text = util.prepare_text(text)
    text = util.add_padding(text, key_matrix.shape[1])
    text_vector = np.array(text_to_vector(text))
    encoded_vector = np.dot(key_matrix, text_vector.reshape(-1, key_matrix.shape[0]).T).T.flatten() % 26
    # print(f"Prepared and padded text for encoding: {text}")
    # print(f"Encoded vector: {encoded_vector}")
    return vector_to_text(encoded_vector)  # Make sure to return the encoded_text


def decode(text, key_matrix, terminal_callback):
    # print(text)
    # print(key_matrix)
    # Note: No padding should be added here, since ciphertext is expected to match block size
    # text = prepare_text(text)  # Ensure this is needed, might not be for pure ciphertext

    key_inv_matrix = matrix_mod_inv(key_matrix, 26)

    if key_inv_matrix is None:
        print("Error: Key matrix inversion failed. Decryption cannot proceed.")
        return None  # Or handle the error as appropriate for your application

    # print(f"Processed text: {text}")
    text = util.prepare_text(text)
    text = util.add_padding(text, key_matrix.shape[1])
    text_vector = np.array(text_to_vector(text))
    # print(f"Text vector length: {len(text_vector)}")

    # print(f"Text vector length before reshaping: {len(text_vector)}")
    # print(f"Expected reshaping dimensions: (-1, {key_matrix.shape[0]})")

    decoded_vector = np.dot(key_inv_matrix, text_vector.reshape(-1, key_matrix.shape[0]).T).T.flatten() % 26
    decoded_text = vector_to_text(decoded_vector)

    # print(f"Key inverse matrix for decoding: {key_inv_matrix}")
    # print(f"Decoded vector: {decoded_vector}")

    # Consider smarter padding removal if needed
    return util.remove_padding(decoded_text)  # Adjust based on your padding strategy


def inv_mod_matrix(matrix, modulus):
    """Calculate the inverse of a matrix modulo a given modulus using SymPy."""
    det_matrix = int(round(det(matrix)))  # Compute the determinant
    det_inv_mod = pow(det_matrix, -1, modulus)  # Find the modular inverse of the determinant

    if det_inv_mod is None:
        raise ValueError("Matrix is not invertible modulo {}".format(modulus))

    matrix_mod_inv = Matrix(matrix).inv_mod(modulus)  # Using SymPy for precise matrix inversion modulo
    return np.array(matrix_mod_inv).astype(int)


def matrix_to_string(matrix):
    """Converts a matrix to a string format for easier display in the GUI."""
    return '\n'.join(' '.join(str(cell) for cell in row) for row in matrix)


def perform_cryptanalysis(known_plaintext, ciphertext, blocksize, output_callback, terminal_callback):
    """Perform cryptanalysis to find valid Hill cipher keys."""
    if not known_plaintext or not ciphertext:
        terminal_callback("Invalid input provided.")
        return []

    valid_keys = []
    seen_hashes = set()

    P_full_vector = np.array(text_to_vector(known_plaintext))
    C_full_vector = np.array(text_to_vector(ciphertext))

    max_length = min(len(P_full_vector), len(C_full_vector))
    max_complete_blocks = max_length // (blocksize ** 2) * (blocksize ** 2)

    P_full_vector = P_full_vector[:max_complete_blocks]
    C_full_vector = C_full_vector[:max_complete_blocks]

    terminal_callback(f"Processing {len(P_full_vector) // (blocksize ** 2)} blocks.")
    try:
        num_matrices = len(P_full_vector) // (blocksize ** 2)
        for i in range(num_matrices):
            P_matrix = P_full_vector[i * blocksize ** 2:(i + 1) * blocksize ** 2].reshape(blocksize, blocksize)
            C_matrix = C_full_vector[i * blocksize ** 2:(i + 1) * blocksize ** 2].reshape(blocksize, blocksize)

            det_P = int(np.round(det(P_matrix))) % 26
            if det_P == 0 or gcd(det_P, 26) != 1:
                terminal_callback("Non-invertible P matrix skipped.")
                continue  # Skip non-invertible matrices

            P_inv_mod_26 = inv_mod_matrix(P_matrix, 26)
            K_matrix = (np.dot(P_inv_mod_26, C_matrix) % 26).astype(int)

            if int(np.round(det(K_matrix))) % 26 == 0 or gcd(int(np.round(det(K_matrix))), 26) != 1:
                terminal_callback("Non-invertible K matrix skipped.")
                continue  # Skip non-invertible key matrices

            matrix_hash = tuple(map(tuple, K_matrix))
            if matrix_hash not in seen_hashes:
                seen_hashes.add(matrix_hash)
                valid_keys.append(K_matrix.tolist())
                terminal_callback(f"Unique key matrix found and added: {K_matrix.tolist()}")

    except Exception as e:
        terminal_callback(f"Error encountered: {e}")

    if not valid_keys:
        terminal_callback("No valid key matrices found after complete analysis.")
    return valid_keys


def cryptanalyse(known_text, cipher_text, key_size, start_index, output_callback, terminal_callback):
    """Main function to handle the setup and execution of cryptanalysis."""
    if len(known_text) < key_size ** 2:
        terminal_callback("Insufficient known plaintext length for analysis.")
        return

    if start_index + len(known_text) > len(cipher_text):
        terminal_callback("Known text alignment exceeds cipher text length.")
        return

    cipher_segment = cipher_text[start_index:start_index + len(known_text)]

    terminal_callback("Starting cryptanalysis...")
    valid_keys = perform_cryptanalysis(known_text, cipher_segment, key_size, output_callback, terminal_callback)

    terminal_callback(f"Received {len(valid_keys)} valid keys.")
    if valid_keys:
        for key_matrix in valid_keys:
            key_string = matrix_to_string(np.array(key_matrix))
            if util.validate_and_convert_hill_key(key_matrix):
                output_callback(f"Found matching key: {key_string}")
            else:
                output_callback("Failed validation functiom")
    else:
        output_callback("No valid keys found.")


