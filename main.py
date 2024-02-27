from ciphers.caesar import encode as caesar_encode, decode as caesar_decode, chi_cryptanalysis as caesar_crptanalyse
from analysis import utility as u

from analysis.frequency_data import letter_frequencies as exp_letter, bigram_frequencies as exp_bi, trigram_frequencies as exp_tri
import pandas as pd

glasgow_text = ("Glasgow has the largest economy in Scotland and the third-highest GDP per capita of any city in the "
                "UK.[9][10] Glasgow's major cultural institutions enjoy international reputations including The Royal "
                "Conservatoire of Scotland, Burrell Collection, Kelvingrove Art Gallery and Museum, Royal Scottish "
                "National Orchestra, BBC Scottish Symphony Orchestra, Scottish Ballet and Scottish Opera. The city "
                "was the European Capital of Culture in 1990 and is notable for its architecture, culture, media, "
                "music scene, sports clubs and transport connections. It is the fifth-most visited city in the United "
                "Kingdom.[11] The city hosted the 2021 United Nations Climate Change Conference (COP26) at its main "
                "events venue, the SEC Centre. Glasgow hosted the 2014 Commonwealth Games and the first European "
                "Championships in 2018, and was one of the host cities for UEFA Euro 2020. The city is also well "
                "known in the sporting world for football, particularly for the Old Firm rivalry.")

# Example usage
# Load your plain text
plain_text = u.read_from_file('plain_texts/hobbit.txt')
plain_text2 = "Hello world my name is charlie"
cipher_text = caesar_encode(plain_text2, 9)

# Assuming exp_letter, exp_bi, exp_tri are defined as expected frequencies
caesar_crptanalyse(cipher_text, exp_letter, exp_bi, exp_tri)



