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
    
    def CreateAuctionTable(self, samdb):
        rows = "( \
            auction_header_type   char(10) NOT NULL PRIMARY KEY, \
            auction_header_text	  char(60) NULL \
            )"
        samdb.CreateTable("Auction", rows, "auction_header_type")

    def AddAuction(self, samdb, header_type, header_text):
        fields = "auction_header_type, auction_header_text"
        values = "'" + header_type + "'" + ',' \
               + "'" + header_type + "'" 
        samdb.InsertRow("Auction", fields, values)
        
    def FetchAuctionHeaderText(self, samdb, header_type):
        query = "SELECT auction_header_text \
                 FROM Auction WHERE auction_header_type = " + \
                 header_type + ";"
        return samdb.FetchRow(query)
                
    def UpdateAuction(self, samdb, type, text):
        query = "UPDATE Auction  \
                    SET auction_header_text = '" + text + "' \
                    WHERE auction_header_type = '" + type + "' ; "
        samdb.ExecuteQuery(query)
        
    def AddAuctionTitle(self, samdb, text):
        fields = "auction_header_type, auction_header_text"
        values = "'title'" + ',' + "'" + text + "'"
        samdb.InsertRow("Auction", fields, values)
        print 'ADDED TITLE'
        
    def AddAuctionSubtitle(self, samdb, text):
        fields = "auction_header_type, auction_header_text"
        values = "'subtitle'" + ',' + "'" + text + "'"
        samdb.InsertRow("Auction", fields, values)
        print 'ADDED SUBTITLE'
        
    def AddAuctionDate(self, samdb, text):
        fields = "auction_header_type, auction_header_text"
        values = "'date'" + ',' + "'" + text + "'"
        samdb.InsertRow("Auction", fields, values)
        print 'ADDED DATE'
        
    def GetAuctionTitle(self, samdb):
        query = "SELECT auction_header_text \
                FROM Auction WHERE auction_header_type = 'title' ;"
        row = samdb.FetchRow(query)
        return row[0]
    
    def GetAuctionSubtitle(self, samdb):
        query = "SELECT auction_header_text \
                FROM Auction WHERE auction_header_type = 'subtitle' ;"
        row = samdb.FetchRow(query)
        return row[0]
    
    def GetAuctionDate(self, samdb):
        query = "SELECT auction_header_text \
                FROM Auction WHERE auction_header_type = 'date' ;"
        row = samdb.FetchRow(query)
        return row[0]
    
# Run the program
if __name__ == '__main__':
    if len(sys.argv) < 2:
        print 'Usage: python Auction.py dbname'
    else:
        try:
            samdb = dbservices.Samdb(dbname='mysql')
            dbname = sys.argv[1]
            print('Now create ' + dbname + ';')
            samdb.CreateDatabase(dbname)
            print(dbname + ' created.')
            Auction = Auction()
            Auction.CreateAuctionTable(samdb)
        except MySQLdb.Error, e:
            print "Error %d: %s" % (e.args[0], e.args[1])
            sys.exit (1)
        except MySQLdb.Warning, e:
            print("Warning: ", e)
