# Necessary imports
import pandas as pd
from string import punctuation
from pathlib import Path
import tkinter as tk
from tkinter import filedialog as fd

def getCompanyDomain(email):
    """Takes in an email. It will split the text on the '@' and return the domain. 
    
    Example:
        Input = test@live.com
        Return = live.com
    """
    return (email.split("@")[1])

def get_punct(email_prefix):
    punctReturn = ""
    
    for punct in punctuation:
        if punct in email_prefix:
            punctReturn = punct
            break
    
    return punctReturn

def findPattern(df, index, row):
    """
    Tries to match the pattern based on some preset patterns

    Returns:
        If pattern matches, an integer of the type of format, bool for hasPunctuation 
            1 - first + last
            2 - first + lastInit
            3-  firstInit + last
            4 - last + firstInit 
            5 - lastInit + first
            6 - last + first
            7 - first
            8 - last
            9 - firstInit + lastInit
    """    
    firstName = df.at[index, 'First Name'].lower()
    lastName = df.at[index, 'Last Name'].lower()
    firstInit = firstName[0].lower()
    lastInit = lastName[0].lower()
    email = df.at[index, 'Email'].lower()
    domain = getCompanyDomain(email).lower()
    punct = get_punct(email.split("@")[0])

    if(email == (firstName + punct + lastName + "@" + domain)):
        df.at[index, 'pattern'] = 1
    elif(email == (firstName + punct + lastInit + "@" + domain)):
        df.at[index, 'pattern'] = 2
    elif(email == (firstInit + punct + lastName + "@" + domain)):
        df.at[index, 'pattern'] = 3
    elif(email == (lastName + punct + firstInit + "@" + domain)):
        df.at[index, 'pattern'] = 4
    elif(email == (lastInit + punct + firstName + "@" + domain)):
        df.at[index, 'pattern'] = 5
    elif(email == (lastName + punct + firstName + "@" + domain)):
        df.at[index, 'pattern'] = 6
    elif(email == (firstName + punct + "@" + domain)):
        df.at[index, 'pattern'] = 7
    elif(email == (lastName + punct + "@" + domain)):
        df.at[index, 'pattern'] = 8
    elif(email == (firstInit + punct + lastInit + "@" + domain)):
        df.at[index, 'pattern'] = 9 
    else:
        df.at[index, 'pattern'] = 100
    
    # If this is the first run, can't comapre previous email pattern-- assume all is well
    if(index == 0):
        df.at[index, 'hasDiffPatterns'] = 0
        df.at[index, 'emailExistsForCompany'] = 0
        return [True, df, punct]
        
    # Otherwise, check to see if this is for the same company or a new one
    else:
        # If new company -- just set the hasDiffPatterns and emailExistsForCompany
        if(df.at[index, 'Company Name'] != df.at[(index-1), 'Company Name'] ):
            df.at[index, 'hasDiffPatterns'] = 0
            df.at[index, 'emailExistsForCompany'] = 0
            return [True, df, punct]
        
        # Else need to see if the pattern matches previous one
        else:
            # If patterns match -- Update columns, return true
            if(df.at[index, 'pattern'] == df.at[(index-1), 'pattern']):
                df.at[index, 'hasDiffPatterns'] = 0
                df.at[index, 'emailExistsForCompany'] = 0
                return [True, df, punct]
            
            # Otherwise, update columns, return false
            else:
                df.at[index, 'hasDiffPatterns'] = 1
                df.at[index, 'emailExistsForCompany'] = 1
                return [False, df, punct]

def createEmail(df, index, pattern, punct):
    """
    Takes in a dataframe, the index, and pattern. It will generate an email based on the pattern. The patterns can be found in findPattern
    """
    firstName = df.at[index, 'First Name'].lower()
    lastName = df.at[index, 'Last Name'].lower()
    firstInit = firstName[0].lower()
    lastInit = lastName[0].lower()
    email = df.at[index, 'Email']
    
    # If index = 0 and email = null -- can't get domain
    if(index == 0 and pd.isna(email)):
        domain = ""
    else:
        # If email is null -- get the domain from previous row
        if(pd.isna(email)):
            domain = getCompanyDomain(df.at[(index-1), 'newEmail'])
        # Otherwise, get domain from this email
        else:
            domain = getCompanyDomain(df.at[index, 'Email'])
    
    # Find pattern type and generate email
    if(pattern == 1):
        df.at[index, 'newEmail'] = (firstName + punct + lastName + "@" + domain)
    elif(pattern == 2):
        df.at[index, 'newEmail'] = (firstName + punct + lastInit + "@" + domain)
    elif(pattern == 3):
        df.at[index, 'newEmail'] = (firstInit + punct + lastName + "@" + domain)
    elif(pattern == 4):
        df.at[index, 'newEmail'] = (lastName + punct + firstInit + "@" + domain)
    elif(pattern == 5):
        df.at[index, 'newEmail'] = (lastInit + punct + firstName + "@" + domain)
    elif(pattern == 6):
        df.at[index, 'newEmail'] = (lastName + punct + firstName + "@" + domain)
    elif(pattern == 7):
        df.at[index, 'newEmail'] = (firstName + punct + "@" + domain)
    elif(pattern == 8):
        df.at[index, 'newEmail'] = (lastName + punct + "@" + domain)
    elif(pattern == 9):
        df.at[index, 'newEmail'] = (firstInit + punct + lastInit + "@" + domain)    
    else:
        # Can't find pattern, don't create email
        return df
    
    df.at[index, 'emailExistsForCompany'] = 0
    return df

def convertDTypes(df):
    """
    Takes in a DataFrame and returns the DF with String types
    """
    # Let's start by coverting these objects to strings to allow for easier string manipulation
    df['Company Name'] = df['Company Name'].astype("string")
    df['URL'] = df['URL'].astype("string")
    df['Contact'] = df['Contact'].astype("string")
    df['First Name'] = df['First Name'].astype("string")
    df['Last Name'] = df['Last Name'].astype("string")
    df['Email'] = df['Email'].astype("string")
    
    return df

def printStatment(df):
    # Taking a look at the first few rows of data
    print(df.head(10))
    print()
    
    # Taking a look at object types
    print(df.dtypes)
    print()

def createNewColumns(df):
    # This will be for the new email we generate from our pattern
    df['newEmail'] = None
    
    # This will be for the type of pattern it is 
    df['pattern'] = None
    
    # If 0 -- all patterns match in this company
    #   Else -- one or more patterns don't match 
    df['hasDiffPatterns'] = None   
    
    # Check to see if we can even find a pattern for the company
    #   0 = Yes
    #   1 = No
    df['emailExistsForCompany'] = None 
    
    return df

def setColumnsToSkip(df, index):
    df.at[index, 'pattern'] = 0
    df.at[index, 'hasDiffPatterns'] = 0
    df.at[index, 'emailExistsForCompany'] = 1
    
    return df

def main():
        
    # Open prompt for the file to select
    filename = fd.askopenfilename(
        title='Open a file',
        initialdir='/',
        filetypes=(
            ('CSV', '*.csv'),
            ('All files', '*.*')
        )
    )
    
    # If no file is selected, print message and close. 
    if(filename == ''):
        print("You must select a valid .csv file. Stopping execution.")
        exit()
    
    # Importing the dataset
    df = pd.read_csv(filename)
    
    # Let's convert the dtypes to Strings and add some additional columns
    df = convertDTypes(df)
    df = createNewColumns(df)
    
    # Now let's sort df by Company Name & Email -- placing non empty emails at the top of each company 
    df = df.sort_values(by=['Company Name', 'Email'], na_position='last')
    df.reset_index(drop=True, inplace=True)
    
    # If you would like to see the head & dtypes, uncomment next line
    #printStatment(df)
    
    # Looping through the df to find patterns and update email
    for index, row in df.iterrows():
        
        # If this is the first run, we won't be able to compare to the previous row
        if(index == 0):
            # Check if email is null
            if(pd.isna(df.at[index, 'Email'])):
                # If email is null -- we need to go to the next company
                df = setColumnsToSkip(df, index)
                #print(df.iloc[index])
            # If not -- does the pattern match the others in this company
            else:
                foundPattern, df, punct = findPattern(df, index, row)                
                # If returns True -- we found the pattern, it matches the previous pattern -- call createEmail
                if(foundPattern == True):
                    pattern = df.at[index, 'pattern'] 
                    df = createEmail(df, index, pattern, punct)
        
        # Otherwise, check if new company
        else:
            # If it's a new company
            if(df.at[index, 'Company Name'] != df.at[(index-1), 'Company Name']):
                # If so check if email is null
                if(pd.isna(df.at[index, 'Email'])):
                    # If email is null -- we need to go to the next company
                    df = setColumnsToSkip(df, index)
                    #print(df.iloc[index])
                # If not -- does the pattern match the others in this company
                else:
                    foundPattern, df, punct = findPattern(df, index, row)
                    # If returns True -- we found the pattern, it matches the previous pattern -- call createEmail
                    if(foundPattern == True):
                        pattern = df.at[index, 'pattern'] 
                        df = createEmail(df, index, pattern, punct)
                    # Otherwise it must have a different pattern
                    else:
                        df.at[index, 'hasDiffPatterns'] = 1
            
            # We're on the same company
            else:
                # Check if emailExistsForCompany and hasDiffPatterns
                if(df.at[(index-1), 'hasDiffPatterns'] == 1 or df.at[(index-1), 'emailExistsForCompany'] == 1):
                    df = setColumnsToSkip(df, index)
                    #print(df.iloc[index])
                # Otherwise -- does email exist?
                else:
                    # Is email null?
                    if(pd.isna(df.at[index, 'Email'])):
                        # If email is null -- use the previously found pattern to create an email
                        df.at[index, 'pattern'] = df.at[(index-1), 'pattern']
                        punct = get_punct(df.at[index-1, 'newEmail'].split("@")[0])
                        df = createEmail(df, index, df.at[index, 'pattern'], punct) 
                    # Else it has an email
                    else:
                        # Find the pattern of this email
                        foundPattern, df, punct = findPattern(df, index, row)
                        # If returns True -- we found the pattern, it matches the previous pattern -- call createEmail
                        if(foundPattern == True):
                            pattern = df.at[index, 'pattern'] 
                            df = createEmail(df, index, pattern, punct)
                        # Otherwise it must have a different pattern
                        else:
                            df.at[index, 'hasDiffPatterns'] = 1
        #print(df.iloc[index])

    # Removing columns we no longer need
    df.drop(columns=['pattern', 'hasDiffPatterns', 'emailExistsForCompany'], axis=1, inplace=True)
    
    print(df.head(50))
    
    # Saving df to a new .csv
    #df.to_csv('updated_contacts.csv', header=True, index=False)
    
if __name__ =='__main__':
    main()