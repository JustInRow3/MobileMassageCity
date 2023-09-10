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

#Constant filepath of input xlsx file
file = 'Keywords.xlsx'
filetorun = 'Output' # Filename of excel input inside For_Run folder
write_excel_path = misc.write_excel_path(filetorun)
print(write_excel_path)

# Create new excel file every run
wb = openpyxl.Workbook()
ws = wb.active
wb.save(write_excel_path)
wb.close()

import sys
f = open(misc.writelogs(), 'a', encoding="utf-8")
sys.stdout = f
print("-------------------------------------------------------------------------------" + "\n" +
      "-------------------------Mobile Massage Script Logs----------------------------" + "\n" +
      "-------------------------------------------------------------------------------")

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

for_excel1 = pd.DataFrame()
for_excel2 = pd.DataFrame()

for keyword_add in misc.read_xlsx(file):
    #Open browser window
    wd = webdriver.Chrome(service=service, options=options)
    wd.implicitly_wait(10)
    wd.get('https://www.google.com/')
    wait = WebDriverWait(wd, 50) # setup wait

    #Input keyword
    wd.switch_to.frame(wait.until(EC.presence_of_element_located((By.NAME, 'callout')))) # enter iframe first
    wait.until(EC.presence_of_element_located((By.XPATH, '//*[@id="yDmH0d"]/c-wiz/div/div/c-wiz/div/div/div/div[2]/div[2]/button'))).click() # Click signout
    wd.switch_to.default_content()
    wait.until(EC.presence_of_element_located((By.CLASS_NAME, 'gLFyf'))).send_keys(str(keyword) + ' ' + str(keyword_add))
    wait.until(EC.presence_of_element_located((By.CLASS_NAME, 'gLFyf'))).send_keys(Keys.RETURN)
    time.sleep(2)
    fullkeyword = str(keyword) + ' ' + str(keyword_add)
    print('FullKeyword: ' + fullkeyword)
    print(misc.isbusiness(wd=wd, wait=wait, EC=EC, By=By, NSE=NSE))
    if misc.isbusiness(wd=wd, wait=wait, EC=EC, By=By, NSE=NSE):
        #Click more business button
        button = wait.until(EC.presence_of_element_located((By.CLASS_NAME, 'iNTie')))
        htmlbutton = button.get_attribute('outerHTML')
        morebutton = BeautifulSoup(htmlbutton, "html.parser")
        morebusinesslink = morebutton.findAll('a')

        Results = wait.until(EC.presence_of_element_located((By.CLASS_NAME, 'eKPi4'))).text
        print(Results)
        for link in morebusinesslink:
            link_url = link['href']
            print(link_url)

        #set window handler to reference
        wd.execute_script("window.open('');")
        wd.switch_to.window(wd.window_handles[1])
        wd.get(link_url)

        #Get details
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
            Keyword = fullkeyword
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
            row1 = pd.DataFrame(data=[Keyword, Results, MName, MAddress, MTel, MType]).transpose()
            for_save1 = pd.concat([for_save1, row1], ignore_index=True)
            #for_save1.columns = ["Name", "Address", "Telephone", "Type"]
            #print(for_save1)

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
        for_excel1 = pd.concat([for_save1, for_save2], axis=1, ignore_index=True) # output every valid keyword
        for_excel2 = pd.concat([for_excel2, for_excel1], ignore_index=True) # past and present
    else:
        print('Keyword Invalid!')
        datainvalid = pd.DataFrame([fullkeyword, 'none', 'none', 'none', 'none', 'none', 'none', 'none']).transpose() # output of invalid keywork
        print(datainvalid)
        for_excel2 = pd.concat([for_excel2, datainvalid], ignore_index=True)
    #for_excel2 = pd.concat([for_excel2, for_excel1], ignore_index=True)
    wd.close()
    wd.quit()
excel_out = pd.ExcelWriter(write_excel_path)
columns = ['Keyword', 'Results for', "Name", "Address", "Telephone", "Type", 'Website', 'Directions']
for_excel2.columns = columns
for_excel2.to_excel(excel_out)
excel_out.close()
"""for website in for_excel2['Website']:
    if website != 'none':
        # Open browser window
        wd = webdriver.Chrome(service=service, options=options)
        wd.implicitly_wait(10)
        wd.get(website)
        wait = WebDriverWait(wd, 50)  # setup wait"""


f.close()
quit()


#rgnuSb xYjf2e
#class="deyx8d"