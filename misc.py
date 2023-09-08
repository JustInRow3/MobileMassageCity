import time
import os
from pathlib import Path

string_ = '1234134145'
def istellnumber(string):
        int_list = ['0', '1', '2', '3', '4', '5', '6', '7', '8', '9', ',', '.', ' ', '+', '(', ')']
        return all([(x in int_list) for x in string])
#print(istellnumber(string_))
def isOpen(string):
        test1 = (string.lower()).find('open')
        test2 = (string.lower()).find('close')
        if test1 == -1 or test2 == -1:
                return False
        else:
                return True
#print(isOpen(string_))
def write_excel_path(file):
    filename_date = time.strftime("_%Y%m%d%H%M%S", time.localtime())
    script_dir = Path(os.path.dirname(__file__))  # <-- absolute dir the script is in
    rel_path = Path(r"/Done_Run/" + file + filename_date + '.xlsx')
    new_file = script_dir.joinpath(*rel_path.parts[1:])
    #abs_file_path = os.path.join(script_dir, rel_path)
    return new_file
#print(write_excel_path('file'))

def isbusiness(wd):

