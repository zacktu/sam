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
import dbservices
warnings.simplefilter("error", MySQLdb.Warning)

class Items(object):
    '''
    classdocs
    '''
    
    def createItemsTable(self, samdb):
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
        samdb.createTable("Items", rows, "item_number")
        '''  I couldn't determine whether these two lines of code worked.
        samdb.addForeignKey("Items", "item_donatedby", "Donors", "donor_num")
        samdb.addForeignKey("Items", "item_purchasedby", "Buyers", "buyer_num")
        '''

    def addItem(self, samdb, item_number, item_description, item_donatedby,
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
        samdb.insertRow("Items", fields, values)
        
    def fetchItem(self, samdb, itemNumber):
        query = "SELECT item_description, item_donatedby, item_retail, \
                item_minimumbid, item_bidincrement, item_purchasedby, \
                item_salesprice \
                FROM Items WHERE item_number = '" + itemNumber + "';"
        return samdb.fetchRow(query)
        
    def deleteItem(self, samdb, itemNumber):
        samdb.deleteRow("Items", "item_number", itemNumber)
        
    # Confirm whether a donor number is in the database.
    def isValidItemNumber(self, samdb, itemNumber):
        query = "SELECT item_description FROM Items \
                WHERE item_number = '" + itemNumber + "' ; "
        rows = samdb.fetchRows(query)
        if len(rows) > 0:
            return True
        else:
            return False
     
    # Use the MySQL update function to modify a row in the table.   
    def updateItem(self, samdb, itemNumber, description, donorNumber,
                   retailPrice, minimumBid, increment):
        query = "UPDATE Items  \
                    SET item_number = '" + itemNumber + "' , \
                        item_description = '"  + description + "' , \
                        item_donatedby = '" + donorNumber + "' , \
                        item_retail = '" + retailPrice + "' , \
                        item_minimumbid = '" + minimumBid + "' , \
                        item_bidincrement = '" + increment + "' \
                    WHERE item_number = '" + itemNumber + "' ; "
        samdb.executeQuery(query)

    ''' Determine whether an item has been purchased.  Fetch the 
    item_purchasedby column for a row.  This vaoue will be either
    a buyer number (has been purchased) or None (hasn't been
    purchased '''
    def checkItemHasBuyer(self, itemNumber, samdb):
        query = 'SELECT item_purchasedby FROM Items WHERE item_number = ' \
                + itemNumber + ';' 
        row = samdb.fetchRow(query)
        return row[0]   # returns either a buyer number or None

    def getAllItems(self, samdb):
        query = 'SELECT item_number FROM Items ORDER BY item_number'
        allItems = samdb.fetchRows(query)
        return allItems

    def areAllCartsEmpty(self, samdb):
        query = "Select COUNT(*) FROM Items WHERE item_purchasedby IS NOT NULL"
        rows = samdb.fetchRows(query)
        count = rows[0][0]
        if count == 0:
            return True
        else:
            return False

if __name__ == '__main__':
    samdb = dbservices.Samdb()
    samdb.createDatabase()
    dt = Items()
    dt.createItemsTable(samdb)
