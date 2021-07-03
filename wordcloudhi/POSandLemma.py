import stanza

nlp = stanza.Pipeline('hi', processors='tokenize,pos,lemma') 
sentence = open("nofor.txt").read()
doc = nlp(sentence)
# for token in doc:
#   print(token.text, token.norm_, token.orth_)
for sentence in doc.sentences:
     for word in sentence.words:
         print("{:12s}\t{:12s}\t{:6s}".format(word.text, word.lemma, word.upos)) 

