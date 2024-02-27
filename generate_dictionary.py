import itertools
import string
import os
import time
import argparse


def generate_dictionary(n, output_file):
    # Calculate total number of combinations
    total_combinations = 26 ** n

    # Start a timer
    start_time = time.time()

    # Process a small sample to estimate time
    sample_size = min(1000, total_combinations)  # Use 1000 combinations or total if fewer
    for _ in itertools.product(string.ascii_lowercase, repeat=min(3, n)):
        pass  # Simulate processing without writing to file for the sample
    sample_time = time.time() - start_time

    # Extrapolate estimated total time
    estimated_total_time = sample_time / sample_size * total_combinations
    print(f"Estimated time to complete: {estimated_total_time:.2f} seconds")

    # Ensure the output directory exists
    output_dir = os.path.dirname(output_file)
    if output_dir:  # If there's a specific directory path in output_file
        os.makedirs(output_dir, exist_ok=True)

    # Process all combinations, writing to file
    with open(output_file, 'w') as file:
        for word_tuple in itertools.product(string.ascii_lowercase, repeat=n):
            word = ''.join(word_tuple)
            file.write(f"{word}\n")

    actual_time_taken = time.time() - start_time
    print(f"Actual time taken: {actual_time_taken:.2f} seconds")


if __name__ == "__main__":
    # Set up argument parsing
    parser = argparse.ArgumentParser(
        description='Generate a dictionary file with all possible words of a given length.')
    parser.add_argument('n', type=int, help='Length of the words to generate.')
    parser.add_argument('output_file', type=str, help='Path to the output file where the words will be stored.')

    # Parse arguments
    args = parser.parse_args()

    # Call the function with the provided arguments
    generate_dictionary(args.n, args.output_file)
