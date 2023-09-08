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

#Constant filepath of input xlsx file
filetorun = 'Try' # Filename of excel input inside For_Run folder
write_excel_path = misc.write_excel_path(filetorun)
print(write_excel_path)

# Create new excel file every run
wb = openpyxl.Workbook()
ws = wb.active
wb.save(write_excel_path)
wb.close()

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

for_save1 = pd.DataFrame()
for_save2 = pd.DataFrame()

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
    row1 = pd.DataFrame(data=[MName, MAddress, MTel, MType]).transpose()
    for_save1 = pd.concat([for_save1, row1], ignore_index=True)
    #for_save1.columns = ["Name", "Address", "Telephone", "Type"]
    print(for_save1)

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
    row2 = pd.DataFrame(data=[Website, Directions]).transpose()
    for_save2 = pd.concat([for_save2, row2], ignore_index=True)
    #for_save2.columns = ['Website', 'Directions']
    print(for_save2)
excel_out = pd.ExcelWriter(write_excel_path)
for_excel = pd.concat([for_save1, for_save2], axis=1, ignore_index=True)
columns = ["Name", "Address", "Telephone", "Type", 'Website', 'Directions']
for_excel.columns = columns
for_excel.to_excel(excel_out)
excel_out.close()


wd.close()
wd.quit()
#rgnuSb xYjf2e
#class="deyx8d"