import numpy as np
from numpy.linalg import inv, det


def text_to_vector(text):
    """Convert text to a numerical vector."""
    return [ord(char) - ord('A') for char in text]


def vector_to_text(vector):
    """Convert a numerical vector to text."""
    return ''.join(chr(int(num) + ord('A')) for num in vector)


def matrix_mod_inv(matrix, modulus):
    """Find the modular inverse of a matrix."""
    det_inv = pow(int(round(det(matrix))), -1, modulus)
    matrix_inv = det_inv * np.round(det(matrix) * inv(matrix)).astype(int) % modulus
    return matrix_inv


def encode(text, key_matrix):
    """Encode text using the Hill cipher with a given key matrix."""
    text_vector = np.array(text_to_vector(text))
    encoded_vector = np.dot(key_matrix, text_vector.reshape(-1, key_matrix.shape[0]).T).T.flatten() % 26
    return vector_to_text(encoded_vector)


def decode(text, key_matrix):
    """Decode text using the Hill cipher with a given key matrix."""
    key_inv_matrix = matrix_mod_inv(key_matrix, 26)
    text_vector = np.array(text_to_vector(text))
    decoded_vector = np.dot(key_inv_matrix, text_vector.reshape(-1, key_matrix.shape[0]).T).T.flatten() % 26
    return vector_to_text(decoded_vector)
