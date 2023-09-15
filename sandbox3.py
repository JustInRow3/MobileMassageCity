# -*- coding: utf-8 -*-

from bs4 import BeautifulSoup
import requests
import misc
import re

headers = {'User-Agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/74.0.3729.169 Safari/537.36'}

url = r'https://www.relaxcoach.net/impressum'
html = requests.get(url, headers=headers)
soup = BeautifulSoup(html.text, 'html.parser')

print(misc.getnames2(soup.text))