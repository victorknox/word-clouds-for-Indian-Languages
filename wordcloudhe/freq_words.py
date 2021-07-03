from collections import Counter
from spacy.lang.hi import STOP_WORDS as STOP_WORDS_HI
from nltk.tokenize import word_tokenize
from nltk.probability import FreqDist

import matplotlib.pyplot as plt
from matplotlib.pyplot import figure
from matplotlib.font_manager import FontProperties
import matplotlib as mpl




file1 = open("nostop.txt")
text = file1.read()
# text = " ". join(paragraph)
words = text.split(" ")


cnt = Counter(words)

cnt.most_common(10)

not_stop_words = [word for word in words if word not in set(STOP_WORDS_HI) ]


# non_stop_cnt = Counter(non_stop_words)
non_stop_cnt = Counter(not_stop_words)


fdist = non_stop_cnt.most_common(30)
# print(fdist)



mpl.rcParams['font.sans-serif'] = ['Source Han Sans TW',
                                   'sans-serif',
                                   "Lohit Devanagari"  # fc-list :lang=hi family
                                   ]

# figure(num=None, figsize=(15, 6), dpi=80, facecolor='w', edgecolor='k')

figure(num=None, figsize=(15, 6), dpi=80, facecolor='w', edgecolor='k')
a = list.copy(fdist)
b = dict(a)


val_val = b.values()
key_val = b.keys()
plt.bar(key_val,val_val)
plt.show()