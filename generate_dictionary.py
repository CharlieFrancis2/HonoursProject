import random
import string


def generate_random_words(num_words, word_length=10):
    """
    Generate a specified number of random words, each of a given length.

    :param num_words: The number of random words to generate.
    :param word_length: The length of each word. Default is 10.
    :return: A list of random words.
    """
    words = set()  # Use a set to avoid duplicates

    while len(words) < num_words:
        # Generate a random word
        word = ''.join(random.choice(string.ascii_lowercase) for _ in range(word_length))
        words.add(word)

    return list(words)


# Number of words to generate
num_words = 59049

# Generate the words
random_words = generate_random_words(num_words)

# Optionally, save the words to a file
with open("random_words.txt", "w") as file:
    for word in random_words:
        file.write(word + "\n")

print(f"Generated {len(random_words)} random words.")
