'''
Created on Jan 3, 2010

@author: bob
'''

class Purchases(object):
        
    def PurchaseItem(self, samdb, itemNumber, buyerNumber, salesPrice):
        query = "UPDATE Items SET item_purchasedby = '" + buyerNumber + \
                "', item_salesprice = '" + salesPrice + \
                "' WHERE item_number = '" + itemNumber + "';"
        samdb.ExecuteQuery(query)
              
    def FetchPurchase(self, samdb, itemNumber):
        query = 'SELECT item_purchasedby, item_salesprice FROM Items \
                WHERE item_number = ' + itemNumber + ';'
        ## temporary
        row = samdb.FetchRow(query)
        return row
        ### return samdb.FetchRow(query)S
        
    def HasBeenPurchased(self, samdb, itemNumber):
        row = self.FetchPurchase(samdb, itemNumber)
        if not row[0] == None:
            return True
        else:
            return False
    
    def DeletePurchase(self, samdb, itemNumber):
        query = 'UPDATE Items SET item_purchasedby = NULL, \
                item_salesprice = NULL \
                WHERE item_number = ' + itemNumber + ';'
        samdb.ExecuteQuery(query)

