# -*- coding: utf-8 -*-
import pandas as pd
import misc
import openpyxl

filetorun = 'Output' # Filename of excel input inside For_Run folder
write_excel_path = misc.write_excel_path(filetorun)
print(write_excel_path)

# Create new excel file every run
# wb = openpyxl.Workbook()
# ws = wb.active
# wb.save(write_excel_path)
# wb.close()

import misc
for_excel = pd.DataFrame()
headers = {'User-Agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/74.0.3729.169 Safari/537.36'}

url_list = [r'https://www.rebalance-massage-berlin.de/']
for url in url_list:
    output = misc.getall(url).transpose()
    for_excel = pd.concat([for_excel, output], ignore_index=True)
    for_excel.columns = ['website', 'email', 'contact', 'possible_human_name']
excel_out = pd.ExcelWriter(write_excel_path)
for_excel.to_excel(excel_out)
excel_out.close()


