# from nltk.tokenize import word_tokenize
# from nltk.probability import FreqDist
# import matplotlib.pyplot as plt

# file = open("text.txt")
# text = file.read()
# tokenized_word=word_tokenize(text)
# # print(tokenized_word)

# fdist = FreqDist(tokenized_word)
# # print(fdist)
# # print(fdist.most_common(2))

# fdist.plot(30,cumulative=False)
# plt.show()



#########################################################
import stanza
from collections import Counter
from spacy.lang.hi import STOP_WORDS as STOP_WORDS_HI
from nltk.tokenize import word_tokenize
from nltk.probability import FreqDist

import matplotlib.pyplot as plt
from matplotlib.pyplot import figure
from matplotlib.font_manager import FontProperties
import matplotlib as mpl




file1 = open("nofor.txt")
text = file1.read()
# text = " ". join(paragraph)
words = text.split(" ")


cnt = Counter(words)

cnt.most_common(10)



nlp = stanza.Pipeline('hi', processors='tokenize,pos,lemma') 
sentence = open("nofor.txt").read()
doc = nlp(sentence)

pos_all = []

# for token in doc:
#   print(token.text, token.norm_, token.orth_)
for sentence in doc.sentences:
     for word in sentence.words:
        pos_all.append(word.upos)



not_stop_words = [word for word in words if word not in set(STOP_WORDS_HI) ]


non_stop_cnt = Counter(not_stop_words)
POS_ALL = Counter(pos_all)


fdist = non_stop_cnt.most_common(30)
Pos_all = POS_ALL.most_common(30)

# print(fdist)



mpl.rcParams['font.sans-serif'] = ['Source Han Sans TW',
                                   'sans-serif',
                                   "Lohit Devanagari"  # fc-list :lang=hi family --> run in bash to check what fonts are supported
                                   ]


figure(num=None, figsize=(15, 6), dpi=80, facecolor='w', edgecolor='k')

# POS
a = list.copy(Pos_all)
b = dict(a)


val_val = b.values()
key_val = b.keys()
plt.bar(key_val,val_val)
plt.show()


