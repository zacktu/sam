'''
Created on Jan 3, 2010

@author: bob
'''

import warnings
import MySQLdb
import dbservices
warnings.simplefilter("error", MySQLdb.Warning)

class Buyers(object):
    '''
    classdocs
    '''
    
    def createBuyersTable(self, samdb):
        rows = "( \
            buyer_number      char(3)  NOT NULL PRIMARY KEY, \
            buyer_last        char(20) NOT NULL, \
            buyer_first       char(20) NOT NULL, \
            buyer_street      char(40) NULL, \
            buyer_city        char(40) NULL, \
            buyer_telno       char(12) NOT NULL \
            )"
        samdb.createTable("Buyers", rows, "buyer_number")

    def addBuyer(self, samdb, buyer_number, buyer_last, buyer_first,\
            buyer_street, buyer_city, buyer_telno):
        fields = "buyer_number, buyer_last, buyer_first, buyer_street, \
                  buyer_city, buyer_telno"
        values = "'" + buyer_number + "'" + ',' \
               + "'" + buyer_last + "'" + ',' \
               + "'" + buyer_first + "'" + "," \
               + "'" + buyer_street + "'" + ',' \
               + "'" + buyer_city + "'" + ',' \
               + "'" + buyer_telno + "'"
        samdb.insertRow("Buyers", fields, values)
        
    def fetchBuyer(self, samdb, buyerNumber):
        query = "SELECT buyer_last, buyer_first, \
                    buyer_street, buyer_city, buyer_telno \
                FROM Buyers WHERE buyer_number = " + buyerNumber + ";"
        return samdb.fetchRow(query)
                
    def updateBuyer(self, samdb, buyerNumber, lastName, firstName, \
                    street, city, telno):
        query = "UPDATE Buyers  \
                    SET buyer_last = '" + lastName + "' , \
                        buyer_first = '" + firstName + "' , \
                        buyer_street = '"  + street + "' , \
                        buyer_city = '" + city + "' , \
                        buyer_telno = '" + telno + "' \
                    WHERE buyer_number = '" + buyerNumber + "' ; "
        samdb.executeQuery(query)

    def DeleteBuyer(self, samdb, buyerNumber):
        samdb.deleteRow("Buyers", "buyer_number", buyerNumber)
        
    # Confirm whether a donor number is in the database.
    def isValidBuyerNumber(self, samdb, buyerNumber):
        query = "SELECT buyer_last FROM Buyers \
                WHERE buyer_number = '" + buyerNumber + "' ; "
        rows = samdb.fetchRows(query)
        if len(rows) > 0:
            return True
        else:
            return False

    def getBuyersItems(self, samdb, buyerNumber):
        query = 'SELECT item_number FROM Items WHERE item_purchasedby = ' \
                + buyerNumber + ';'
        items = samdb.fetchRows(query)
        itemList = []
        for item in items:
            itemList.append(item[0])
        return itemList
    
    def getBuyersPurchases(self, samdb, buyerNumber):
        query = 'SELECT item_number, item_description, item_salesprice \
                 FROM Items \
                 WHERE item_purchasedby = ' + buyerNumber + ';'
        items = samdb.fetchRows(query)
        return items
    
    def getAllBuyers(self, samdb):
        query = 'SELECT buyer_number FROM Buyers ORDER BY buyer_number'
        allBuyers = samdb.fetchRows(query)
        return allBuyers

if __name__ == '__main__':
    samdb = dbservices.Samdb()
    samdb.createDatabase()
    buyers = Buyers()
    buyers.createBuyersTable(samdb)
