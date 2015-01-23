__author__ = 'bob'

'''
Create a /home/<user>/.sam/profile for one of the people using the program.
The principal user has created the database, owns it, and has a profile that
enables use of the database.  Everyone else will use the same profile and
the same login for the database.  They must have a profile before launching
the sam program.

USAGE: sudo copyprofile.py username

Written by Bob Cannon 22 Jan 2015
'''

import sys
import os
import profileservices
import subprocess

def copyProfile():
    if (len(sys.argv) <= 1):
        print 'Usage: python copyprofile.py username [usernames]'
        sys.exit()
    for count in range (1, len(sys.argv)):

        userName = sys.argv[count]

        ## Get path this source profile
        try:
            homeDirectory= os.getenv('HOME')
            sourceProfile = homeDirectory + '/.sam/profile'
            if not os.path.exists(sourceProfile):
                print 'Can''t get path to your sam profile.'
                sys.exit()
        except IOError as e:
            dialogs.displayErrorDialog(
                'copyProfile: Unable to get path to your home directory.')
            sys.exit()

        ## Get path to destination profile
        try:
            destinationPath = '/home/' + userName + '/.sam'
            if not os.path.exists(destinationPath):
                os.makedirs(destinationPath)
        except IOError as e:
            dialogs.displayErrorDialog(
                'copyProfile: Unable to create the destination directory.')
            sys.exit()
        destinationDirectory = '/home/' + userName + '/.sam'

        ## Copy the file and change owner and group
        try:
            command = \
                'cp -r ' + sourceProfile + ' ' + destinationDirectory + '/.'
            subprocess.Popen(command, shell=True)
            command = 'chown -R ' + userName + ' ' + destinationDirectory
            subprocess.Popen(command, shell=True)
            command = 'chgrp -R ' + userName + ' ' + destinationDirectory
            subprocess.Popen(command, shell=True)
        except OSError as e:
            dialogs.displayErrorDialog('Unable to execute the system commands.')
            sys.exit()

if __name__ == '__main__':
    copyProfile()
