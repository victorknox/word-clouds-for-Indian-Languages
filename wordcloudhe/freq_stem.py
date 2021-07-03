
from collections import Counter
from spacy.lang.hi import Hindi
from spacy.lang.hi import STOP_WORDS as STOP_WORDS_HI
from nltk.tokenize import word_tokenize
from nltk.probability import FreqDist
import matplotlib.pyplot as plt
from nltk.tokenize import word_tokenize

from matplotlib.pyplot import figure
from matplotlib.font_manager import FontProperties
import matplotlib as mpl




file1 = open("nofor.txt")
text = file1.read()
words = text.split(" ")


cnt = Counter(words)

cnt.most_common(10)

stemt = []

sentence = open("text.txt").read()
nlp = Hindi()
doc = nlp(sentence)
for token in doc:
  stemt.append(token.norm_)




not_stop_words = [word for word in words if word not in set(STOP_WORDS_HI) ]


non_stop_cnt = Counter(not_stop_words)


fdist = non_stop_cnt.most_common(30)

# print(fdist)




mpl.rcParams['font.sans-serif'] = ['Source Han Sans TW',
                                   'sans-serif',
                                   "Lohit Devanagari"  # fc-list :lang=hi family --> run in bash to check what fonts are supported
                                   ]


figure(num=None, figsize=(15, 6), dpi=80, facecolor='w', edgecolor='k')




# print(tokenized_word)

fdist = FreqDist(stemt)
# print(fdist)
# print(fdist.most_common(2))

fdist.plot(30,cumulative=False)
plt.show()


