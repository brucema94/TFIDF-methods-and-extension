import pandas
import re
import nltk.corpus
import math
import operator
from nltk.stem.snowball import SnowballStemmer
import simplejson

stemmer = SnowballStemmer("dutch")
# in this example the entire corpus consist 4 classes
Java_developer = pandas.read_csv("C:/Myler text/Java_developer.csv", sep=';')
Project_Leader = pandas.read_csv("C:/Myler text/Project_Leader.csv", sep=';')
SoftwareTesters = pandas.read_csv("C:/Myler text/SoftwareTesters.csv", sep=';')
System_Administrator = pandas.read_csv("C:/Myler text/System_Administrator.csv", sep=';')


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
Wordlist_SE = open("C:/Myler text/StackOverflowTags.txt", 'r')
skillname = [line.rstrip('\n') for line in Wordlist_SE]
skills = list(skillname)

for skill in skills:
    skill = stemmer.stem(str(skill).lower())

Assignment = Java_developer['Fulltext']
Project_Leader_Assignment = Project_Leader['FullText']
SoftwareTesters_Assignment = SoftwareTesters['FullText']
System_Administrator_Assignment = System_Administrator['FullText']

Java_developer_assignments = [line.rstrip('\n') for line in Assignment]
ProjectLeaderAssignment = [line.rstrip('\n') for line in Project_Leader_Assignment]
SoftwareTesterAssignment = [line.rstrip('\n') for line in SoftwareTesters_Assignment]
SystemAdministratorAssignment = [line.rstrip('\n') for line in System_Administrator_Assignment]

# TF calculation with Java developer
TF = dict()
TF_individual = dict()
TF_for_avg = dict()
for i in range(0, len(Java_developer_assignments) - 1):
    TFi = dict()
    TFn = dict()
    Java_developer_assignments[i] = re.split(
        r"[' ' |\( | \) | \/ |\,|\;|\:|\-|\"|\\|\?|\•|\t|\n|\»|\«|\/|\(|\)|\."
        r"|\�|\&|\!|\<|\>|\%|\~|\=|\||\`|\[|\]|\…|\*|\_|\{]+",
        Java_developer_assignments[i]
    )
    Java_developer_assignments[i] = [token.lower() for token in Java_developer_assignments[i]]
    Java_developer_assignments[i] = [stemmer.stem(token) for token in Java_developer_assignments[i]]
    useful = []
    for a in Java_developer_assignments[i]:
        if a in stopwords or a == '':
            pass
        elif a in skills:
            useful.append(a)
    Java_developer_assignments[i] = useful
    for a in Java_developer_assignments[i]:
        if a in TFi:
            TFi[a] += 1
        else:
            TFi[a] = 1

        if a not in TF_for_avg:
            TF_for_avg[a] = 1
        else:
            TF_for_avg[a] += 1

        for x in TFi:
            TFn[x] = TFi[x] / len(Java_developer_assignments[i])

    TF[i] = TFn

    TF_individual[i] = TFi

# DF calculation
DF = dict()
for i in range(0, len(TF)):
    for a in TF[i]:
        if a in DF:
            DF[a] += 1
        else:
            DF[a] = 1

# IDF calculation
IDF = dict()
for word in DF:
    IDF[word] = math.log((len(TF) - 1) / float(DF[word]))

# calculation of total length Java
total_length_Java = 0
for i in range(0, len(Java_developer_assignments) - 1):
    total_length_Java += len(Java_developer_assignments[i])

# calculation of average term freq for Java
TF_avg_Java = dict()
for a in TF_for_avg:
    TF_avg_Java[a] = TF_for_avg[a] / total_length_Java

# total term freq for project leader
TF_projectleader = dict()
for i in range(0, len(ProjectLeaderAssignment) - 1):
    ProjectLeaderAssignment[i] = re.split(
        r"[' ' |\( | \) | \/ |\,|\;|\:|\-|\"|\\|\?|\•|\t|\n|\»|\«|\/|\(|\)|\."
        r"|\�|\&|\!|\<|\>|\%|\~|\=|\||\`|\[|\]|\…|\*|\_|\{]+",
        ProjectLeaderAssignment[i]
    )
    ProjectLeaderAssignment[i] = [token.lower() for token in ProjectLeaderAssignment[i]]
    ProjectLeaderAssignment[i] = [stemmer.stem(token) for token in ProjectLeaderAssignment[i]]
    useful = []
    for a in ProjectLeaderAssignment[i]:
        if a in stopwords or a == '':
            next
        elif a in skills:
            useful.append(a)
    ProjectLeaderAssignment[i] = useful
    for a in ProjectLeaderAssignment[i]:
        if a not in TF_projectleader:
            TF_projectleader[a] = 1
        else:
            TF_projectleader[a] += 1


            # calculation of total length ProjectLeader
total_length_ProjectLeader = 0
for i in range(0, len(ProjectLeaderAssignment) - 1):
    total_length_ProjectLeader += len(ProjectLeaderAssignment[i])

# calculation of average term freq for ProjectLeader
TF_avg_ProjectLeader = dict()
for a in TF_projectleader:
    TF_avg_ProjectLeader[a] = TF_projectleader[a] / total_length_ProjectLeader

# total term freq for softwareTester
TF_SoftwareTester = dict()
for i in range(0, len(SoftwareTesterAssignment) - 1):
    SoftwareTesterAssignment[i] = re.split(
        r"[' ' |\( | \) | \/ |\,|\;|\:|\-|\"|\\|\?|\•|\t|\n|\»|\«|\/|\(|\)|\."
        r"|\�|\&|\!|\<|\>|\%|\~|\=|\||\`|\[|\]|\…|\*|\_|\{]+",
        SoftwareTesterAssignment[i]
    )
    SoftwareTesterAssignment[i] = [token.lower() for token in SoftwareTesterAssignment[i]]
    SoftwareTesterAssignment[i] = [stemmer.stem(token) for token in SoftwareTesterAssignment[i]]

    useful = []
    for a in SoftwareTesterAssignment[i]:
        if a in stopwords or a == '':
            next
        elif a in skills:
            useful.append(a)
    SoftwareTesterAssignment[i] = useful
    for a in SoftwareTesterAssignment[i]:
        if a not in TF_SoftwareTester:
            TF_SoftwareTester[a] = 1
        else:
            TF_SoftwareTester[a] += 1


            # calculation of total length SoftwareTester
total_length_SoftwareTester = 0
for i in range(0, len(SoftwareTesterAssignment) - 1):
    total_length_SoftwareTester += len(SoftwareTesterAssignment[i])

# calculation of average term freq for SoftwareTester
TF_avg_SoftwareTester = dict()
for a in TF_SoftwareTester:
    TF_avg_SoftwareTester[a] = TF_SoftwareTester[a] / total_length_SoftwareTester

# total term freq for systemAdministrator
TF_SystemAdministrator = dict()
for i in range(0, len(SystemAdministratorAssignment) - 1):
    SystemAdministratorAssignment[i] = re.split(
        r"[' ' |\( | \) | \/ |\,|\;|\:|\-|\"|\\|\?|\•|\t|\n|\»|\«|\/|\(|\)|\."
        r"|\�|\&|\!|\<|\>|\%|\~|\=|\||\`|\[|\]|\…|\*|\_|\{]+",
        SystemAdministratorAssignment[i]
    )
    SystemAdministratorAssignment[i] = [token.lower() for token in SystemAdministratorAssignment[i]]
    SystemAdministratorAssignment[i] = [stemmer.stem(token) for token in SystemAdministratorAssignment[i]]
    useful = []
    for a in SystemAdministratorAssignment[i]:
        if a in stopwords or a == '':
            pass
        elif a in skills:
            useful.append(a)
    SystemAdministratorAssignment[i] = useful
    for a in SystemAdministratorAssignment[i]:
        if a not in TF_SystemAdministrator:
            TF_SystemAdministrator[a] = 1
        else:
            TF_SystemAdministrator[a] += 1



# calculation of total length SystemAdministrator
total_length_SystemAdministrator = 0
for i in range(0, len(SystemAdministratorAssignment) - 1):
    total_length_SystemAdministrator += len(SystemAdministratorAssignment[i])

# calculation of average term freq for SystemAdministrator
TF_avg_SystemAdministrator = dict()
for a in TF_SystemAdministrator:
    TF_avg_SystemAdministrator[a] = TF_SystemAdministrator[a] / total_length_SystemAdministrator

# calculation for inter class weight "De"
total_average_TF = dict()
for a in TF_avg_Java:
    if a not in TF_avg_ProjectLeader:
        TF_avg_ProjectLeader[a] = 0
    if a not in TF_avg_SoftwareTester:
        TF_avg_SoftwareTester[a] = 0
    if a not in TF_avg_SystemAdministrator:
        TF_avg_SystemAdministrator[a] = 0

    total_average_TF[a] = (TF_avg_Java[a] + TF_avg_ProjectLeader[a] + TF_avg_SoftwareTester[a] +
                           TF_avg_SystemAdministrator[a]) / 4

interclass_weight = dict()
for a in total_average_TF:
    interclass_weight[a] = ((TF_avg_Java[a] - total_average_TF[a]) ** 2 + (
    TF_avg_ProjectLeader[a] - total_average_TF[a]) ** 2 + (TF_avg_SoftwareTester[a] - total_average_TF[a]) ** 2 + (
                            TF_avg_SystemAdministrator[a] - total_average_TF[a]) ** 2) / 4

# for intraclass calculation "Di"
avg_tf_java = dict()
for a in TF_avg_Java:
    for i in range(0, len(Java_developer_assignments) - 1):
        if a not in TF[i]:
            TF[i][a] = 0
        if a not in avg_tf_java:
            avg_tf_java[a] = TF[i][a] / len(Java_developer_assignments)
        else:
            avg_tf_java[a] += TF[i][a] / len(Java_developer_assignments)

intraclass_weight = dict()
square_weight = dict()
for a in TF_avg_Java:
    for i in range(0, len(Java_developer_assignments) - 1):
        if a not in intraclass_weight:
            intraclass_weight[a] = (TF[i][a] - avg_tf_java[a]) ** 2 / len(Java_developer_assignments)
            square_weight[a] = (TF[i][a]) ** 2 / len(Java_developer_assignments)
        else:
            intraclass_weight[a] += (TF[i][a] - avg_tf_java[a]) ** 2 / len(Java_developer_assignments)
            square_weight[a] += (TF[i][a]) ** 2 / len(Java_developer_assignments)

normalized_intraclass_weight = dict()
for a in intraclass_weight:
    normalized_intraclass_weight[a] = intraclass_weight[a] / square_weight[a]

# new TF-IDF calculation
TFIDF = dict()
for i in range(0, len(TF)):
    result = dict()
    for a in TF[i]:
        if TF[i][a] != 0:
            result[a] = TF[i][a] * IDF[a] * (1 - intraclass_weight[a]) * interclass_weight[a]
    TFIDF[i] = result

TFIDFFinal = dict()
for i in range(0, len(TFIDF)):
    a = dict()
    a = sorted(TFIDF[i].items(), key=operator.itemgetter(1))
    TFIDFFinal[i] = a

with open('TFIDF-De-Di.txt', 'w') as file:
    for frequencies in TF:
        simplejson.dump(frequencies, file)
        file.write("\n")

