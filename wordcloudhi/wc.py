from wordcloud import WordCloud
from spacy.lang.hi import STOP_WORDS as STOP_WORDS_HI

import matplotlib.pyplot as plt
from collections import Counter

file1 = open("nostop_wc.txt")
text = file1.read()
words = text.split(" ")

not_stop_words = [word for word in words if word not in set(STOP_WORDS_HI) ]

non_stop_cnt = Counter(not_stop_words)

# print(non_stop_cnt.most_common(15))

wordcloud = WordCloud(font_path="Lohit-Devanagari.ttf",
    width=400,
    height=300,
    max_font_size=80, 
    max_words=50,
    background_color="white", 
    stopwords=STOP_WORDS_HI,
    regexp=r"[\u0900-\u097F]+"
).fit_words(non_stop_cnt)

# print(text)
plt.figure()
plt.imshow(wordcloud)

plt.axis("off")
plt.show()

