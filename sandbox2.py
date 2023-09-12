import pandas as pd
from bs4 import BeautifulSoup
import requests
import urllib
import misc
import os
import configparser
import openpyxl

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

headers = {'User-Agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/74.0.3729.169 Safari/537.36'}

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

#Initialize dataframes
for_excel1 = pd.DataFrame()
for_excel2 = pd.DataFrame()

#Loop in Keywords.xlsx
file = 'Keywords.xlsx'
for keyword_add in misc.read_xlsx(file):
    keyword_url = urllib.parse.quote_plus((str(keyword) + ' ' + str(keyword_add)))
    url = r'https://www.google.com/search?q=' + keyword_url
    html = requests.get(url, headers=headers)
    soup = BeautifulSoup(html.text, 'html.parser')
    print(keyword_add)
    if misc.business(soup) == True:
        button = soup.find('div', class_='iNTie')
        morebusiness = button.findAll('a')
        for link in morebusiness:
            link_url = link['href']
            print(link_url)
        businesslist = requests.get(link_url, headers=headers)
        business_soup = BeautifulSoup(businesslist.content, 'html.parser')
        establishmentlist = business_soup.findAll('div', class_='deyx8d')

        for_save1 = pd.DataFrame()
        for_save2 = pd.DataFrame()

        # List every establishment main details
        for each_name in establishmentlist:
            # Set to default
            Keyword = fullkeyword
            MName = 'none'
            MType = 'none'
            MTel = 'none'
            each_detail = each_name.findAll('div', class_='I9iumb')

            # print([detail for detail in each_detail])
            print("Name: " + each_detail[0].text)
            MName = each_detail[0].text
            print("Type: " + each_detail[1].find('span', class_="hGz87c").text)
            MType = each_detail[1].find('span', class_="hGz87c").text
            sched_address_num = [x for x in each_detail[2]]

            # print(sched_address_num)
            for cel in sched_address_num:
                if misc.istellnumber(cel.text):
                    print('Tel:' + cel.text)
                    MTel = cel.text
                elif misc.isOpen(cel.text):
                    # print('Schedule:' + cel.text)
                    pass
                else:
                    print('Address: ' + cel.text)
                    MAddress = cel.text
            row1 = pd.DataFrame(data=[Keyword, Results, MName, MAddress, MTel, MType]).transpose()
            for_save1 = pd.concat([for_save1, row1], ignore_index=True)
            # for_save1.columns = ["Name", "Address", "Telephone", "Type"]
            # print(for_save1)

        establishmentlist_details = table.findAll('div', class_='DyM7H')
        # List every establishment main details
        for each_detail_add in establishmentlist_details:
            each_detail_sub = each_detail_add.findAll('div', class_='zuotBc')
            # Set to default
            Website = 'none'
            Directions = 'none'
            for det in each_detail_sub:
                # print(det.findAll('a'))
                # Website
                if det.text == "Website":
                    print('Website: ' + det.find('a')['href'])
                    Website = det.find('a')['href']
                elif det.text == "Directions":
                    print('Directions: ' + det.find('a')['href'])
                    Directions = det.find('a')['href']
            row2 = pd.DataFrame(data=[Website, Directions]).transpose()
            for_save2 = pd.concat([for_save2, row2], ignore_index=True)
        for_excel1 = pd.concat([for_save1, for_save2], axis=1, ignore_index=True)  # output every valid keyword
        for_excel2 = pd.concat([for_excel2, for_excel1], ignore_index=True)  # past and present
    else:
        print('Keyword Invalid!')
        datainvalid = pd.DataFrame([fullkeyword, 'none', 'none', 'none', 'none', 'none', 'none',
                                    'none']).transpose()  # output of invalid keywork
        print(datainvalid)
        for_excel2 = pd.concat([for_excel2, datainvalid], ignore_index=True)
excel_out = pd.ExcelWriter(write_excel_path)
columns = ['Keyword', 'Results for', "Name", "Address", "Telephone", "Type", 'Website', 'Directions']
for_excel2.columns = columns
for_excel2.to_excel(excel_out)
excel_out.close()