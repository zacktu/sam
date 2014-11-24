'''
Created on 13 May 2010

A program to set up a database fir the silent auction program.  This is intended to 
be executed as a command line program on the MySQL server.  The command
line syntax is
    
python CreateAuction dbname

The program creates a Samdb object.  When the object is created it connects
to mysql and to the mysql database, which always exists.

1.    Instantiate an Samdb object that is connected to mysql.
2.    Invoke dbservices.CreateDatabase to create dbname.
3.    Tell mysql to USE dbname.  After this all mysql commands apply to dbname.
      Create an Auction object and then the Auction table in dbname.
4.    Create a Donors object and then the Donors table in dbname.
5.    Create a Buyers object and then the Buyers table in dbname.
6.    Create an Items object and then the Buyers table in dbname.

There is no GUI, and there is no interchange with the user.  At the
moment, this program recreates only a database for the auction and also
creates Auction, Donor, Buyer, and Item tables.

@author: bob
'''

import MySQLdb
import sys
import dbservices
import auction
import donors
import buyers
import items

def CreateAuction(hname, pnumber, uname, pword, \
                  dbnam, title, subtitle, date):
    print 'ENTERED CREATE AUCTION'
    print hname, pnumber, uname, pword, dbnam, title, subtitle, date
    try:
        samdb = dbservices.Samdb(dbname='mysql',
                    hostname=hname,
                    portnumber=int(pnumber),
                    username=uname,
                    password=pword)
        DoEverything(samdb, dbnam, title, subtitle, date)
    except MySQLdb.Error, e:
        print "CreateAuction.CreateAuction: Error %d: %s" % \
                (e.args[0], e.args[1])
        sys.exit (1)
    except MySQLdb.Warning, e:
        print("CreateAuction.CreateAuction: Warning: ", e)

def DoEverything(samdb, dbnam, title, subtitle, date):
    print 'ENTERED DOEVERYTHING'
    try:
        ''' Now create the database. ''' 
        samdb.createDatabase(dbnam)
        print 'Database ' + dbnam + ' created.'
        dd = donors.Donors()
        dd.createDonorsTable(samdb)
        print "Donors table created."
        db = buyers.Buyers()
        db.createBuyersTable(samdb)
        print "Buyers table created."
        di = items.Items()
        di.createItemsTable(samdb)
        print "Items table created."
        
        ''' The Auction table is special because the data in it are
            entered by the auction manager, rather than by other users
            of the system.  Data for the table will come eventually
            from a GUI.  For the moment, default data are entered
            into the table.  '''
        da = auction.Auction()
        da.CreateAuctionTable(samdb)
        print "Auction table created."
        print 'ENTERING AUCTION DATA'
        da.AddAuctionTitle(samdb, title)
        da.AddAuctionSubtitle(samdb, subtitle)
        da.AddAuctionDate(samdb, date)
        print 'ADDED AUCTION DATA'
    except MySQLdb.Error, e:
        print "CreateAuction.DoEverything: Error %d: %s" % \
                (e.args[0], e.args[1])
        sys.exit (1)
    except MySQLdb.Warning, e:
        print("CreateAuction.DoEverything: Warning: ", e)
    
    return

if __name__ == '__main__':
    if not (len(sys.argv) == 2 or len(sys.argv) == 6):
        print 'Usage: python createauction.py dbname ' + \
              '[hostname portnumber username password]'
    else:
        try:
            ''' 'mysql' is the database that's always there 
                so connect to it when instantiating Samdb '''
            if len(sys.argv) == 6:
                samdb = dbservices.Samdb(dbname='mysql',
                                    hostname=sys.argv[2],
                                    portnumber=int(sys.argv[3]),
                                    username=sys.argv[4],
                                    password=sys.argv[5])
            else: 
                samdb = dbservices.Samdb(dbname='mysql')

            DoEverything(samdb, sys.argv[1], 
                         'WNC Returned Peace Corps Volunteers',
                         'Working to improve the world community',
                         'September 14, 2011')
        except MySQLdb.Error, e:
            print "CreateAuction.CreateAuction: Error %d: %s" % \
                    (e.args[0], e.args[1])
            sys.exit (1)
        except MySQLdb.Warning, e:
            print("CreateAuction.CreateAuction: Warning: ", e)