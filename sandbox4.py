from bs4 import BeautifulSoup
import requests


headers = {'User-Agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/74.0.3729.169 Safari/537.36'}

url = r'https://www.peterschroeter.info/impressum.html'
html = requests.get(url, headers=headers)
soup = BeautifulSoup(html.text, 'html.parser')


from nltk.tag.stanford import NERTagger
st = NERTagger('stanford-ner/all.3class.distsim.crf.ser.gz', 'stanford-ner/stanford-ner.jar')
text = soup.text

for sent in nltk.sent_tokenize(text):
    tokens = nltk.tokenize.word_tokenize(sent)
    tags = st.tag(tokens)
    for tag in tags:
        if tag[1]=='PERSON': print(tag)