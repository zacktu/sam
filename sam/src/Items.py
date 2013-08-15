'''
Created on Jan 3, 2010

@author: bob

Manage the table of items.  The columns of the table are defined here,
and functions that add and delete table entries are here.  Some other
service functions are also located here.  Function names are long and
intended to describe their work.

'''

import warnings
import MySQLdb
import SAMDB
warnings.simplefilter("error", MySQLdb.Warning)

class Items(object):
    '''
    classdocs
    '''
    
    def CreateItemsTable(self, samdb):
        rows = "( \
            item_number       char(4)     NOT NULL PRIMARY KEY, \
            item_description  char(50)    NOT NULL, \
            item_donatedby    char(3)     NOT NULL REFERENCES  \
                                            Donors(donor_number), \
            item_retail       decimal(6)  NULL, \
            item_minimumbid   decimal(6)  NOT NULL, \
            item_bidincrement decimal(6)  NOT NULL, \
            item_purchasedby  char(3)     NULL REFERENCES \
                                            Buyers(buyer_number), \
            item_salesprice   decimal(6)  NULL \
            )"
        samdb.CreateTable("Items", rows, "item_number")
        '''  I couldn't determine whether these two lines of code worked.
        samdb.AddForeignKey("Items", "item_donatedby", "Donors", "donor_num")
        samdb.AddForeignKey("Items", "item_purchasedby", "Buyers", "buyer_num")
        '''

    def AddItem(self, samdb, item_number, item_description, item_donatedby, 
                 item_retail, item_minimumbid, item_bidincrement):
        fields = "item_number, item_description, item_donatedby, \
                  item_retail, item_minimumbid, item_bidincrement, \
                  item_purchasedby, item_salesprice"
        values = "'" + item_number + "'" + ',' \
               + "'" + item_description + "'" + "," \
               + "'" + item_donatedby + "'" + ',' \
               + "'" + item_retail + "'" + ',' \
               + "'" + item_minimumbid + "'" + ',' \
               + "'" + item_bidincrement + "'" + ',' \
               + ' NULL, NULL'
        samdb.InsertRow("Items", fields, values)
        
    def FetchItem(self, samdb, itemNumber):
        query = "SELECT item_description, item_donatedby, item_retail, \
                item_minimumbid, item_bidincrement \
                FROM Items WHERE item_number = " + itemNumber + ";"
        return samdb.FetchRow(query)
        
    def DeleteItem(self, samdb, itemNumber):
        samdb.DeleteRow("Items", "item_number", itemNumber)
        
    # Confirm whether a donor number is in the database.
    def IsValidItemNumber(self, samdb, itemNumber):
        query = "SELECT item_description FROM Items \
                WHERE item_number = '" + itemNumber + "' ; "
        rows = samdb.FetchRows(query)
        if len(rows) > 0:
            return True
        else:
            return False
     
    # Use the MySQL update function to modify a row in the table.   
    def UpdateItem(self, samdb, itemNumber, description, donorNumber,
                   retailPrice, minimumBid, increment):
        query = "UPDATE Items  \
                    SET item_number = '" + itemNumber + "' , \
                        item_description = '"  + description + "' , \
                        item_donatedby = '" + donorNumber + "' , \
                        item_retail = '" + retailPrice + "' , \
                        item_minimumbid = '" + minimumBid + "' , \
                        item_bidincrement = '" + increment + "' \
                    WHERE item_number = '" + itemNumber + "' ; "
        samdb.ExecuteQuery(query)

    ''' Determine whether an item has been purchased.  Fetch the 
    item_purchasedby column for a row.  This vaoue will be either
    a buyer number (has been purchased) or None (hasn't been
    purchased '''
    def CheckItemHasBuyer(self, itemNumber, samdb):
        query = 'SELECT item_purchasedby FROM Items WHERE item_number = ' \
                + itemNumber + ';' 
        row = samdb.FetchRow(query)
        return row[0]   # returns either a buyer number or None
        

if __name__ == '__main__':
    samdb = SAMDB.SAMDB()
    samdb.CreateDatabase()
    dt = Items()
    dt.CreateItemsTable(samdb)
