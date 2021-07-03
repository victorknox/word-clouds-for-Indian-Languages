# import io
# from nltk.corpus import stopwords
# from nltk.tokenize import word_tokenize

# # word_tokenize accepts
# # a string as an input, not a file.
# stop_words = set(stopwords.words('english'))
# file1 = open("test.txt")

# # Use this to read file content as a stream:
# line = file1.read()
# words = line.split()
# for r in words:
# 	if not r in stop_words:
# 		appendFile = open('filteredtext.txt','a')
# 		appendFile.write(" "+r)
# 		appendFile.close()



from spacy.lang.hi import STOP_WORDS as STOP_WORDS_HI
from collections import Counter

file1 = open("text_with_stop.txt")
text = file1.read()
# text = " ". join(paragraph)
words = text.split(" ")


not_stop_words = [word for word in words if word not in set(STOP_WORDS_HI) ]
# non_stop_cnt = Counter(non_stop_words)
non_stop_cnt = Counter(not_stop_words)

print(not_stop_words)

