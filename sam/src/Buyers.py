'''
Created on Jan 3, 2010

@author: bob
'''

import warnings
import MySQLdb
import SAMDB
warnings.simplefilter("error", MySQLdb.Warning)

class Buyers(object):
    '''
    classdocs
    '''
    
    def CreateBuyersTable(self, samdb):
        rows = "( \
            buyer_number      char(3)  NOT NULL PRIMARY KEY, \
            buyer_last        char(20) NOT NULL, \
            buyer_first       char(20) NOT NULL, \
            buyer_street      char(40) NULL, \
            buyer_city        char(15) NULL, \
            buyer_state       char(2)  NULL, \
            buyer_zip         char(10) NULL, \
            buyer_telno1      char(12) NOT NULL, \
            buyer_telno2      char(12) NULL \
            )"
        samdb.CreateTable("Buyers", rows, "buyer_number")

    def AddBuyer(self, samdb, buyer_number, buyer_last, buyer_first,\
            buyer_street, buyer_city, buyer_state, buyer_zip, buyer_telno1,\
            buyer_telno2):
        fields = "buyer_number, buyer_last, buyer_first, buyer_street, \
                  buyer_city, buyer_state, buyer_zip, buyer_telno1,\
                  buyer_telno2"
        values = "'" + buyer_number + "'" + ',' \
               + "'" + buyer_last + "'" + ',' \
               + "'" + buyer_first + "'" + "," \
               + "'" + buyer_street + "'" + ',' \
               + "'" + buyer_city + "'" + ',' \
               + "'" + buyer_state + "'" + ',' \
               + "'" + buyer_zip + "'" + ',' \
               + "'" + buyer_telno1 + "'" ',' \
               + "'" + buyer_telno2 + "'" 
        samdb.InsertRow("Buyers", fields, values)
        
    def FetchBuyer(self, samdb, buyerNumber):
        query = "SELECT buyer_last, buyer_first, \
                    buyer_street, buyer_city, buyer_state, buyer_zip, \
                    buyer_telno1, buyer_telno2 \
                FROM Buyers WHERE buyer_number = " + buyerNumber + ";"
        return samdb.FetchRow(query)
                
    def UpdateBuyer(self, samdb, buyerNumber, lastName, firstName, \
                    street, city, state, zip, telno1, telno2):
        query = "UPDATE Buyers  \
                    SET buyer_last = '" + lastName + "' , \
                        buyer_first = '" + firstName + "' , \
                        buyer_street = '"  + street + "' , \
                        buyer_city = '" + city + "' , \
                        buyer_state = '" + state + "' , \
                        buyer_zip = '" + zip + "' , \
                        buyer_telno1 = '" + telno1 + "' , \
                        buyer_telno2 = '" + telno2 + "' \
                    WHERE buyer_number = '" + buyerNumber + "' ; "
        samdb.ExecuteQuery(query)

    def DeleteBuyer(self, samdb, buyerNumber):
        samdb.DeleteRow("Buyers", "buyer_number", buyerNumber)
        
    # Confirm whether a donor number is in the database.
    def IsValidBuyerNumber(self, samdb, buyerNumber):
        query = "SELECT buyer_last FROM Buyers \
                WHERE buyer_number = '" + buyerNumber + "' ; "
        rows = samdb.FetchRows(query)
        if len(rows) > 0:
            return True
        else:
            return False

    def GetBuyersItems(self, samdb, buyerNumber):
        query = 'SELECT item_number FROM Items WHERE item_purchasedby = ' \
                + buyerNumber + ';'
        items = samdb.FetchRows(query)
        itemList = []
        for item in items:
            itemList.append(item[0])
        return itemList
    
    def GetBuyersPurchases(self, samdb, buyerNumber):
        query = 'SELECT item_number, item_description, item_salesprice \
                 FROM Items \
                 WHERE item_purchasedby = ' + buyerNumber + ';'
        items = samdb.FetchRows(query)
        return items
    
    def GetAllBuyers(self, samdb):
        query = 'SELECT buyer_number FROM Buyers ORDER BY buyer_number'
        allBuyers = samdb.FetchRows(query)
        return allBuyers

if __name__ == '__main__':
    samdb = SAMDB.SAMDB()
    samdb.CreateDatabase()
    buyers = Buyers()
    buyers.CreateBuyersTable(samdb)
