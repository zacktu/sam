'''
Created on July 9, 2013

@author: bob
'''

import sys
import MySQLdb
import SAMDB
import Console
import Printer


''' Print all donors in the database to the console.  This program
    assumes that a SAM database already exists.  Everything here
    has been adapted from the TestConnectAndPopulate program. '''

def ConsoleShowDonors():
    if not (len(sys.argv) == 2 or len(sys.argv) == 6):
        print 'Usage: python ConsoleShowDonors.py dbname ' + \
              '[hostname portnumber username password]'
        exit()
    samdb = Connect(sys.argv)
    samdb.UseDatabase(sys.argv[1])
    console = Console.Console()
    console.DisplayDonors(samdb)
    
''' Connect to the mysql server.  If remote, then the database name, server
    name, user name, and password are needed.  If the server is on localhost,
    only the name of the database is needed.' '''
def Connect(argv):
    try:
        if len(sys.argv) == 6:
            samdb = SAMDB.SAMDB(dbname = argv[1],
                                hostname = argv[2],
                                portnumber = int(argv[3]),
                                username = argv[4],
                                password = argv[5])
        else: 
            samdb = SAMDB.SAMDB(dbname = argv[1])
    except MySQLdb.Error, e:
        print "ConsoleShowDonors.Connect: Error %d: %s" % \
                (e.args[0], e.args[1])
        exit (1)
    except MySQLdb.Warning, e:
        print("ConsoleShowDonors.Connect: Warning: ", e)
    return samdb

if __name__ == '__main__':
    ConsoleShowDonors()
