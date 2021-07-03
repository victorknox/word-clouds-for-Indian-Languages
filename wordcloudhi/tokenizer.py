from inltk.inltk import tokenize

hindi_text = open("nofor.txt").read()

print(tokenize(hindi_text, "hi"))


