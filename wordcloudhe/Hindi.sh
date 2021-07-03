#!bin/bash


# corpus collection, cleaning and sentence tokenization
python3 crawl.py > text_with_stop.txt                   # corpus collection from <p> tags in wikipedia
python3 removefor.py > nofor.txt                        # remove foreign words from the collected corpus
python3 punctuation.py                                  # removes all the punctuations from the file

# word tokenization, POS tagging, stopwords removal, stemming and lemmatization
python3 tokenizer.py > tokens.txt                       # tokenizes the words and stores in tokens.txt
python3 POSandLemma.py > POSandLemma.txt                # does POS tagging and lemmatization on nofor.txt
python3 stopwords.py > nostop.txt                       # removes stopwords and stores data in nostop.txt
python3 nostop_wc.py > nostop_wc.txt                    # supply text for wordcloud
python3 punctuation_wc.py                               # supply text to wordcloud without punctuations
python3 stemt.py > stemt.txt                            # stemming of words in stem_data.txt and putting it in stemt.txt

# frequency graphs, wordcloud
python3 freq_withstop.py                                # plots frequency graph of text_with_stop.txt  
python3 freq_words.py                                   # plots frequency graph of nostop.txt
python3 freq_POS.py                                     # plots POS freq graph of nofor.txt
python3 freq_stem.py                                    # plots stem freq graph for nostop.txt      
python3 freq_lemma.py                                   # plots lemma freq graph for nostop.txt
python3 wc.py                                           # plots a wordcloud of nostop.txt                                   