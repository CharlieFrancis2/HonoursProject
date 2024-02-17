from ciphers.caesar import encode as caesar_encode, decode as caesar_decode, cryptanalyse as caesar_crptanalyse
from analysis import utility as u

from analysis.frequency_data import letter_frequencies as exp_letter, bigram_frequencies as exp_bi, trigram_frequencies as exp_tri
import pandas as pd

# plain_text = u.read_from_file('plain_texts/hobbit.txt')
# cipher_text = caesar_encode(plain_text, 6)


# key = 4
# glasgow_text = ("Glasgow has the largest economy in Scotland and the third-highest GDP per capita of any city in the "
#                 "UK.[9][10] Glasgow's major cultural institutions enjoy international reputations including The Royal "
#                 "Conservatoire of Scotland, Burrell Collection, Kelvingrove Art Gallery and Museum, Royal Scottish "
#                 "National Orchestra, BBC Scottish Symphony Orchestra, Scottish Ballet and Scottish Opera. The city "
#                 "was the European Capital of Culture in 1990 and is notable for its architecture, culture, media, "
#                 "music scene, sports clubs and transport connections. It is the fifth-most visited city in the United "
#                 "Kingdom.[11] The city hosted the 2021 United Nations Climate Change Conference (COP26) at its main "
#                 "events venue, the SEC Centre. Glasgow hosted the 2014 Commonwealth Games and the first European "
#                 "Championships in 2018, and was one of the host cities for UEFA Euro 2020. The city is also well "
#                 "known in the sporting world for football, particularly for the Old Firm rivalry.")

# letter_frequencies1, bigram_frequencies1, trigram_frequencies1 = u.generate_frequency_data(plain_text)
# letter_frequencies2, bigram_frequencies2, trigram_frequencies2 = u.generate_frequency_data(cipher_text)
#
#
# print("Plaintext letter, bi and tri: ")
# print(u.compute_chi_squared(letter_frequencies1, exp_letter, len(plain_text)))
# print(u.compute_chi_squared(bigram_frequencies1, exp_bi, len(plain_text)))
# print(u.compute_chi_squared(trigram_frequencies1, exp_tri, len(plain_text)))
# print("")
# print("Ciphertext letter, bi and tri: ")
# print(u.compute_chi_squared(letter_frequencies2, exp_letter, len(plain_text)))
# print(u.compute_chi_squared(bigram_frequencies2, exp_bi, len(plain_text)))
# print(u.compute_chi_squared(trigram_frequencies2, exp_tri, len(plain_text)))

def caesar_cipher_chi_analysis(text, exp_letter, exp_bi, exp_tri):
    # Assuming caesar_encode function encodes the plaintext with a given key
    # Assuming exp_letter, exp_bi, exp_tri are dictionaries with expected frequencies

    results = []

    for key in range(26):
        cipher_text = caesar_decode(text, key)

        # Generate frequency data for the cipher text
        letter_freqs, bigram_freqs, trigram_freqs = u.generate_frequency_data(cipher_text)

        # Compute chi-squared scores
        chi_letter = u.compute_chi_squared(letter_freqs, exp_letter, len(text))
        chi_bi = u.compute_chi_squared(bigram_freqs, exp_bi, len(text))
        chi_tri = u.compute_chi_squared(trigram_freqs, exp_tri, len(text))

        # Append results
        results.append((key, chi_letter, chi_bi, chi_tri))

    # Create a DataFrame to display the results
    df = pd.DataFrame(results, columns=['Key', 'Chi-Squared Letters', 'Chi-Squared Bigrams', 'Chi-Squared Trigrams'])

    # Sort the DataFrame by the Chi-Squared Letters column as a primary focus
    df_sorted = df.sort_values(by=['Chi-Squared Letters', 'Chi-Squared Bigrams', 'Chi-Squared Trigrams'])

    return df_sorted


# Example usage
# Load your plain text
#plain_text = u.read_from_file('plain_texts/hobbit.txt')
plain_text = "Hello world"
cipher_text = caesar_encode(plain_text, 6)

# Assuming exp_letter, exp_bi, exp_tri are defined as expected frequencies
df_results = caesar_cipher_chi_analysis(cipher_text, exp_letter, exp_bi, exp_tri)
print(df_results)


