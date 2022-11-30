import pandas as pd

import re



def main():
    stringTest = 'Spangler, Gla'
    
    #listVar = stringTest.split(" ")
    #print(len(listVar))

    x = re.search('[a-zA-Z]\\, ', stringTest)
    if x:
        print(x)
    else:
        print("nope")
        
    print(stringTest)

if __name__ =='__main__':
    main()