'''
Created on August 3, 2011

@author: bob
'''

import sys
import warnings
import MySQLdb
import dbservices
warnings.simplefilter("error", MySQLdb.Warning)

class Auction(object):
    '''
    classdocs
    '''
    
    def createAuctionTable(self, samdb):
        rows = "( \
            auction_header_type   char(10) NOT NULL PRIMARY KEY, \
            auction_header_text	  char(60) NULL \
            )"
        samdb.createTable("Auction", rows, "auction_header_type")

    def addAuction(self, samdb, header_type, header_text):
        fields = "auction_header_type, auction_header_text"
        values = "'" + header_type + "'" + ',' \
               + "'" + header_type + "'" 
        samdb.insertRow("Auction", fields, values)
        
    def fetchAuctionHeaderText(self, samdb, header_type):
        query = "SELECT auction_header_text \
                 FROM Auction WHERE auction_header_type = " + \
                 header_type + ";"
        return samdb.fetchRow(query)
                
    def updateAuction(self, samdb, type, text):
        query = "UPDATE Auction  \
                    SET auction_header_text = '" + text + "' \
                    WHERE auction_header_type = '" + type + "' ; "
        samdb.executeQuery(query)
        
    def addAuctionTitle(self, samdb, text):
        fields = "auction_header_type, auction_header_text"
        values = "'title'" + ',' + "'" + text + "'"
        samdb.insertRow("Auction", fields, values)
        print 'ADDED TITLE'
        
    def addAuctionSubtitle(self, samdb, text):
        fields = "auction_header_type, auction_header_text"
        values = "'subtitle'" + ',' + "'" + text + "'"
        samdb.insertRow("Auction", fields, values)
        print 'ADDED SUBTITLE'
        
    def addAuctionDate(self, samdb, text):
        fields = "auction_header_type, auction_header_text"
        values = "'date'" + ',' + "'" + text + "'"
        samdb.insertRow("Auction", fields, values)
        print 'ADDED DATE'
        
    def getAuctionTitle(self, samdb):
        query = "SELECT auction_header_text \
                FROM Auction WHERE auction_header_type = 'title' ;"
        row = samdb.fetchRow(query)
        return row[0]
    
    def getAuctionSubtitle(self, samdb):
        query = "SELECT auction_header_text \
                FROM Auction WHERE auction_header_type = 'subtitle' ;"
        row = samdb.fetchRow(query)
        return row[0]
    
    def getAuctionDate(self, samdb):
        query = "SELECT auction_header_text \
                FROM Auction WHERE auction_header_type = 'date' ;"
        row = samdb.fetchRow(query)
        return row[0]
    
# Run the program
if __name__ == '__main__':
    if len(sys.argv) < 2:
        print 'Usage: python auction.py dbname'
    else:
        try:
            samdb = dbservices.Samdb(dbname='mysql')
            dbname = sys.argv[1]
            print('Now create ' + dbname + ';')
            samdb.createDatabase(dbname)
            print(dbname + ' created.')
            auction = Auction()
            auction.createAuctionTable(samdb)
        except MySQLdb.Error, e:
            print "Error %d: %s" % (e.args[0], e.args[1])
            sys.exit (1)
        except MySQLdb.Warning, e:
            print("Warning: ", e)
