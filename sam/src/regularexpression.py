'''
Functions to check regular expressions.  These are used
for data entry to be certain that id numbers are numeric,
phone numbers are in the XXX-XXX-XXXX format, etc.

Author: bob
Date: 2 June 2010

'''

import re

# Donor number must be three decimal digits.
def CheckDonorNumber(s):
    return re.match(r"\d{3}", s)

# Item number must be three decimal digits.
def CheckItemNumber(s):
    return re.match(r"\d{3}", s)

# Buyer number must be three decimal digits.
def CheckBuyerNumber(s):
    return re.match(r"\d{3}", s)

# State must be 2 alpohabetic characters.
def CheckState(s):
    return re.match(r"[A-Z]{2}", s)

# Zip code must be 5 decimal digits.
def CheckZipCode(s):
    return re.match(r"\d{5}", s)

# Telephone number must be in format XXX-XXX-XXXX.
def CheckTelno(s):
    return re.match(r"\d{3}\-\d{3}\-\d{4}", s)

def CheckMoney(s):
    # This approach seems ridiculous, but I couldn't find another way
    returnValue = re.match(r"\d", s) and not re.search(r"\D", s)
    if returnValue is None:
        returnValue = False
    return returnValue