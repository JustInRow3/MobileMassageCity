import requests
from selenium.webdriver.common.keys import Keys
from selenium.common.exceptions import NoSuchElementException as NSE
import openpyxl
import time
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.chrome.options import Options
import configparser
import os
import misc
import pandas as pd

#Parse in Beautiful Soup
from bs4 import BeautifulSoup
from selenium.webdriver.common.keys import Keys
from selenium.common.exceptions import NoSuchElementException as NSE
import openpyxl
import time
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.chrome.options import Options
import configparser
import os
import misc
import pandas as pd
#Open browser window

thisfolder = os.path.dirname(os.path.abspath(__file__))
initfile = os.path.join(thisfolder, 'config.txt')
# print this folder
print('config.txt location: ' + initfile)

config = configparser.ConfigParser()
# Open config file for variables
config.read(initfile)
keyword = config.get('MMC-VARIABLES', 'Keyword')
print('Keyword= ' + keyword)
autoinstalldriver = config.get('MMC-VARIABLES', 'AutoInstallDriver') # If auto-install chrome driver
print('AutoInstallDriver= ' + autoinstalldriver)
chromedriver = config.get('MMC-VARIABLES', 'ChromeDriver') # Path to chromedriver
print('ChromeDriver= ' + chromedriver)
headless = config.get('MMC-VARIABLES', 'Headless?')
print('Headless= ' + headless)

#Chromedriver Options
options = Options()
options.page_load_strategy = 'eager' # Webdriver waits until DOMContentLoaded event fire is returned.
options.add_experimental_option('excludeSwitches', ['enable-logging'])
options.headless = False

if autoinstalldriver:
    service = Service(ChromeDriverManager().install())
else:
    service = Service(executable_path=chromedriver)

if headless == 'True':
    options.headless = True

Url = r'https://madlens-sinnesreise.jimdosite.com/impressum/'
page = requests.get(Url)
soup = BeautifulSoup(page.content, "html.parser")

# check if it contains email
#misc.find_email(soup.text)
#print(soup.text)
print(soup)

#+49 (0) 30 403 67 70 77
#Festnetz: 030/403677077
#about
#impressum
#contact+us
chromedriver = r'C:\Users\jjie\.wdm\drivers\chromedriver\win64\116.0.5845.180\chromedriver-win32\chromedriver.exe'
service = Service(executable_path=chromedriver)
options = Options()
options.page_load_strategy = 'eager' # Webdriver waits until DOMContentLoaded event fire is returned.
#service = Service(ChromeDriverManager().install())
# wd = webdriver.Chrome(service=service, options=options)
# wd.implicitly_wait(10)
#wd.get(Url)
# print(BeautifulSoup(wd.page_source, "html.parser"))

#print(page.get_attribute('outerHTML'))
print(misc.getcontactnumbers(soup, webdriver=webdriver, url=Url, service=service, options=options))