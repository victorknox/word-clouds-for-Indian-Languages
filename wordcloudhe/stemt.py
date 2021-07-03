from spacy.lang.hi import Hindi
Stc = open("stem_data.txt").read()
nlp = Hindi()
doc = nlp(Stc)
for token in doc:
  print(token.text, token.norm_)