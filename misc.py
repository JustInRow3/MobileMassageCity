import time
import os
from pathlib import Path
import pandas as pd
import re
import requests
from bs4 import BeautifulSoup
import concurrent.futures
from retrying import retry


def istellnumber(string):
    int_list = ['0', '1', '2', '3', '4', '5', '6', '7', '8', '9', ',', '.', ' ', '+', '(', ')']
    return all([(x in int_list) for x in string])


# print(istellnumber(string_))
def isOpen(string):
    test1 = (string.lower()).find('open')
    test2 = (string.lower()).find('close')
    if test1 == -1 or test2 == -1:
        return False
    else:
        return True


# print(isOpen(string_))
def writelogs():
    filename_date = time.strftime("%Y%m%d%H%M%S", time.localtime())
    script_dir = Path(os.path.dirname(__file__))  # <-- absolute dir the script is in
    rel_path = Path(r"/Logs/" + 'Logs_' + filename_date + '.out')
    new_file = script_dir.joinpath(*rel_path.parts[1:])
    # abs_file_path = os.path.join(script_dir, rel_path)
    return new_file


def write_excel_path(file):
    filename_date = time.strftime("_%Y%m%d%H%M%S", time.localtime())
    script_dir = Path(os.path.dirname(__file__))  # <-- absolute dir the script is in
    rel_path = Path(r"/Done_Run/" + file + filename_date + '.xlsx')
    new_file = script_dir.joinpath(*rel_path.parts[1:])
    # abs_file_path = os.path.join(script_dir, rel_path)
    return new_file


# print(write_excel_path('file'))

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


# CAYQGA
# YzSd

def file_(file):
    script_dir = Path(os.path.dirname(__file__))  # <-- absolute dir the script is in
    rel_path = Path("/For_Run/" + file)
    # abs_file_path = os.path.join(script_dir, rel_path)
    new_file = script_dir.joinpath(*rel_path.parts[1:])
    return new_file


def read_xlsx(file):
    data = pd.read_excel(file_(file))
    # print(data['Keyword'])
    return data['Keyword']


# - Kontakt
# - Über uns
# - Über mich
# - Impressum

def find_email(html):
    email_pattern = r"[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,4}"
    emails = re.findall(email_pattern, html)
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
    pattern9 = r'\+49[().:\0-9-\s]+'
    pattern_list = [pattern9, pattern8, pattern7, pattern6, pattern5, pattern4, pattern3, pattern2, pattern1]
    collected = []
    for pattern in pattern_list:
        matches = re.findall(pattern, text, flags=re.IGNORECASE)
        valid_search = [valid for valid in matches if valid != []]
        for match in valid_search:
            if len(match) > 9:
                new_string = ''.join(re.findall(r'\w+', match))
                collected.append(new_string)
            else:
                pass
    print('Numbers')
    print(collected)
    return collected

def getalltext(url, timeout):
    headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/74.0.3729.169 Safari/537.36'}
    response = requests.get(url)
    if response.status_code == 200:
        session = requests.Session()
        html = session.get(url, headers=headers, timeout=timeout)
        soup = BeautifulSoup(html.content, 'html.parser')
        if check_readability(soup):
            print(url + '- Cannot read page.')
            pass
        else:
            print('Found:' + url)
            Email = find_email(soup.text)
            Contact = getcontactnumbers(soup.text)
            Name = getnames3(soup.text)
            return (Email, Contact, Name)

def check_readability(soup):
    needs_selenium = 'Just a moment...Enable JavaScript and cookies to continue'
    if soup.text == needs_selenium:
        return True
    else:
        return False


def getgender(url, timeout):
    # Define a retry decorator with exponential backoff
    @retry(wait_exponential_multiplier=1000, wait_exponential_max=10000, stop_max_attempt_number=5)
    def make_request(url):
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/74.0.3729.169 Safari/537.36'}
        session = requests.Session()
        html = session.get(url[1], headers=headers, timeout=timeout)
        html.raise_for_status()  # Check for HTTP errors
        return html
    try:
        html = make_request(url)
        soup = BeautifulSoup(html.content, 'html.parser')
        gender = soup.find('div', class_='searchresult_top_heading')
        gender = (gender.find('b')).text
        if gender in ['Male', 'Female', 'Unisex']:
            return str(url[0]) + ' - ' + str(gender)
    except requests.exceptions.RequestException as e:
        print(f"Request failed after retries: {e}")
def get_links(url):
    possible_url = ['impressum.html', 'Impressum.html', 'impressum', 'about', 'about+us', 'aboutus', 'kontakt.html', 'kontakt']
    links = [(url + '/' + pos) for pos in possible_url]
    return links

def getnames3(text):
    pattern1 = "([A-ZÄÖÜß][a-zäßöü]+\s)(von|Von|da|Da|de|De|d'|du|Della|del|Del|della|di|y|Y'|[A-Z].)(\s[A-ZÄÖÜß][a-zäßöü,]+|[A-ZÄÖÜß][a-zäßöü,]+)"  # Von/von--Good
    pattern2 = '([A-ZÄÖÜß][a-zäöüéàèéùâêßîôûçëïü]+[- ][A-ZÄÖÜß][a-zäßöüééàèùâêîôûçëïü]+)'  # -- 2words
    pattern3 = '([A-ZÄÖÜß][a-zäöüééàèùâßêîôûçëïü]+[- ][A-ZÄÖÜß][a-zäöüééàèùâêßîôûçëïü]+[ -][A-ZÄÖÜß][a-zäöüéàèùâêßîôûçëïü]+)'  # --3words
    pattern4 = '([A-ZÄÖÜß][a-zäöüéàèùâßêîôûçëïü]+ [- ][A-ZÄÖÜß][a-zäöüéàèéùâßêîôûçëïü]+[ -][A-ZÄÖÜß][a-zäöüééàèùâêîôûçßëïü]+[ -][A-ZÄÖÜß][a-zäöüéàèùâßêîéôûçëïü]+)'  # 4words
    pat_regex = re.compile("|".join("({})".format(x) for x in [pattern4, pattern3, pattern2, pattern1]))
    matches = pat_regex.findall(text)
    for_filter = list(set(matches))
    name_url = []
    genders = []
    for_filter2 = [list(set(x)) for x in for_filter if x]
    genderchecker = r'http://www.namegenderpro.com/search-result/?gender_name='
    for elem in for_filter2:
        for sub in elem:
            if len(sub.split(' ')) > 1 and sub.split(' ')[0] != '' and sub.split(' ')[1] != '':
                print(sub)
                name_url.append((sub, (str(genderchecker)+str(sub.split(' ')[0]))))
    print(name_url)
    with concurrent.futures.ThreadPoolExecutor() as executor:
        futures = []
        for url in name_url:
            futures.append(
                executor.submit(
                    getgender, url=url, timeout=30
                )
            )
        for future in concurrent.futures.as_completed(futures):
            try:
                if future.result() is not None:
                    genders.append(future.result())
                    print(future.result())
            except requests.ConnectTimeout:
                print("ConnectTimeout.")
    return genders

def getall2(url):
    if url == None:
        pass
    else:
        results = []
        all_url = get_links(url)
        with concurrent.futures.ThreadPoolExecutor() as executor:
            futures = []
            for url in all_url:
                # Submit tasks to the executor
                futures.append(executor.submit(getalltext, url, 50))
            concurrent.futures.wait(futures)
            for future in futures:
                result = future.result()
                if result != None:
                    results.append(result)
    output_list = [sum(sublist, []) for sublist in zip(*results)]
    clean_list = ['; '.join(list(set(x))) for x in output_list]
    clean_list.insert(0, url)
    print(clean_list)
    return clean_list
def mainpage(all_url):
    results = []
    with concurrent.futures.ThreadPoolExecutor() as executor:
        futures = []
        for url in all_url:
            # Submit tasks to the executor
            futures.append(executor.submit(getall2, url))
        concurrent.futures.wait(futures)
        for future in futures:
            result = future.result()
            if result != None:
                results.append(result)
    print(results)


