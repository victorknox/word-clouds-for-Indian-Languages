import re
import requests
from bs4 import BeautifulSoup
import nltk
from nltk.tokenize import sent_tokenize, word_tokenize
import string
import wxconv
from wxconv import WXC
con = WXC(order='utf2wx',lang='mal')
bac = WXC(order='wx2utf',lang='mal')

nltk.download('punkt')
nltk.download('wordnet')

punct = ['[',']',',','.',':',';',"'",'"','(',')','!','?','-','/','%','‘','’','“','”','_'] + [str(i) for i in list(range(10))]
punct_eng = punct + list(string.ascii_letters)

def translit(con,s):
    return con.convert(s).replace("ൽ",'l').replace("ൻ",'n').replace("ർ",'r').replace("ൾ",'lY')
  
def translit_back(bac,s):
    return bac.convert(s).replace('l',"ൽ").replace('n',"ൻ").replace('r',"ർ").replace('lY',"ൾ")

def stem(w):
    for e in endings:
        w = re.sub(e,'',w)
    return w

mal_stopwords = ['ഞാൻ', 'എന്നെ','എനിക്ക്','എനിക്കു','എന്റെ','എന്നിൽ','എന്നാൽ','എന്നോട്','എന്നോടു',
                 'നീ','നിന്നെ','നിനക്ക്','നിനക്കു','നിന്റെ','നിന്നിൽ','നിന്നാൽ','നിന്നോട്','നിന്നോടു',
                 'അവൻ','അവനെ','അവന്','അവനു','അവന്റെ','അവനിൽ','അവനാൽ','അവനോട്','അവനോടു',
                 'അവൾ','അവളെ','അവൾക്ക്','അവൾക്കു','അവളുടെ','അവളിൽ','അവളാൽ','അവളോട്','അവരോടു',
                 'അത്','അതു','അതിന്','അതിനു','അതിന്റെ','അതിൽ','അതിൽ','അതിനാൽ','അതിനോട്','അതിനോടു',
                 'ഇവൻ','ഇവനെ','ഇവന്','ഇവനു','ഇവന്റെ','ഇവനിൽ','ഇവനാൽ','ഇവനോട്','ഇവനോടു',
                 'ഇവൾ','ഇവളെ','ഇവൾക്ക്','ഇവൾക്കു','ഇവളുടെ','ഇവളിൽ','ഇവളാൽ','ഇവളോട്','ഇവളോടു',
                 'ഇത്','ഇതു','ഇതിന്','ഇതിനു','ഇതിന്റെ','ഇതിൽ','ഇതിൽ','ഇതിനാൽ','ഇതിനോട്','ഇതിനോടു',
                 'ഞങ്ങൾ','ഞങ്ങളെ','ഞങ്ങൾക്ക്','ഞങ്ങൾക്കു','ഞങ്ങളുടെ','ഞങ്ങളിൽ','ഞങ്ങളാൽ','ഞങ്ങളോട്','ഞങ്ങളോടു',
                 'നമ്മൾ','നമ്മളെ','നമുക്ക്','നമുക്കു','നമ്മളുടെ','നമ്മളിൽ','നമ്മളാൽ','നമ്മളോട്','നമ്മളോടു',
                 'നിങ്ങൾ','നിങ്ങളെ','നിങ്ങൾക്ക്','നിങ്ങൾക്കു','നിങ്ങളുടെ','നിങ്ങളിൽ','നിങ്ങളാൽ','നിങ്ങളോട്','നിങ്ങളോടു',
                 'അവർ','അവരെ','അവർക്ക്','അവർക്കു','അവരുടെ','അവരിൽ','അവരാൽ','അവരോട്','അവരോടു',
                 'അദ്ദേഹം','അദ്ദേഹത്തെ','അദ്ദേഹത്തിന്','അദ്ദേഹത്തിനു','അദ്ദേഹത്തിന്റെ','അദ്ദേഹത്തിൽ','അദ്ദേഹത്താൽ',
                 'അദ്ദേഹത്തോട്','അദ്ദേഹത്തോടു',
                 'ഇവർ','ഇവരെ','ഇവർക്ക്','ഇവർക്കു','ഇവരുടെ','ഇവരിൽ','ഇവരാൽ','ഇവരോട്','ഇവരോടു',
                 'ഇദ്ദേഹം','ഇദ്ദേഹത്തെ','ഇദ്ദേഹത്തിന്','ഇദ്ദേഹത്തിനു','ഇദ്ദേഹത്തിന്റെ','ഇദ്ദേഹത്തിൽ','ഇദ്ദേഹത്താൽ',
                 'ഇദ്ദേഹത്തോട്','ഇദ്ദേഹത്തിനോടു',
                 'നിന്നു','നിന്ന്','നിന്നും','കൊണ്ട്','വരെ','മുതൽ',
                 'ആണ്','ആണു','ഉണ്ട്','ഉണ്ടു','ആയിരുന്നു','ആകുന്നു','ആകും',
                 'മാത്രം','ശേഷം','തന്നെ',
                 'പിന്നെ','മുമ്പെ','മുന്നിൽ','പിന്നാലെ','താഴെ','മുകളിൽ','പറകെ','പിന്നീട്','ഏറ്റവും','കൂടുതൽ',
                 'എന്ത്','എവിടെ','ആര്','എങ്ങോട്ട്','എങ്ങനെ','എങ്ങനത്തെ','ഏത്','എപ്പോൾ',
                 'വേണം','വേണ്ട',
                 'ഈ','ആ','ഇവിടെ','അവിടെ','ഇങ്ങോട്ട്','ഇങ്ങോട്ടു','അങ്ങോട്ട്','അങ്ങോട്ടു','ഇങ്ങനെ','അങ്ങനെ',
                 'ഇങ്ങനത്തെ','അങ്ങനത്തെ','ഇപ്പോൾ','അപ്പോൾ',
                 'നും','ഒരു','എന്നു','എന്ന്','എന്നാണ്','എന്ന','എന്നീ','എന്നിവ','എന്നിവയാണ്','എന്നും','തുടങ്ങിയ',
                 'മറ്റു','സ്വന്തം','ചില','എല്ലാ','ഓരോ','വളരെ','തന്റെ',
                 'ചെയ്യുന്നു','ചെയ്തു']
mal_stopwords_tr = [translit(con,w) for w in mal_stopwords]

endings = [r'ulYlYa(w(u?))?$',r'Aya(w(u?))?$',r'Ayi$',r'ANu?$',r'A(n|M)$',r'uka$',r'(a|e)Nta$',r'aNaM$',
           r'Aw((eV)|(wa))$',r'uM$',r'[^(Ayir)]unnu$',r'v?u(M|m)$',r'(M|m)$',r'y?uteV$',r'((ww)|y)?eV$',
           r'(ww)?inrYeV$',r'y?kku?$',r'(ww)?inu?$',r'ww$',r'((ww)|y)?il(eV)?$',r'((ww)|y)?oTu?$',
           r'(k|(ff))alY$',r'n$']

def anc(t):
    ancestors = []
    prev = t.parent
    while prev != None:
        ancestors.append(prev.name)
        prev = prev.parent
    
    return ancestors

def crawl(url):
    res = requests.get(url)
    html_page = res.content

    soup = BeautifulSoup(html_page, 'html.parser')
    text = soup.find_all(text=True)

    output = ''
    extractlist = ['p','em','b','i','strong','a']

    for t in text:
        a = anc(t)
        if 'cite' not in a and 'table' not in a and 'p' in a:
            if t.parent.name in extractlist and format(t) != 'Navigation menu':
                output += " " + format(t)
            elif t.parent.name == 'a' and 'wiki' in t.parent('href'):
                output += format(t)
    
    output = re.sub(r'\s+', " ", output.replace("\n"," ").replace("`", "'").replace(" .", ".").replace(" ,", ","))
    
    return output
  
wikilinks = ['കേരളം','ആലപ്പുഴ_ജില്ല','എറണാകുളം_(ജില്ല)','ഇടുക്കി_(ജില്ല)','കൊല്ലം_(ജില്ല)','കണ്ണൂർ_(ജില്ല)','കാസർഗോഡ്_(ജില്ല)','കോട്ടയം_(ജില്ല)','കോഴിക്കോട്_(ജില്ല)','മലപ്പുറം_(ജില്ല)',
             'പാലക്കാട്_(ജില്ല)','പത്തനംതിട്ട_(ജില്ല)','തൃശ്ശൂർ_(ജില്ല)','തിരുവനന്തപുരം_(ജില്ല)','വയനാട്_(ജില്ല)','ആലപ്പുഴ','എറണാകുളം','പൈനാവ്','കൊല്ലം','കണ്ണൂർ','കാസർഗോഡ്',
             'കോട്ടയം','കോഴിക്കോട്','മലപ്പുറം','പാലക്കാട്','പത്തനംതിട്ട','തൃശ്ശൂർ','തിരുവനന്തപുരം','കൽപറ്റ','വടക്കേ_മലബാർ','തെക്കേ_മലബാർ','കൊച്ചി','തെക്കൻ_തിരുവിതാംകൂർ',
             'മയ്യഴി','പെരിയാർ','ഭാരതപ്പുഴ','പമ്പാ_നദി','നെയ്യാർ','മയ്യഴിപ്പുഴ','മലയാളം_വിക്കിപീഡിയ','മലയാളം','മലയാളം_വിക്കിപീഡിയ','മലയാളം','കേരളചരിത്രം','മണിപ്രവാളം',
             'തുഞ്ചത്തെഴുത്തച്ഛൻ','അദ്ധ്യാത്മരാമായണം_കിളിപ്പാട്ട്','ദ്രാവിഡ_ഭാഷകൾ','ഇന്ത്യ','ആന്ധ്രാ_പ്രദേശ്','അരുണാചൽ_പ്രദേശ്','ആസാം','ബീഹാർ','ഛത്തീസ്ഗഡ്','ഗോവ','ഗുജറാത്ത്',
             'ഹരിയാന','ഹിമാചൽ_പ്രദേശ്','ഝാർഖണ്ഡ്','കർണാടക','മധ്യപ്രദേശ്','മഹാരാഷ്ട്ര','മണിപ്പൂർ','മേഘാലയ','മിസോറം','നാഗാലാൻഡ്','ഒറീസ്സ','പഞ്ചാബ്','രാജസ്ഥാൻ','സിക്കിം',
             'തമിഴ്നാട്','ത്രിപുര','ഉത്തരാഖണ്ഡ്','ഉത്തർപ്രദേശ്','പശ്ചിമ_ബംഗാൾ','തെലംഗാണ','ആൻഡമാൻ_നിക്കോബാർ_ദ്വീപുകൾ','ചണ്ഢീഗഡ്','ദാദ്ര,_നഗർ_ഹവേലി','ദമൻ,_ദിയു','ലക്ഷദ്വീപ്',
             'ഡൽഹി','പുതുച്ചേരി','ജമ്മു-കശ്മീർ','ലഡാക്','ഭാരതത്തിലെ_ഔദ്യോഗിക_ഭാഷകൾ','ആസ്സാമീസ്','ബംഗാളി_ഭാഷ','ബോഡോ','ദോഗ്രി','ഗുജറാത്തി_ഭാഷ','ഹിന്ദി','കന്നഡ',
             'കശ്മീരി_ഭാഷ','കൊങ്കണി_ഭാഷ','മൈഥിലി_ഭാഷ','മണിപ്പൂരി_ഭാഷ','മറാഠി_ഭാഷ','നേപ്പാളി_ഭാഷ','ഒഡിയ','പഞ്ചാബി_ഭാഷ','സംസ്കൃതം','സന്താലി_ഭാഷ','സിന്ധി_ഭാഷ',
             'തമിഴ്','തെലുഗു_ഭാഷ','ഉർദു','മിസോ_ഭാഷ','ചെമ്മീൻ_(ചലച്ചിത്രം)','ചെമ്മീൻ_(നോവൽ)','കയർ_(നോവൽ)','തകഴി_ശിവശങ്കരപ്പിള്ള','കുമാരനാശാൻ','കമല_സുറയ്യ','രണ്ടാമൂഴം',
             'കാലം_(നോവൽ)','എം.ടി._വാസുദേവൻ_നായർ','വൈക്കം_മുഹമ്മദ്_ബഷീർ','പ്രേമലേഖനം_(നോവൽ)','ബാല്യകാലസഖി','ശബ്ദങ്ങൾ_(നോവൽ)','ന്റുപ്പൂപ്പാക്കൊരാനേണ്ടാർന്ന്',
             'പാത്തുമ്മായുടെ_ആട്','മതിലുകൾ_(നോവൽ)','മമ്മൂട്ടി','മോഹൻലാൽ','ദുൽഖർ_സൽമാൻ','നിവിൻ_പോളി','പൃഥ്വിരാജ്','ഫഹദ്_ഫാസിൽ','നസ്രിയ_നസീം','ബാംഗ്ലൂർ_ഡെയ്സ്',
             'പ്രേംനസീർ','ഷീല','മധു_(നടൻ)','സത്യൻ']

### Crawling ###
raw = ''
i = 1
for link in wikilinks:
    raw += crawl("https://ml.wikipedia.org/wiki/" + link) + ' '
    print("Scraped https://ml.wikipedia.org/wiki/" + link)
raw_tr = translit(con,raw)
### Now the raw data is obtained. Sentence and word tokenisation and cleaning are left. ###

### File Writing and Reading ###
with open('raw.txt','w') as r:
    print(raw, file=r)
with open('raw_tr.txt','w') as r:
    print(raw_tr, file=r)

filename = input("Enter name of file with raw data in Malayalam: ")
with open(filename,'r') as rawfile:
    raw = rawfile.read()
### The raw data is now ready to be processed. ###

print("Raw data ready")

### Tokenisation ###
sentences = sent_tokenize(raw)
sentences_tr = sent_tokenize(raw_tr)
words = word_tokenize(raw)
words_tr = word_tokenize(raw_tr)
### Now a list of sentences and a list of words are obtained. The latter will next be cleaned. ###

print("Data tokenised")

### Cleaning ###
cleaned_words = [w for w in words if all(p not in w for p in punct_eng)] # words with punctuation etc removed
cleaned_words_tr = [w for w in words_tr if all(p not in w for p in punct)]
### Now we have a list of words without punctuation, abbreviation, symbols or foreign words. ###

print("Data cleaned")

### Removing Stopwords ###
unstop_words = [w for w in cleaned_words if not w in mal_stopwords and len(w) > 2]
unstop_words_tr = [w for w in cleaned_words_tr if not w in mal_stopwords_tr and len(w) > 2]
### Now we have a list without stopwords. ###

print("Stopwords removed")

### POS Tagging ###

### Stemming ###
stems_tr = [stem(w) for w in unstop_words_tr if len(stem(w)) > 0]
stems = [bac.convert(w) for w in stems_tr]
### Now we have a rudimentarily stemmed list. ###

print("Data stemmed")

fd_words = nltk.FreqDist(words_tr)
fd_words.plot(20, title="Unprocessed Wordlist Frequencies")

fd_cleaned = nltk.FreqDist(cleaned_words_tr)
fd_cleaned.plot(20, title="Cleaned Wordlist Frequencies")

fd_unstop = nltk.FreqDist(unstop_words_tr)
fd_unstop.plot(20, title="Unstop Wordlist Frequencies")

fd_stems = nltk.FreqDist(stems_tr)
fd_stems.plot(20, title="Stem Frequencies")


with open('mostcommon_tr.txt','w') as m:
    for w,f in fd_unstop.most_common(50):
        print(w + ' - ' + str(f), file=m)

with open('mostcommon.txt','w') as m:
    for w,f in fd_unstop.most_common(50):
        print(translit_back(bac,w) + ' - ' + str(f), file=m)
