import pandas
import nltk, re
from nltk.stem.snowball import SnowballStemmer
import simplejson
import math
from collections import defaultdict, OrderedDict
stemmer = SnowballStemmer("dutch")

# import stopword list
General_corpus = open("C:/Your folder/general_corpus", errors='ignore')
Default_stopwords = open("C:/Your folder/nl.txt", errors='ignore')
# stopword list with words appears in the corpus that is only number
Numbers = open("C:/Your folder/onlynumber.txt", errors='ignore')
# stopword list of words that only appears once in the whole corpus
TF1 = open("C:/Your folder/TF1word.txt",errors = 'ignore')
General_corpus_striped = [line.rstrip('\n') for line in General_corpus]
Default_stopwords_striped = [line.rstrip('\n') for line in Default_stopwords]
Numbers_striped = [line.rstrip('\n') for line in Numbers]
TF1word = [line.rstrip('\n') for line in TF1]
stopwords = nltk.corpus.stopwords.words('dutch')
stopwords.extend(General_corpus_striped)
stopwords.extend(Default_stopwords_striped)
stopwords.extend(Numbers_striped)
stopwords.extend(TF1word)
# add custom stopwords here
stopwords.append('februari')

# here a list of tags extracted from stack overflow is created
Wordlist_SE = open("C:/Your folder/StackOverflowTags.txt", 'r')
Java_developer = pandas.read_csv("C:/Myler text/Java_developer.csv", sep=';')
skillname = [line.rstrip('\n') for line in Wordlist_SE]
Assignments = Java_developer['Fulltext']
Assignment = [line.rstrip('\n') for line in Assignments]
skills = list(skillname)

for skill in skills:
    skill = stemmer.stem(str(skill).lower())

# calculation of document length after processing the document
Doc_Len = dict()
for index, cv in enumerate(Assignment):
    cv = re.split(
        r"[' ' |\( | \) | \/ |,|;|: |\-|\"|\\ |\? |\• |\t |\n |\» |\« |\/|\(|\)|,|;|\.\s | \� "
        r"| \& | \! |\< |\> |\€ |\% |\~ |\= |\| |\` |\[ |\] |\… |\*|\_|\{]",
        cv
    )
    cv = [token.lower() for token in cv]
    cv = [stemmer.stem(token) for token in cv]
    Doc_Len[index] = len(cv)

AVG_DL = sum(Doc_Len) / len(Doc_Len)

term_frequency = defaultdict(int)

for index, cv in enumerate(Assignment):
    cur_term_frequency = defaultdict(int)
    TFn = dict()
    useful = []
    for a in cv:
        if a not in stopwords and a != '' and a in skills:
            useful.append(a)

    cv = useful
    for a in cv:
        cur_term_frequency[a] += 1

    for word, frequency in cur_term_frequency.items():
        TFn[word] = frequency * 2.75 / (1.75 * (0.25 + 0.75 * Doc_Len[index] / AVG_DL) + frequency)

    term_frequency[index] = TFn
    # uniqueness
    Assignment[index] = list(set(cv))

# DF calculation
DF = defaultdict(int)
for i in range(0, len(term_frequency)):
    for a in term_frequency[i]:
        DF[a] += 1

# IDF calculation
IDF = dict()
for cv in DF:
    IDF[cv] = math.log((len(term_frequency) - 1) / float(DF[cv]))

# new TF-IDF calculation
TFIDF = dict()
for i in range(0, len(term_frequency)):
    result = OrderedDict()
    for a in term_frequency[i]:
        result[a] = term_frequency[i][a] * IDF[a]
    TFIDF[i] = sorted(result.items(), key=lambda tup: tup[1])

with open('bm25withse.txt', 'w') as file:
    for frequencies in term_frequency:
        simplejson.dump(frequencies, file)
        file.write("\n")
