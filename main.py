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

#Parse in Beautiful Soup
from bs4 import BeautifulSoup

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
#iNTie
#jRKCUd
#oYWfcb OSrXXb RB2q5e
button = wait.until(EC.presence_of_element_located((By.CLASS_NAME, 'iNTie')))
htmlbutton = button.get_attribute('outerHTML')
morebutton = BeautifulSoup(htmlbutton, "html.parser")
morebusinesslink = morebutton.findAll('a')

for link in morebusinesslink:
    link_url = link['href']
    print(link_url)

#set window handler to reference
wd.execute_script("window.open('');")
wd.switch_to.window(wd.window_handles[1])
wd.get(link_url)

#wait.until(EC.presence_of_element_located((By.XPATH, '//*[@id="rso"]/div[2]/div/div/div[1]/div[5]/div/div[1]/a/div'))).click() # More business
#wait.until(EC.presence_of_element_located((By.XPATH, '//*[@id="Odp5De"]/div/div/div[1]/div[2]/div[1]/div[2]/g-more-link/a/div/span[1]/span'))).click()

#Get details
#table = wait.until(EC.presence_of_element_located((By.XPATH, '//*[@id="yDmH0d"]/c-wiz/div/div[3]/div/div/div[1]/div[3]/div[3]/c-wiz/div/div/div[1]/c-wiz/div')))
table = wait.until(EC.presence_of_element_located((By.CLASS_NAME, 'ykYNg')))

html = table.get_attribute('outerHTML')
table = BeautifulSoup(html, "html.parser")

# Get all Establishments
establishmentlist = table.findAll('div', class_='deyx8d')

#List every establishment details
for each_name in establishmentlist:
    #print('Name= ' + each_name.find('div', class_='rgnuSb xYjf2e').text) # Name
    #print('Address= ' + each_name.find('span', class_='hGz87c').text) # Address
    each_detail = each_name.findAll('div', class_='I9iumb')
    #print([detail for detail in each_detail])
    print("Name")
    print(each_detail[0].text)
    print("Type")
    #print(each_detail[1])
    print(each_detail[1].find('span', class_= "hGz87c").text)
    print("Address")
    print(each_detail[2])
    print(len(each_detail[2]))
    sched_address_num = [x for x in each_detail[2]]
    print(sched_address_num)
    for cel in sched_address_num:

        if misc.istellnumber(cel.text):
            print('Tel:' + cel.text)
        elif misc.isOpen(cel.text):
            print('Schedule:' + cel.text)
        else:
            print('Address: ' + cel.text)

#[<div class="I9iumb"><div class="rgnuSb xYjf2e">Kawayan Home Massage Service</div></div>, <div class="I9iumb"><div class="Ty81De hGz87c GEx0hc"><div class="OJbIQb"><div aria-hidden="true" class="rGaJuf">4.6</div><div aria-label="Rated 4.6 out of 5" class="dHX2k" role="img"><svg class="ePMStd NMm5M" focusable="false" height="12" viewbox="0 0 12 12" width="12"><path d="M6 .6L2.6 11.1 11.4 4.7H.6L9.4 11.1Z" fill="#fabb05" stroke="#fabb05" stroke-linejoin="round" stroke-width="1"></path></svg><svg class="ePMStd NMm5M" focusable="false" height="12" viewbox="0 0 12 12" width="12"><path d="M6 .6L2.6 11.1 11.4 4.7H.6L9.4 11.1Z" fill="#fabb05" stroke="#fabb05" stroke-linejoin="round" stroke-width="1"></path></svg><svg class="ePMStd NMm5M" focusable="false" height="12" viewbox="0 0 12 12" width="12"><path d="M6 .6L2.6 11.1 11.4 4.7H.6L9.4 11.1Z" fill="#fabb05" stroke="#fabb05" stroke-linejoin="round" stroke-width="1"></path></svg><svg class="ePMStd NMm5M" focusable="false" height="12" viewbox="0 0 12 12" width="12"><path d="M6 .6L2.6 11.1 11.4 4.7H.6L9.4 11.1Z" fill="#fabb05" stroke="#fabb05" stroke-linejoin="round" stroke-width="1"></path></svg><svg class="ePMStd NMm5M hhikbc" focusable="false" height="12" viewbox="0 0 12 12" width="12"><path d="M6 .6L2.6 11.1 11.4 4.7H.6L9.4 11.1Z" fill="#dadce0" stroke="#dadce0" stroke-linejoin="round" stroke-width="1"></path><path d="M 5.9785156 0.099609375 C 5.7694302 0.10826956 5.5878505 0.24620779 5.5234375 0.4453125 L 4.3085938 4.1992188 L 0.59960938 4.1992188 C 0.11615617 4.2005387 -0.084192375 4.8189487 0.30664062 5.1035156 L 3.3085938 7.2871094 L 2.125 10.945312 C 1.976014 11.405803 2.5028618 11.788235 2.8945312 11.503906 L 6 9.2441406 L 6 0.1015625 C 5.9926244 0.10156576 5.9859412 0.099278595 5.9785156 0.099609375 z " fill="#fabb05"></path></svg></div></div><div aria-label="48 reviews" class="leIgTe">(48)</div></div><span class="hGz87c">Massage therapist</span><div class="FjZRNe hGz87c">10+ years in business</div></div>, <div class="I9iumb"><span class="hGz87c"><span class="A5yTVb"><span style="color:rgba(217,48,37,1)">Closed</span> â‹… Opens 3â€¯PM</span></span><span class="hGz87c"><span>Quezon City, Metro Manila</span></span><span class="hGz87c">0917 143 5959</span></div>]
#['Blue Tranquility Home Service Massage Spa', '3.6(19)Spa10+ years in business', 'Closed â‹… Opens 12\u202fPMQuezon City, Metro Manila0917 822 6303']
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