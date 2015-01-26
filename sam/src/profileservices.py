'''

Profile -- a program to set manage the user's SAM profile

Functions
    create profile
    get profile
    
Created on 9 January 2015

Author Bob Cannon
'''

import os
import sys
import wx
import dialogs

def createProfile(dbName, hostName, portNumber, \
                  userName, password, title, subtitle, date):
    profile = {
               'dbName': dbName,
               'hostName': hostName,
               'portNumber': portNumber,
               'userName': userName,
               'password': password,
               'title': title,
               'subtitle': subtitle,
               'date': date}
    try:
        homeDirectory = os.getenv('HOME')
        path = homeDirectory + '/.sam'
        if not os.path.exists(path):
            os.makedirs(path)
        with open(os.path.join(path, 'profile'), 'w') as myFile:
            myFile.write(str(profile))
    except IOError as e:
        dialogs.displayErrorDialog(
            'Profile.createProfile: Unable to write the profile file.')
        sys.exit()

def getProfile():
    path = os.getenv('HOME') + '/.sam/profile'
    try:
        if not os.path.exists(path):
            dialogs.displayErrorDialog(
                'There is no user profile.\nSee the Auction manager.')
            sys.exit()
        else:
            fp = open(path, 'r').read()
            profile = eval(fp)
            return profile
    except IOError as e:
        dialogs.displayErrorDialog('Unable to read the profile.')
        sys.exit()

if __name__ == '__main__':
    app = wx.PySimpleApp()
    createProfile('test11', 'localhost', '3306', 'bob', 'bobspw', \
                    'TITLE FOR TESTING', 'SUBTITLE FOR TESTING', '1 Oct 2015')
    myProfile = getProfile()
    print 'PROFILE CONTENTS IN TEST HARNESS: '
    print '   ' + myProfile.get('dbName')
    print '   ' + myProfile.get('hostName')
    print '   ' + myProfile.get('portNumber')
    print '   ' + myProfile['userName']
    print '   ' + myProfile['password']
    print '   ' + myProfile['title']
    print '   ' + myProfile['subtitle']
    print '   ' + myProfile['date']


