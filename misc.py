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


