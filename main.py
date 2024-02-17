from ciphers.caesar import encode as caesar_encode, decode as caesar_decode, cryptanalyse as caesar_crptanalyse
from analysis.utility import read_from_file as read, prepare_text as prepare


plain_text = read('plain_texts/hobbit.txt')
key = 4
glasgow_text = "Glasgow has the largest economy in Scotland and the third-highest GDP per capita of any city in the UK.[9][10] Glasgow's major cultural institutions enjoy international reputations including The Royal Conservatoire of Scotland, Burrell Collection, Kelvingrove Art Gallery and Museum, Royal Scottish National Orchestra, BBC Scottish Symphony Orchestra, Scottish Ballet and Scottish Opera. The city was the European Capital of Culture in 1990 and is notable for its architecture, culture, media, music scene, sports clubs and transport connections. It is the fifth-most visited city in the United Kingdom.[11] The city hosted the 2021 United Nations Climate Change Conference (COP26) at its main events venue, the SEC Centre. Glasgow hosted the 2014 Commonwealth Games and the first European Championships in 2018, and was one of the host cities for UEFA Euro 2020. The city is also well known in the sporting world for football, particularly for the Old Firm rivalry."

prepared = prepare(glasgow_text)
print(prepared)

encoded = caesar_encode(glasgow_text, 3)
print(encoded)


# # Encoding with Ceasar cipher
# cipher1 = caesar_encode(plain_text, 4)
# print(cipher1)
# cipher2 = caesar_encode(plain_text, 3)
# print(cipher2)

# caesar_crptanalyse(cipher1)



