from spacy.lang.hi import STOP_WORDS as STOP_WORDS_HI

file1 = open("nofor.txt")
text = file1.read()
words = text.split(" ")


not_stop_words = [word for word in words if word not in set(STOP_WORDS_HI) ]

print(not_stop_words)

