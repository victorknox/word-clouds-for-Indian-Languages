from inltk.inltk import remove_foreign_languages

text = open("text_with_stop.txt").read()

print(remove_foreign_languages(text, 'hi'))