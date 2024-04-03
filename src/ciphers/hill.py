import numpy as np
from numpy.random import randint
from math import gcd
from sympy import Matrix
from analysis.utility import mod_inverse, prepare_text, add_padding, remove_padding


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
        matrix = randint(0, 26, (n, n))
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


def encode(text, key_matrix, terminal_callbacl):
    """Encode text using the Hill cipher with a given key matrix."""
    text = prepare_text(text)
    text = add_padding(text, key_matrix.shape[1])
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
    text = prepare_text(text)
    text = add_padding(text, key_matrix.shape[1])
    text_vector = np.array(text_to_vector(text))
    # print(f"Text vector length: {len(text_vector)}")

    # print(f"Text vector length before reshaping: {len(text_vector)}")
    # print(f"Expected reshaping dimensions: (-1, {key_matrix.shape[0]})")

    decoded_vector = np.dot(key_inv_matrix, text_vector.reshape(-1, key_matrix.shape[0]).T).T.flatten() % 26
    decoded_text = vector_to_text(decoded_vector)

    # print(f"Key inverse matrix for decoding: {key_inv_matrix}")
    # print(f"Decoded vector: {decoded_vector}")

    # Consider smarter padding removal if needed
    return remove_padding(decoded_text)  # Adjust based on your padding strategy


def cryptanalyse(known_plaintext, ciphertext, blocksize, output_callback, terminal_callback):

    if not known_plaintext or not ciphertext:
        terminal_callback("Invalid input provided.")
        return []

    # Initialize a list to hold all valid key matrices
    valid_keys = []

    # Convert plaintext and ciphertext to vectors
    P_full_vector = text_to_vector(known_plaintext)
    C_full_vector = text_to_vector(ciphertext)

    # Attempt to derive a key for each possible segment of the given size
    for start in range(len(P_full_vector) - blocksize ** 2 + 1):
        P_vector = P_full_vector[start:start + blocksize ** 2]
        C_vector = C_full_vector[start:start + blocksize ** 2]

        P = Matrix(P_vector).reshape(blocksize, blocksize)
        C = Matrix(C_vector).reshape(blocksize, blocksize)

        try:
            # Check if P is invertible in mod 26
            if P.det() % 26 == 0 or gcd(int(P.det()), 26) != 1:
                continue

            P_inv_mod_26 = P.inv_mod(26)

            # Calculating the potential key matrix
            K = P_inv_mod_26 * C % 26

            # Check if the derived matrix K is valid
            if gcd(int(K.det()), 26) == 1:
                # Add the valid key to the list
                valid_keys.append((K.tolist(), start))

        except Exception as e:
            terminal_callback(f"Error encountered at start {start}: {e}")
            continue

    if not valid_keys:
        output_callback("No valid key matrices found.")
        return []

    # for key, position in valid_keys:
    #     output_callback(f"Valid key matrix found at position {position}: {key}")

    return valid_keys
