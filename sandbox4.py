# -*- coding: utf-8 -*-

from bs4 import BeautifulSoup
import requests
import re

headers = {'User-Agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/74.0.3729.169 Safari/537.36'}

url = r'https://www.mobile-massagepraxis.de/kontakt/'
html = requests.get(url, headers=headers)
soup = BeautifulSoup(html.text, 'html.parser')
def getnames2(text):
    # pattern1 = r'(Festnetz*[.:\0-9-\s]+)'
    # pattern2 = r'(Handy*[.:\0-9-\s]+)'
    # pattern3 = r'(Telefon*[.:\0-9-\s]+)'
    # pattern4 = r'(Mobil*[.:\0-9-\s]+)'
    # pattern5 = r'(Tel*[.:\0-9-\s]+)'
    # pattern6 = r'(Fon*[.:\0-9-\s]+)'
    # pattern7 = r'(Telefax*[.:\0-9-\s]+)'
    # pattern8 = r'(Fax*[.:\0-9-\s]+)'
    # pattern9 = r'((\+)[.:\0-9-\s]+)'
    # pattern_list = [pattern9, pattern8, pattern7, pattern6, pattern5, pattern4, pattern3, pattern2, pattern1]
    # collected = []
    # for pattern in pattern_list:
    #da
    pattern1 = "([A-ZÄÖÜß][a-zäöü]+\s)(von|Von|da|Da|de|De|d'|du|Della|del|Del|della|di|y|Y'|[A-Z].)(\s[A-ZÄÖÜß][a-zäöü,]+|[A-ZÄÖÜß][a-zäöü,]+)" #Von/von--Good
    pattern2 = '([A-ZÄÖÜß][a-zäöüéàèéùâêîôûçëïü]+[- ][A-ZÄÖÜß][a-zäöüééàèùâêîôûçëïü]+)' #-- 2words
    pattern3 = '([A-ZÄÖÜß][a-zäöüééàèùâêîôûçëïü]+[- ][A-ZÄÖÜß][a-zäöüééàèùâêîôûçëïü]+[ -][A-ZÄÖÜß][a-zäöüéàèùâêîôûçëïü]+)' #--3words
    pattern4 = '([A-ZÄÖÜß][a-zäöüéàèùâêîôûçëïü]+ [- ][A-ZÄÖÜß][a-zäöüéàèéùâêîôûçëïü]+[ -][A-ZÄÖÜß][a-zäöüééàèùâêîôûçëïü]+[ -][A-ZÄÖÜß][a-zäöüéàèùâêîéôûçëïü]+)' #4words
    pat_regex = re.compile("|".join("({})".format(x) for x in [pattern4, pattern3, pattern2, pattern1]))
    matches = pat_regex.findall(text)
    #matches = re.findall(pattern, text)
    for_filter = list(set(matches))
    name = []
    #print(for_filter)
    for_filter2 = [list(set(x)) for x in for_filter if x]
    for elem in for_filter2:
        for sub in elem:
            if len(sub.split(' ')) > 1:
                name.append(sub)
    return name
print(getnames2(soup.text))
