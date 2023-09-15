import time
import os
from pathlib import Path
import pandas as pd
import re
import requests
from bs4 import BeautifulSoup
import nltk
from nltk.corpus import wordnet

def istellnumber(string):
        int_list = ['0', '1', '2', '3', '4', '5', '6', '7', '8', '9', ',', '.', ' ', '+', '(', ')']
        return all([(x in int_list) for x in string])
#print(istellnumber(string_))
def isOpen(string):
        test1 = (string.lower()).find('open')
        test2 = (string.lower()).find('close')
        if test1 == -1 or test2 == -1:
                return False
        else:
                return True
#print(isOpen(string_))
def writelogs():
    filename_date = time.strftime("%Y%m%d%H%M%S", time.localtime())
    script_dir = Path(os.path.dirname(__file__))  # <-- absolute dir the script is in
    rel_path = Path(r"/Logs/" + 'Logs_' + filename_date + '.out')
    new_file = script_dir.joinpath(*rel_path.parts[1:])
    #abs_file_path = os.path.join(script_dir, rel_path)
    return new_file
def write_excel_path(file):
    filename_date = time.strftime("_%Y%m%d%H%M%S", time.localtime())
    script_dir = Path(os.path.dirname(__file__))  # <-- absolute dir the script is in
    rel_path = Path(r"/Done_Run/" + file + filename_date + '.xlsx')
    new_file = script_dir.joinpath(*rel_path.parts[1:])
    #abs_file_path = os.path.join(script_dir, rel_path)
    return new_file
#print(write_excel_path('file'))

def isbusiness(wd, wait, EC, By, NSE):
    try:
        if wd.find_element(By.CLASS_NAME, 'YzSd').text == 'Businesses':
            return True
        else:
            return False
    except NSE:
        return False


def business(soup):
    for found in soup.findAll('div', class_='YzSd'):
        if found.text == 'Businesses':
            print("Business!")
            return True
    print('Not Business!')
    return False
#CAYQGA
#YzSd

def file_(file):
    script_dir = Path(os.path.dirname(__file__))  # <-- absolute dir the script is in
    rel_path = Path("/For_Run/" + file)
    #abs_file_path = os.path.join(script_dir, rel_path)
    new_file = script_dir.joinpath(*rel_path.parts[1:])
    return new_file
def read_xlsx(file):
    data = pd.read_excel(file_(file))
    #print(data['Keyword'])
    return data['Keyword']

# - Kontakt
# - Über uns
# - Über mich
# - Impressum

def find_email(html):
    email_pattern = r"[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,4}"
    emails = re.findall(email_pattern, html)
    print('Emails')
    print(emails)
    return emails

def getcontactnumbers(text):
    pattern1 = r'(Festnetz*[.:\0-9-\s]+)'
    pattern2 = r'(Handy*[.:\0-9-\s]+)'
    pattern3 = r'(Telefon*[.:\0-9-\s]+)'
    pattern4 = r'(Mobil*[.:\0-9-\s]+)'
    pattern5 = r'(Tel*[.:\0-9-\s]+)'
    pattern6 = r'(Fon*[.:\0-9-\s]+)'
    pattern7 = r'(Telefax*[.:\0-9-\s]+)'
    pattern8 = r'(Fax*[.:\0-9-\s]+)'
    pattern9 = r'((\+)[.:\0-9-\s]+)'
    pattern_list = [pattern9, pattern8, pattern7, pattern6, pattern5, pattern4, pattern3, pattern2, pattern1]
    collected = []
    for pattern in pattern_list:
        matches = re.findall(pattern, text, flags=re.IGNORECASE)
        valid_search = [valid for valid in matches if valid != []]
        for match in valid_search:
            if len(match) > 9:
                collected.append(match)
        #collected.append(valid_search)
    print('Numbers')
    print(collected)
    return collected

#Handy: - done
#Telefon - done
#Mobil -done
#Fon - done
#Telefax
#Festnetz - done
#tel : - done
#Tel. -done
#+49 - country code
def getall(url):
    Email = []
    Contact = []
    HumanNames = []
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/74.0.3729.169 Safari/537.36'}
    # if url['website']==None:
    #     return (None, None, None)
    if url == '':
        pass
    else:
        possible_url = ['', 'impressum', 'contact', 'contact+us','kontakt', 'impressum.html', 'Impressum.html', 'kontakt.html']
        #remove 'about', 'about+us', , 'über-mich', 'aboutus'
        for element in possible_url:
            full_url = url + element
            response = requests.get(full_url)
            if response.status_code == 200:
                print('Web site exists: ' + str(full_url))
                session = requests.Session()
                html = session.get(full_url, headers=headers)
                soup = BeautifulSoup(html.content, 'html.parser')
                if check_readability(soup):
                    print('Cannot read page.')
                    pass
                else:
                    Email = [*Email, *(find_email(soup.text))]
                    Contact = [*Contact, *(getcontactnumbers(soup.text))]
                    HumanNames = [*HumanNames, *(getnames(soup.text))]
            else:
                print('Web site does not exist: ' + str(full_url))
    Email_string = ",".join(str(x) for x in list(set(Email)))
    Contact_string = ",".join(str(x) for x in list(set(Contact)))
    HumanNames_string = ",".join(str(x) for x in list(set(HumanNames)))
    print(HumanNames_string)
    data = pd.DataFrame([url, Email_string, Contact_string, HumanNames_string])
    return (data)
def check_readability(soup):
    needs_selenium = 'Just a moment...Enable JavaScript and cookies to continue'
    if soup.text == needs_selenium:
        return True
    else:
        return False

def getnames(text):
    person_list = []
    person_names = person_list
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

    names = get_human_names(text)
    for person in person_list:
        person_split = person.split(" ")
        for name in person_split:
            if wordnet.synsets(name):
                if(name in person):
                    person_names.remove(person)
                    break
    #print('Names')
    #print(person_names)
    name_gender = []
    for first_name in person_names:
        #first name
        first = first_name.split(' ')[0]
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/74.0.3729.169 Safari/537.36'}
        genderchecker = r'http://www.namegenderpro.com/search-result/?gender_name='
        gender_url = genderchecker + first
        response = requests.get(gender_url)
        if response.status_code == 200:
            session = requests.Session()
            html = session.get(gender_url, headers=headers)
            soup = BeautifulSoup(html.content, 'html.parser')
            gender = soup.find('div', class_='searchresult_top_heading')
            gender = (gender.find('b')).text
            if gender in ['Male', 'Female', 'Unisex']:
                name_gender.append(first_name + '-' + gender)
    print(name_gender)
    return (name_gender)
def getnames2(text):
    pattern1 = "([A-ZÄÖÜß][a-zäßöü]+\s)(von|Von|da|Da|de|De|d'|du|Della|del|Del|della|di|y|Y'|[A-Z].)(\s[A-ZÄÖÜß][a-zäßöü,]+|[A-ZÄÖÜß][a-zäßöü,]+)" #Von/von--Good
    pattern2 = '([A-ZÄÖÜß][a-zäöüéàèéùâêßîôûçëïü]+[- ][A-ZÄÖÜß][a-zäßöüééàèùâêîôûçëïü]+)' #-- 2words
    pattern3 = '([A-ZÄÖÜß][a-zäöüééàèùâßêîôûçëïü]+[- ][A-ZÄÖÜß][a-zäöüééàèùâêßîôûçëïü]+[ -][A-ZÄÖÜß][a-zäöüéàèùâêßîôûçëïü]+)' #--3words
    pattern4 = '([A-ZÄÖÜß][a-zäöüéàèùâßêîôûçëïü]+ [- ][A-ZÄÖÜß][a-zäöüéàèéùâßêîôûçëïü]+[ -][A-ZÄÖÜß][a-zäöüééàèùâêîôûçßëïü]+[ -][A-ZÄÖÜß][a-zäöüéàèùâßêîéôûçëïü]+)' #4words
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
    name_gender = []
    for first_name in name:
        #first name
        first = first_name.split(' ')[0]
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/74.0.3729.169 Safari/537.36'}
        genderchecker = r'http://www.namegenderpro.com/search-result/?gender_name='
        gender_url = genderchecker + first
        response = requests.get(gender_url)
        if response.status_code == 200:
            session = requests.Session()
            html = session.get(gender_url, headers=headers)
            soup = BeautifulSoup(html.content, 'html.parser')
            gender = soup.find('div', class_='searchresult_top_heading')
            gender = (gender.find('b')).text
            if gender in ['Male', 'Female', 'Unisex']:
                name_gender.append(first_name + '-' + gender)
    #print(name_gender)
    return (name_gender)