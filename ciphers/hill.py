import numpy as np
from analysis.utility import mod_inverse, prepare_text, add_padding, remove_padding


def matrix_mod_inv(matrix, modulus):
    """
    Calculates the modular inverse of a 2x2 matrix under a given modulus.

    Args:
        matrix (numpy.ndarray): The 2x2 matrix for which to find the modular inverse.
        modulus (int): The modulus to perform calculations under.

    Returns:
        numpy.ndarray: The modular inverse of the matrix under the given modulus.
    """
    # Calculate the determinant of the matrix
    det = int(np.round(np.linalg.det(matrix)))
    # Find the modular inverse of the determinant
    det_inv = mod_inverse(det, modulus)

    if det_inv is None:
        raise ValueError("Matrix is not invertible modulo {}".format(modulus))

    # Apply the formula for the inverse of a 2x2 matrix, adjusting for modular arithmetic
    matrix_modulus_inv = np.array([[matrix[1, 1], -matrix[0, 1]], [-matrix[1, 0], matrix[0, 0]]])
    matrix_modulus_inv = (det_inv * matrix_modulus_inv) % modulus

    return matrix_modulus_inv.astype(int)


def text_to_vector(text):
    """Convert text to numerical vector based on alphabetical position."""
    return [ord(char) - ord('A') for char in text]  # Example for uppercase letters


def vector_to_text(vector):
    """Convert numerical vector back to text based on alphabetical position."""
    return ''.join(chr(num + ord('A')) for num in vector)  # Example for uppercase letters


def encode(text, key_matrix):
    """Encode text using the Hill cipher with a given key matrix."""
    text = prepare_text(text)
    text = add_padding(text, key_matrix.shape[1])
    text_vector = np.array(text_to_vector(text))
    encoded_vector = np.dot(key_matrix, text_vector.reshape(-1, key_matrix.shape[0]).T).T.flatten() % 26
    return vector_to_text(encoded_vector)  # Make sure to return the encoded_text


def decode(text, key_matrix):
    print(text)
    print(key_matrix)
    # Note: No padding should be added here, since ciphertext is expected to match block size
    text = prepare_text(text)  # Ensure this is needed, might not be for pure ciphertext

    key_inv_matrix = matrix_mod_inv(key_matrix, 26)

    print(f"Processed text: {text}")
    text_vector = np.array(text_to_vector(text))
    print(f"Text vector length: {len(text_vector)}")

    decoded_vector = np.dot(key_inv_matrix, text_vector.reshape(-1, key_matrix.shape[0]).T).T.flatten() % 26
    decoded_text = vector_to_text(decoded_vector)

    # Consider smarter padding removal if needed
    return remove_padding(decoded_text)  # Adjust based on your padding strategy


plain = 'hello'
key = np.array([[5, 17], [4, 15]])
print(plain)
print(key)

ciphertext = encode(plain, key)
print(decode(ciphertext, key))
