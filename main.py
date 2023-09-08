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

#List every establishment main details
for each_name in establishmentlist:
    # Set to default
    MName = 'none'
    MType = 'none'
    MTel = 'none'
    each_detail = each_name.findAll('div', class_='I9iumb')

    #print([detail for detail in each_detail])
    print("Name: " + each_detail[0].text)
    MName = each_detail[0].text
    print("Type: " + each_detail[1].find('span', class_="hGz87c").text)
    MType = each_detail[1].find('span', class_="hGz87c").text
    sched_address_num = [x for x in each_detail[2]]

    #print(sched_address_num)
    for cel in sched_address_num:
        if misc.istellnumber(cel.text):
            print('Tel:' + cel.text)
            MTel = cel.text
        elif misc.isOpen(cel.text):
            #print('Schedule:' + cel.text)
            pass
        else:
            print('Address: ' + cel.text)
            MAddress = cel.text
    row = pd.DataFrame(data=[MName, MAddress, MTel, MType]).transpose()
    print(row)

establishmentlist_details = table.findAll('div', class_='DyM7H')
#List every establishment main details
for each_detail_add in establishmentlist_details:
    each_detail_sub = each_detail_add.findAll('div', class_='zuotBc')
    # Set to default
    Website = 'none'
    Directions = 'none'
    for det in each_detail_sub:
        #print(det.findAll('a'))
        #Website
        if det.text == "Website":
            print('Website: ' + det.find('a')['href'])
            Website = det.find('a')['href']
        elif det.text == "Directions":
            print('Directions: ' + det.find('a')['href'])
            Directions = det.find('a')['href']
    row = pd.DataFrame(data=[Website, Directions]).transpose()
    print(row)
    #time.sleep(1)

""""[<a aria-label="Website" data-no-redirect="1" href="http://www.kawayanmassage.com/" ping="/url?sa=t&amp;source=web&amp;rct=j&amp;url=http://www.kawayanmassage.com/&amp;ved=2ahUKEwjc2MbNqJqBAxWbAzoCHRiHBOEQgU96BAgAECo&amp;opi=89978449"><div data-ved="2ahUKEwjc2MbNqJqBAxWbAzoCHRiHBOEQgU96BAgAECo" data-website-url="http://www.kawayanmassage.com/" jsaction="JIbuQc:THpQJf" jscontroller="CCRWHf"><div class="VfPpkd-dgl2Hf-ppHlrf-sM5MNb" data-is-touch-wrapper="true"><button aria-hidden="true" class="VfPpkd-LgbsSe VfPpkd-LgbsSe-OWXEXe-INsAgc VfPpkd-LgbsSe-OWXEXe-Bz112c-M1Soyc VfPpkd-LgbsSe-OWXEXe-dgl2Hf Rj2Mlf OLiIxf PDpWxe LQeN7 DDYJo s73B3c wF1tve Q8G3mf" data-idom-class="Rj2Mlf OLiIxf PDpWxe LQeN7 DDYJo s73B3c wF1tve Q8G3mf" jsaction="click:cOuCgd; mousedown:UX7yZ; mouseup:lbsD7e; mouseenter:tfO1Yc; mouseleave:JywGue; touchstart:p6p2H; touchmove:FwuNnf; touchend:yfqBxc; touchcancel:JMtRjd; focus:AHmuwe; blur:O22p3e; contextmenu:mg9Pef;mlnRJb:fLiPzd;" jscontroller="soHxf" tabindex="-1"><div class="VfPpkd-Jh9lGc"></div><div class="VfPpkd-J1Ukfc-LhBDec"></div><div class="VfPpkd-RLmnJb"></div><span aria-hidden="true" class="VfPpkd-kBDsod"><svg class="NMm5M" focusable="false" height="24" viewbox="0 0 24 24" width="24"><path d="M12 2C6.48 2 2 6.48 2 12s4.48 10 10 10 10-4.48 10-10S17.52 2 12 2zM4 12c0-.61.08-1.21.21-1.78L8.99 15v1c0 1.1.9 2 2 2v1.93C7.06 19.43 4 16.07 4 12zm13.89 5.4c-.26-.81-1-1.4-1.9-1.4h-1v-3c0-.55-.45-1-1-1h-6v-2h2c.55 0 1-.45 1-1V7h2c1.1 0 2-.9 2-2v-.41C17.92 5.77 20 8.65 20 12c0 2.08-.81 3.98-2.11 5.4z"></path></svg></span><span class="VfPpkd-vQzf8d" jsname="V67aGc">Website</span></button></div></div></a>]
Prettify
[<a aria-label="Directions" href="https://maps.google.com/maps?um=1&amp;fb=1&amp;gl=ph&amp;sa=X&amp;geocode=Kdm5f4-0t5czMecPH0wHOzLO&amp;daddr=Brgy,+Unit+A,+JFMK+Bldg,+111+Kamias+Rd,+Quezon+City,+1100+Metro+Manila&amp;ved=2ahUKEwjc2MbNqJqBAxWbAzoCHRiHBOEQ48ADegQIABAr" role="link" tabindex="0"><div class="VfPpkd-dgl2Hf-ppHlrf-sM5MNb" data-is-touch-wrapper="true"><button aria-hidden="true" class="VfPpkd-LgbsSe VfPpkd-LgbsSe-OWXEXe-INsAgc VfPpkd-LgbsSe-OWXEXe-Bz112c-M1Soyc VfPpkd-LgbsSe-OWXEXe-dgl2Hf Rj2Mlf OLiIxf PDpWxe LQeN7 DDYJo s73B3c wF1tve Q8G3mf" data-idom-class="Rj2Mlf OLiIxf PDpWxe LQeN7 DDYJo s73B3c wF1tve Q8G3mf" jsaction="click:cOuCgd; mousedown:UX7yZ; mouseup:lbsD7e; mouseenter:tfO1Yc; mouseleave:JywGue; touchstart:p6p2H; touchmove:FwuNnf; touchend:yfqBxc; touchcancel:JMtRjd; focus:AHmuwe; blur:O22p3e; contextmenu:mg9Pef;mlnRJb:fLiPzd;" jscontroller="soHxf" tabindex="-1"><div class="VfPpkd-Jh9lGc"></div><div class="VfPpkd-J1Ukfc-LhBDec"></div><div class="VfPpkd-RLmnJb"></div><span aria-hidden="true" class="VfPpkd-kBDsod"><svg class="NMm5M" enable-background="new 0 0 24 24" focusable="false" height="24" viewbox="0 0 24 24" width="24"><g><rect fill="none" height="24" width="24"></rect></g><g><path d="m21.41 10.59-7.99-8c-.78-.78-2.05-.78-2.83 0l-8.01 8c-.78.78-.78 2.05 0 2.83l8.01 8c.78.78 2.05.78 2.83 0l7.99-8c.79-.79.79-2.05 0-2.83zM13.5 14.5V12H10v3H8v-4c0-.55.45-1 1-1h4.5V7.5L17 11l-3.5 3.5z"></path></g></svg></span><span class="VfPpkd-vQzf8d" jsname="V67aGc">Directions</span></button></div></a>]
Prettify
[<a aria-label="Call" class="Od1FEc" data-phone-number="09171435959" data-ved="2ahUKEwjc2MbNqJqBAxWbAzoCHRiHBOEQ5cADegQIABAs" href="tel:09171435959" jsaction="rcuQ6b:npT2md;JIbuQc:F75qrd;F75qrd" jscontroller="hjq3ae" role="button"><div jsaction="JIbuQc:F75qrd"><div class="VfPpkd-dgl2Hf-ppHlrf-sM5MNb" data-is-touch-wrapper="true"><button aria-hidden="true" class="VfPpkd-LgbsSe VfPpkd-LgbsSe-OWXEXe-INsAgc VfPpkd-LgbsSe-OWXEXe-Bz112c-M1Soyc VfPpkd-LgbsSe-OWXEXe-dgl2Hf Rj2Mlf OLiIxf PDpWxe LQeN7 DDYJo s73B3c wF1tve Q8G3mf" data-idom-class="Rj2Mlf OLiIxf PDpWxe LQeN7 DDYJo s73B3c wF1tve Q8G3mf" jsaction="click:cOuCgd(preventDefault=true); mousedown:UX7yZ; mouseup:lbsD7e; mouseenter:tfO1Yc; mouseleave:JywGue; touchstart:p6p2H; touchmove:FwuNnf; touchend:yfqBxc; touchcancel:JMtRjd; focus:AHmuwe; blur:O22p3e; contextmenu:mg9Pef;mlnRJb:fLiPzd;" jscontroller="soHxf" tabindex="-1"><div class="VfPpkd-Jh9lGc"></div><div class="VfPpkd-J1Ukfc-LhBDec"></div><div class="VfPpkd-RLmnJb"></div><span aria-hidden="true" class="VfPpkd-kBDsod"><svg class="NMm5M" focusable="false" height="24" viewbox="0 0 24 24" width="24"><path d="M16.02 14.46l-2.62 2.62a16.141 16.141 0 0 1-6.5-6.5l2.62-2.62a.98.98 0 0 0 .27-.9L9.15 3.8c-.1-.46-.51-.8-.98-.8H4.02c-.56 0-1.03.47-1 1.03a17.92 17.92 0 0 0 2.43 8.01 18.08 18.08 0 0 0 6.5 6.5 17.92 17.92 0 0 0 8.01 2.43c.56.03 1.03-.44 1.03-1v-4.15c0-.48-.34-.89-.8-.98l-3.26-.65c-.33-.07-.67.04-.91.27z"></path></svg></span><span class="VfPpkd-vQzf8d" jsname="V67aGc">Call</span></button></div></div></a>]
Prettify
[<a aria-label="Share" data-hveid="CAAQLQ" data-ved="2ahUKEwjc2MbNqJqBAxWbAzoCHRiHBOEQpMMJegQIABAt" jsaction="RiZTIb;JIbuQc:RiZTIb" jsname="YOuPgf" role="button" tabindex="0"><div><div class="VfPpkd-dgl2Hf-ppHlrf-sM5MNb" data-is-touch-wrapper="true"><button aria-hidden="true" class="VfPpkd-LgbsSe VfPpkd-LgbsSe-OWXEXe-INsAgc VfPpkd-LgbsSe-OWXEXe-Bz112c-M1Soyc VfPpkd-LgbsSe-OWXEXe-dgl2Hf Rj2Mlf OLiIxf PDpWxe LQeN7 DDYJo s73B3c wF1tve Q8G3mf" data-idom-class="Rj2Mlf OLiIxf PDpWxe LQeN7 DDYJo s73B3c wF1tve Q8G3mf" jsaction="click:cOuCgd; mousedown:UX7yZ; mouseup:lbsD7e; mouseenter:tfO1Yc; mouseleave:JywGue; touchstart:p6p2H; touchmove:FwuNnf; touchend:yfqBxc; touchcancel:JMtRjd; focus:AHmuwe; blur:O22p3e; contextmenu:mg9Pef;mlnRJb:fLiPzd;" jscontroller="soHxf" tabindex="-1"><div class="VfPpkd-Jh9lGc"></div><div class="VfPpkd-J1Ukfc-LhBDec"></div><div class="VfPpkd-RLmnJb"></div><span aria-hidden="true" class="VfPpkd-kBDsod"><svg class="NMm5M hhikbc" focusable="false" height="24" viewbox="0 0 24 24" width="24"><path d="M18 16c-.79 0-1.5.31-2.03.81L8.91 12.7c.05-.23.09-.46.09-.7s-.04-.47-.09-.7l7.05-4.11c.53.5 1.25.81 2.04.81 1.66 0 3-1.34 3-3s-1.34-3-3-3-3 1.34-3 3c0 .24.04.48.09.7L8.04 9.81C7.5 9.31 6.79 9 6 9c-1.66 0-3 1.34-3 3s1.34 3 3 3c.79 0 1.5-.31 2.04-.81l7.05 4.12c-.05.22-.09.45-.09.69 0 1.66 1.34 3 3 3s3-1.34 3-3-1.34-3-3-3zm0-12c.55 0 1 .45 1 1s-.45 1-1 1-1-.45-1-1 .45-1 1-1zM6 13c-.55 0-1-.45-1-1s.45-1 1-1 1 .45 1 1-.45 1-1 1zm12 7c-.55 0-1-.45-1-1s.45-1 1-1 1 .45 1 1-.45 1-1 1z"></path></svg></span><span class="VfPpkd-vQzf8d" jsname="V67aGc">Share</span></button></div></div></a>]
"""
wd.close()
wd.quit()
#rgnuSb xYjf2e
#class="deyx8d"