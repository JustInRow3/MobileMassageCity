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

#Open browser window
wd = webdriver.Chrome(service=service, options=options)
wd.implicitly_wait(10)
wd.get('https://www.google.com/')
wait = WebDriverWait(wd, 50) # setup wait

#Input keyword
wd.switch_to.frame(wait.until(EC.presence_of_element_located((By.NAME, 'callout')))) # enter iframe first
wait.until(EC.presence_of_element_located((By.XPATH, '//*[@id="yDmH0d"]/c-wiz/div/div/c-wiz/div/div/div/div[2]/div[2]/button'))).click() # Click signout
wd.switch_to.default_content()
wait.until(EC.presence_of_element_located((By.CLASS_NAME, 'gLFyf'))).send_keys(keyword)
wait.until(EC.presence_of_element_located((By.NAME, 'btnK'))).click()
time.sleep(2)

#Click more business button
#class="CHn7Qb pYouzb"
#wait.until(EC.presence_of_element_located((By.CLASS_NAME, 'CHn7Qb pYouzb'))).click() # More business
#wait.until(EC.presence_of_element_located((By.XPATH, '//*[@id="rso"]/div[2]/div/div/div[1]/div[5]/div/div[1]/a/div'))).click() # More business
wait.until(EC.presence_of_element_located((By.XPATH, '//*[@id="Odp5De"]/div/div/div[1]/div[2]/div[1]/div[2]/g-more-link/a/div/span[1]/span'))).click()

#Get details
#table = wait.until(EC.presence_of_element_located((By.XPATH, '//*[@id="yDmH0d"]/c-wiz/div/div[3]/div/div/div[1]/div[3]/div[3]/c-wiz/div/div/div[1]/c-wiz/div')))
table = wait.until(EC.presence_of_element_located((By.CLASS_NAME, 'ykYNg')))

#Parse in Beautiful Soup
from bs4 import BeautifulSoup
html = table.get_attribute('outerHTML')
table = BeautifulSoup(html, "html.parser")

# Get all Establishments
establishmentlist = table.findAll('div', class_='deyx8d')

#List every establishment details
for each_name in establishmentlist:
    #print('Name= ' + each_name.find('div', class_='rgnuSb xYjf2e').text) # Name
    #print('Address= ' + each_name.find('span', class_='hGz87c').text) # Address
    each_detail = each_name.findAll('div', class_='I9iumb')
    i = 0
    for fetch in each_detail:
        print([y.text for y in fetch])
        if i == 0:
            print('Name: ' + fetch.find('div', class_='rgnuSb xYjf2e').text)
        elif i == 1:
            print([x.text for x in fetch.findAll('div', class_='hGz87c')])
            """for detail1 in fetch.findAll('div', class_ = 'hGz87c'):
                if sub == 1:
                    print('Type: ' + fetch.find('span', class_='hGz87c').text)
                sub += 1"""
        elif i == 2:
            print([x.text for x in fetch.findAll('div', class_='hGz87c')])
        i += 1
"""            sub1 = 0
            for fetch.findAll('div', class_ = 'hGz87c'):
                if sub1 == 1:
                    print('Address: ' + fetch.find('span', class_='hGz87c').text)
                elif sub1 == 2:
                    print('Number: ' + fetch.find('span', class_='hGz87c').text)
                sub += 1"""


"""class NwqBmc
   I9iumb
       rgnuSb xYjf2e -class
   I9iumb
       non
       hGz87c type - span
   I9iumb
      hGz87c
      hGz87c - address span
      hGz87c - number span"""


#print(table.prettify())
time.sleep(1)
#rgnuSb xYjf2e
#class="deyx8d"