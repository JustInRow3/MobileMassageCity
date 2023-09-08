import misc
import openpyxl
import pandas as pd
""""#print(misc.write_excel_path('try'))

#Constant filepath of input xlsx file
filetorun = 'Try' # Filename of excel input inside For_Run folder
write_excel_path = misc.write_excel_path(filetorun)
print(write_excel_path)

# Create new excel file every run
wb = openpyxl.Workbook()
ws = wb.active
wb.save(write_excel_path)
wb.close()

data1 = pd.DataFrame(['as', 'sd', 'fg']).transpose()
data2 = pd.DataFrame(['qw', 'we', 'er', 'tr']).transpose()
merge = pd.concat([data1, data2], axis=1)
print(merge)""""