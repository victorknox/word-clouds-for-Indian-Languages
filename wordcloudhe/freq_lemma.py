from nltk.tokenize import word_tokenize
from nltk.probability import FreqDist

import matplotlib.pyplot as plt
from matplotlib.pyplot import figure
from matplotlib.font_manager import FontProperties
import matplotlib as mpl
from collections import Counter
import stanza
from spacy.lang.hi import STOP_WORDS as STOP_WORDS_HI






file1 = open("nofor.txt")
text = file1.read()
words = text.split(" ")


cnt = Counter(words)

cnt.most_common(10)


nlp = stanza.Pipeline('hi', processors='tokenize,pos,lemma') 
sentence = open("nofor.txt").read()
doc = nlp(sentence)

lemma_all = []

# for token in doc:
#   print(token.text, token.norm_, token.orth_)
for sentence in doc.sentences:
     for word in sentence.words:
        lemma_all.append(word.lemma)



not_stop_words = [word for word in words if word not in set(STOP_WORDS_HI) ]


# non_stop_cnt = Counter(non_stop_words)
non_stop_cnt = Counter(not_stop_words)
LEMMA_ALL = Counter(lemma_all)


fdist = non_stop_cnt.most_common(30)
Lemma_all = LEMMA_ALL.most_common(30)

# print(fdist)



mpl.rcParams['font.sans-serif'] = ['Source Han Sans TW',
                                   'sans-serif',
                                   "Lohit Devanagari"  # fc-list :lang=hi family --> run in bash to check what fonts are supported
                                   ]


figure(num=None, figsize=(15, 6), dpi=80, facecolor='w', edgecolor='k')

fdist = FreqDist(lemma_all)
fdist.plot(30,cumulative=False)
plt.show()


