from bs4 import BeautifulSoup
import requests


headers = {'User-Agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/74.0.3729.169 Safari/537.36'}

url = r'https://www.mobile-massagepraxis.de/impressum/'
html = requests.get(url, headers=headers)
soup = BeautifulSoup(html.text, 'html.parser')

#misc.get_names()

import nltk
from nltk.corpus import wordnet


person_list = []
person_names=person_list
def get_human_names(text):
    tokens = nltk.tokenize.word_tokenize(text)
    pos = nltk.pos_tag(tokens)
    sentt = nltk.ne_chunk(pos, binary = False)

    person = []
    name = ""
    for subtree in sentt.subtrees(filter=lambda t: t.label() == 'PERSON'):
        for leaf in subtree.leaves():
            person.append(leaf[0])
        if len(person) > 1: #avoid grabbing lone surnames
            for part in person:
                name += part + ' '
            if name[:-1] not in person_list:
                person_list.append(name[:-1])
            name = ''
        person = []
#     print (person_list)

names = get_human_names(soup.text)
for person in person_list:
    person_split = person.split(" ")
    for name in person_split:
        if wordnet.synsets(name):
            if(name in person):
                person_names.remove(person)
                break

print(person_names)
