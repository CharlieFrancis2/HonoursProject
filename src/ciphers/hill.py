import numpy as np
from numpy.random import randint
from math import gcd
from sympy import Matrix
from analysis import utility as util
from numpy.linalg import det


def matrix_mod_inv(matrix, modulus):
    """
    Calculate the modular inverse of a matrix modulo a specified modulus.

    Args:
        matrix (numpy array): The matrix to invert.
        modulus (int): The modulus for inversion.

    Returns:
        numpy array: The modular inverse of the matrix, or None if no inverse exists.
    """
    # Convert numpy matrix to sympy Matrix for mod operations
    sympy_matrix = Matrix(matrix)
    try:
        # Attempt to find the inverse modulo the specified modulus
        inv_mod_matrix = sympy_matrix.inv_mod(modulus)
        return np.array(inv_mod_matrix).astype(int)
    except ValueError as e:
        # Handle cases where the matrix is not invertible modulo the given modulus
        print(f"Matrix inversion error: {e}")
        return None


def text_to_vector(text):
    """
    Convert a string of uppercase letters to a vector of numerical values relative to 'A'.

    Args:
        text (str): The text to convert.

    Returns:
        list of int: A list of integers where each integer represents the positional difference from 'A'.
    """
    return [ord(char) - ord('A') for char in text]


def vector_to_text(vector):
    """
    Convert a list of integers back to text, assuming each integer represents a character offset from 'A'.

    Args:
        vector (list of int): The vector to convert.

    Returns:
        str: The corresponding string of characters.
    """
    return ''.join(chr(num + ord('A')) for num in vector)


def is_invertible(matrix):
    """
    Determine if a matrix is invertible under modular arithmetic by checking its determinant.

    Args:
        matrix (numpy array): The matrix to check.

    Returns:
        bool: True if the matrix is invertible modulo 26, False otherwise.
    """
    det_val = int(np.round(np.linalg.det(matrix)))
    return gcd(det_val, 26) == 1


def generate_key(n):
    """
    Generate a random nxn invertible matrix modulo 26 to be used as a key in the Hill cipher.

    Args:
        n (int): The size of the matrix (nxn). It must be a positive integer.

    Returns:
        numpy array: An invertible matrix modulo 26, or raises ValueError if an invertible matrix cannot be generated.
    """
    if not n >= 0:
        raise ValueError("Matrix size 'n' must be a positive integer.")


    attempt_limit = 100  # Set a limit to avoid infinite loops
    for _ in range(attempt_limit):
        # Create a random nxn matrix with values from 0 to 25
        matrix = randint(0, 26, (n, n))
        if is_invertible(matrix):
            return matrix

    # If no invertible matrix is found within the attempt limit, raise an error
    raise ValueError(f"Failed to generate an invertible {n}x{n} matrix after {attempt_limit} attempts.")


def reshape_or_adjust_matrix(vector, blocksize):
    """
    Reshape a flat list of numbers into a blocksize x blocksize matrix.

    Args:
        vector (list): The flat list to reshape.
        blocksize (int): The size of the blocks (dimension of the square matrix).

    Returns:
        numpy array: The reshaped matrix.
    """
    matrix_size = blocksize ** 2
    new_vector = vector[:matrix_size]
    np_vector = np.array(new_vector)
    return np_vector.reshape((blocksize, blocksize))


def solve_linear_equation(A, B):
    """
    Solve the linear equation AX = B for X using matrix algebra.

    Args:
        A (numpy array): Coefficient matrix.
        B (numpy array): Constant terms matrix.

    Returns:
        numpy array: Solution matrix X.
    """
    A_inv = np.linalg.inv(A)
    return np.dot(A_inv, B)


def read_and_prepare_text(file_path):
    """
    Read text from a file and prepare it by removing non-alphabetical characters and converting to uppercase.

    Args:
        file_path (str): Path to the text file.

    Returns:
        str: The processed text, or None if the file is empty.
    """
    plaintext = util.read_from_file(file_path)
    return util.prepare_text(plaintext) if plaintext else None


def matrix_to_string(matrix):
    """
    Convert a matrix to a single string with elements separated by spaces.

    Args:
        matrix (numpy array): The matrix to convert.

    Returns:
        str: The string representation of the matrix.
    """
    return ' '.join(map(str, matrix.flatten()))


def extract_and_trim(plaintext, start_index, key_size):
    """
    Extract a substring from the plaintext that aligns with the required block size for the Hill cipher.

    Args:
        plaintext (str): The original plaintext.
        start_index (int): The starting index for extraction.
        key_size (int): The size of the key matrix (determines the block size).

    Returns:
        str: The trimmed plaintext suitable for the block size.
    """
    block_size = key_size ** 2
    end_index = len(plaintext)
    trimmed_length = (end_index - start_index) // block_size * block_size
    return plaintext[start_index:start_index + trimmed_length]


def encode(text, key_matrix, terminal_callback):
    """
    Encode text using the Hill cipher with a specified key matrix.

    Args:
        text (str): The plaintext to encode.
        key_matrix (numpy array): The encryption key matrix.

    Returns:
        str: The encoded ciphertext.
    """
    text = util.prepare_text(text)
    text_vector = np.array(text_to_vector(text))
    encoded_vector = np.dot(key_matrix, text_vector.reshape(-1, key_matrix.shape[0]).T).T.flatten() % 26
    return vector_to_text(encoded_vector)


def decode(text, key_matrix, terminal_callback):
    """
    Decode text using the Hill cipher and a specified key matrix.

    Args:
        text (str): The ciphertext to decode.
        key_matrix (numpy array): The decryption key matrix.

    Returns:
        str: The decoded plaintext, or None if decoding is not possible.
    """
    key_inv_matrix = matrix_mod_inv(key_matrix, 26)
    if key_inv_matrix is None:
        print("Error: Key matrix inversion failed. Decryption cannot proceed.")
        return None

    text_vector = np.array(text_to_vector(text))
    decoded_vector = np.dot(key_inv_matrix, text_vector.reshape(-1, key_matrix.shape[0]).T).T.flatten() % 26
    decoded_text = vector_to_text(decoded_vector)
    return util.remove_padding(decoded_text)


def inv_mod_matrix(matrix, modulus):
    """
    Calculate the inverse of a matrix modulo a given modulus using SymPy.

    Args:
        matrix (numpy array): The matrix to invert.
        modulus (int): The modulus for the inversion.

    Returns:
        numpy array: The inverted matrix modulo the given modulus, or raises an error if not invertible.
    """
    det_matrix = int(round(det(matrix)))
    det_inv_mod = pow(det_matrix, -1, modulus)
    if det_inv_mod is None:
        raise ValueError("Matrix is not invertible modulo {}".format(modulus))
    matrix_mod_inv = Matrix(matrix).inv_mod(modulus)
    return np.array(matrix_mod_inv).astype(int)


def matrix_to_string(matrix):
    """
    Convert a numpy matrix to a string, with elements of each row separated by spaces.

    Args:
        matrix (numpy array): The matrix to convert.

    Returns:
        str: The formatted string representation of the matrix.
    """
    return '\n'.join(' '.join(str(cell) for cell in row) for row in matrix)


def perform_cryptanalysis(known_plaintext, ciphertext, blocksize, output_callback, terminal_callback):
    """
    Attempt to deduce valid Hill cipher keys based on known plaintext-ciphertext pairs.

    Args:
        known_plaintext (str): The known plaintext corresponding to the ciphertext.
        ciphertext (str): The ciphertext to analyze.
        blocksize (int): The block size used in the Hill cipher.

    Returns:
        list: A list of valid keys if any are found.
    """
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
                continue
            P_inv_mod_26 = inv_mod_matrix(P_matrix, 26)
            K_matrix = (np.dot(P_inv_mod_26, C_matrix) % 26).astype(int)
            if int(np.round(det(K_matrix))) % 26 == 0 or gcd(int(np.round(det(K_matrix))), 26) != 1:
                terminal_callback("Non-invertible K matrix skipped.")
                continue
            matrix_hash = tuple(map(tuple, K_matrix))
            if matrix_hash not in seen_hashes:
                seen_hashes.add(matrix_hash)
                K_matrix = K_matrix.transpose()
                valid_keys.append(K_matrix.tolist())
                terminal_callback(f"Unique key matrix found and added: {K_matrix.tolist()}")
    except Exception as e:
        terminal_callback(f"Error encountered: {e}")
    if not valid_keys:
        terminal_callback("No valid key matrices found after complete analysis.")
    return valid_keys


def cryptanalyse(known_text, cipher_text, key_size, start_index, output_callback, terminal_callback):
    """
    Main function for cryptanalysis using known plaintext and corresponding ciphertext.

    Args:
        known_text (str): The known plaintext segment.
        cipher_text (str): The corresponding ciphertext.
        key_size (int): The size of the key matrix (block size).
        start_index (int): The starting index in the ciphertext for analysis.

    Returns:
        str: A summary of the results including any valid keys found.
    """
    terminal_callback("Starting cryptanalysis...")
    output_str = "Results:\n"
    if len(known_text) < key_size ** 2:
        terminal_callback("Insufficient known plaintext length for analysis.")
        return
    if start_index + len(known_text) > len(cipher_text):
        terminal_callback("Known text alignment exceeds cipher text length.")
        return
    cipher_segment = cipher_text[start_index:start_index + len(known_text)]
    valid_keys = perform_cryptanalysis(known_text, cipher_segment, key_size, output_callback, terminal_callback)
    terminal_callback(f"Received {len(valid_keys)} valid keys.")
    if valid_keys:
        for key_matrix in valid_keys:
            key_string = matrix_to_string(np.array(key_matrix))
            if util.validate_and_convert_hill_key(key_matrix):
                output_str += f"Found matching key: {key_string}\n"
            else:
                output_str += "Failed validation function\n"
    else:
        output_str += "No valid keys found.\n"
    return output_str
