'''
Functions to check regular expressions.  These are used
for data entry to be certain that id numbers are numeric,
phone numbers are in the XXX-XXX-XXXX format, etc.

Author: bob
Date: 2 June 2010

'''

import re

# Donor number must be three decimal digits.
def checkDonorNumber(s):
    return re.match(r"\d{3}", s)

# Item number must be three decimal digits.
def checkItemNumber(s):
    return re.match(r"\d{3}", s)

# Buyer number must be three decimal digits.
def checkBuyerNumber(s):
    return re.match(r"\d{3}", s)

# State must be 2 alphabetic characters.
def checkState(s):
    return re.match(r"[A-Z]{2}", s)

# Zip code must be 5 decimal digits.
def checkZipCode(s):
    return re.match(r"\d{5}", s)

# Telephone number must be in format XXX-XXX-XXXX.
def checkTelno(s):
    return re.match(r"\d{3}\-\d{3}\-\d{4}", s)

def checkMoney(s):
    # This approach seems ridiculous, but I couldn't find another way
    returnValue = re.match(r"\d", s) and not re.search(r"\D", s)
    if returnValue is None:
        returnValue = False
    return returnValue

# The first two of these are from StackOverflow.  I did the third one.
# https://stackoverflow.com/questions/4202538/
#         python-escape-regex-special-characters
def escapeSingleQuotes(s):
    return re.sub(r"([\'])", r'\\\1', s)

def escapeDoubleQuotes(s):
    return re.sub(r'([\"])', r'\\\1', s)

def escapeQuotes(s):
    return re.sub(r"([\'])", r'\\\1', re.sub(r'([\"])', r'\\\1', s))

if __name__ == '__main__':
    print escapeSingleQuotes("Annie's biscuits.  They're delicious I'm sure.")
    print escapeDoubleQuotes('The name of the book is "Gone with the Wind".')
    print escapeQuotes("Annie's biscuits.  They're delicious I'm sure.")
    print escapeQuotes('The name of the book is "Gone with the Wind".')
    print escapeQuotes("Today's date is \"very\" special.")
