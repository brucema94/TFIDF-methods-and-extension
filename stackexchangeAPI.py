import stackexchange
Wordlist_SE = open("C:/Myler text/StackOverflowTags.txt",'r')
skillname = [line.rstrip('\n') for line in Wordlist_SE]
skills = list(skillname)

# the number in the range is changed every time you run it, and the key below need to change every day after the limit reset
# you can register a stack app on https://stackapps.com/apps/oauth/register#_=_ to boost your daily limit to 10000 instead of
# the default 100.

so = stackexchange.Site(stackexchange.StackOverflow, 't2KSUTfrdmFsqooEwCpjFQ((')
tags = so.tag

# here the synonymlist is created with a set range, however due to the fact that stackexchange API
# has a daily limit of 10000 usage, the extraction is done in a week.
synonymsList = dict()

for i in range(53000,53803):
        entry = str(skills[i])
        try:
                fetch = tags(entry).synonyms.fetch()
                synonyms = []
                for x in fetch:
                        synonyms.append(x.from_tag)
                synonymsList[entry] = synonyms
        except:
                pass

import csv
with open('synonyms54.csv', 'w', newline='') as csvfile:
        spamwriter = csv.writer(csvfile, quoting=csv.QUOTE_ALL)
        spamwriter.writerow(synonymsList.keys())
        spamwriter.writerow(synonymsList.values())