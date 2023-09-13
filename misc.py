import time
import os
from pathlib import Path
import pandas as pd
import re
import requests
from bs4 import BeautifulSoup

string_ = '1234134145'
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
    print(emails)
    return emails

def getcontactnumbers(html, webdriver, url, service, options):
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
    needs_selenium = 'Just a moment...Enable JavaScript and cookies to continue'
    collected = []
    if html.text != needs_selenium:
        string = html.text
        #matches = re.findall(pattern, html.text, flags=re.IGNORECASE)
    else:
        wd = webdriver.Chrome(service=service, options=options)
        wd.implicitly_wait(10)
        wd.get(url)
        newsoup = BeautifulSoup(wd.page_source, "html.parser")
        string = newsoup.text
        wd.close()
        wd.quit()
    for pattern in pattern_list:
        matches = re.findall(pattern, string, flags=re.IGNORECASE)
        valid_search = [valid for valid in matches if valid != []]
        if len(valid_search) > 0:
              collected.append(valid_search)
        #collected.append(matches)
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
def getallemail(url):
    possible_url = ['about', 'about+us', 'impressum', 'contact', 'contact+us',
                    'kontakt', 'impressum.html', 'kontakt.html', 'über-mich', '', 'aboutus']
    for element in possible_url:
        full_url = url + '/' + element
        response = requests.get(full_url)
        if response.status_code == 200:
            print('Web site exists')
            page = requests.get(full_url).page_source
            return find_email(page)

        else:
            print('Web site does not exist')
            return False
