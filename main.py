import time
from ciphers.vigenere import decode as vigenere_decode
from analysis import utility as u


def measure_decryption_time(cipher_text, keys):
    total_time = 0

    # Ensure we're using exactly 100 keys for the measurement
    keys = keys[:100]
    num_keys = len(keys)

    for key in keys:
        start_time = time.time()
        _ = vigenere_decode(cipher_text, key)  # Decrypt with the Vigenère cipher
        end_time = time.time()

        decryption_time = end_time - start_time
        total_time += decryption_time

    average_time = total_time / num_keys
    return average_time


# Load a sample of keys from 'random_words.txt'
sample_keys = u.read_from_file('random_words.txt').splitlines()[:100]  # Use a smaller sample for efficiency

# Assume 'cipher_text' contains the encrypted text of "The Hobbit"
cipher_text = u.read_from_file('plain_texts/hobbit.txt')

# Measure the average decryption time
average_decryption_time = measure_decryption_time(cipher_text, sample_keys)
print(f"Average decryption time: {average_decryption_time} seconds")
print(f"Estimate decryption time: {average_decryption_time * 59049  } seconds")



