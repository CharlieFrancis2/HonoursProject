import numpy as np
from numpy.random import randint
from math import gcd
from sympy import Matrix
from analysis.utility import mod_inverse, prepare_text, add_padding, remove_padding


def matrix_mod_inv(matrix, modulus):
    sympy_matrix = Matrix(matrix)
    return sympy_matrix.inv_mod(modulus).tolist()


def text_to_vector(text):
    """Convert text to numerical vector based on alphabetical position."""
    return [ord(char) - ord('A') for char in text]  # Example for uppercase letters


def vector_to_text(vector):
    """Convert numerical vector back to text based on alphabetical position."""
    return ''.join(chr(num + ord('A')) for num in vector)  # Example for uppercase letters


def is_invertible(matrix):
    det = int(np.round(np.linalg.det(matrix)))
    return gcd(det, 26) == 1


def generate_key(n):
    """
    Generates a random n x n matrix for Hill cipher and returns it as a formatted string.
    """
    while True:
        matrix = randint(0, 26, (n, n))
        if is_invertible(matrix):
            # Convert the matrix to a single string with values separated by spaces
            return ' '.join(map(str, matrix.flatten()))


def reshape_or_adjust_matrix(vector, blocksize):
    # Assuming vector length is at least blocksize^2
    matrix_size = blocksize ** 2
    return vector[:matrix_size].reshape((blocksize, blocksize))


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
    return vector_to_text(encoded_vector)  # Make sure to return the encoded_text


def decode(text, key_matrix, terminal_callback):
    # print(text)
    # print(key_matrix)
    # Note: No padding should be added here, since ciphertext is expected to match block size
    # text = prepare_text(text)  # Ensure this is needed, might not be for pure ciphertext

    key_inv_matrix = matrix_mod_inv(key_matrix, 26)

    # print(f"Processed text: {text}")
    text_vector = np.array(text_to_vector(text))
    # print(f"Text vector length: {len(text_vector)}")

    decoded_vector = np.dot(key_inv_matrix, text_vector.reshape(-1, key_matrix.shape[0]).T).T.flatten() % 26
    decoded_text = vector_to_text(decoded_vector)

    # Consider smarter padding removal if needed
    return remove_padding(decoded_text)  # Adjust based on your padding strategy


def cryptanalyse(known_plaintext, ciphertext, blocksize):
    plaintext_vector = text_to_vector(known_plaintext)
    ciphertext_vector = text_to_vector(ciphertext)

    for i in range(len(ciphertext_vector) - blocksize + 1):
        current_ciphertext_segment = ciphertext_vector[i: i + blocksize]
        if len(plaintext_vector) >= blocksize:
            A = reshape_or_adjust_matrix(plaintext_vector, blocksize)
            B = reshape_or_adjust_matrix(current_ciphertext_segment, blocksize)
            try:
                key_matrix = solve_linear_equation(A, B)
                return key_matrix, i
            except Exception as e:
                # If solving fails (e.g., A is not invertible), continue
                continue

    return None, None


