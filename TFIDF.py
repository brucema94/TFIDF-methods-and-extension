# This is a project trying to calculate TFIDF score for assignments on Java_developers
import pandas
import nltk.corpus
import math
from collections import defaultdict, OrderedDict
import simplejson
from nltk.stem.snowball import SnowballStemmer
import regex as re

stemmer = SnowballStemmer("dutch")
java_dev_cv = pandas.read_csv("C:/Your folder/Java_developer.csv", sep=';')

# import stopword list (customized stopword list created in general_corpus_stripped)
general_corpus = open("C:/Your folder/general_corpus", errors='ignore')
general_corpus_stripped = [line.rstrip('\n') for line in general_corpus]
stopwords = nltk.corpus.stopwords.words('dutch')
stopwords.extend(general_corpus_stripped)


fulltext_cv = java_dev_cv['Fulltext']
individual_cv = [line.rstrip('\n') for line in fulltext_cv]  # remove unnecessary newlines

term_frequency = dict()
for index, cv in enumerate(individual_cv):
    cur_term_frequency = defaultdict(int)
    TFn = dict()
    cv = re.split(
        r"[' ' |\( | \) | \/ |,|;|: |\-|\"|\\ |\? |\• |\t |\n |\» |\« |\/|\(|\)|,|;|\.\s | \� | \& | \! |\< |\> |\€ |\%"
        r" |\~ |\= |\| |\` |\[ |\] |\… |\*|\_|\{]",
        cv
    )
    cv = [token.lower() for token in cv]
    cv = [stemmer.stem(token) for token in cv]
    useful = []
    for a in cv:
        if a not in stopwords and a != '' and bool(re.match('^[a-zA-Z0-9]+$', a)):
            useful.append(a)

    cv = useful
    for a in cv:
        cur_term_frequency[a] += 1

    for word, frequency in cur_term_frequency.items():
        TFn[word] = frequency / len(cv)

    term_frequency[index] = TFn

    # uniqueness
    individual_cv[index] = list(set(cv))

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

with open('TFIDF_without_bigram_snowball.txt', 'w') as file:
    for frequencies in term_frequency:
        simplejson.dump(frequencies, file)
        file.write("\n")
