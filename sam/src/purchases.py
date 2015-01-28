'''
Created on Jan 3, 2010

@author: bob
'''

import buyers
import dialogs

class Purchases(object):
    def __init__(self):
        self.buyers = buyers.Buyers()
        
    def purchaseItem(self, samdb, itemNumber, buyerNumber, salesPrice):
        query = "UPDATE Items SET item_purchasedby = '" + buyerNumber + \
                "', item_salesprice = '" + salesPrice + \
                "' WHERE item_number = '" + itemNumber + "';"
        samdb.executeQuery(query)

        if self.buyers.hasBuyerPaid(samdb, buyerNumber):
            self.buyers.cancelBuyerReceipt(samdb, buyerNumber)
            dialogs.displayErrorDialog(
                'Buyer ' + buyerNumber
                + ' has already paid for other items.\n '
                + 'Please print a new shopping cart,\n'
                + 'collect the proper amount,\n '
                + 'and print a new receipt.')
              
    def fetchPurchase(self, samdb, itemNumber):
        query = 'SELECT item_purchasedby, item_salesprice FROM Items \
                WHERE item_number = ' + itemNumber + ';'
        ## temporary
        row = samdb.fetchRow(query)
        return row
        ### return samdb.fetchRow(query)S
        
    def hasBeenPurchased(self, samdb, itemNumber):
        row = self.fetchPurchase(samdb, itemNumber)
        if not row[0] == None:
            return True
        else:
            return False
    
    def deletePurchase(self, samdb, itemNumber):
        # Who bought this item?
        query = 'SELECT item_purchasedby FROM Items \
                 WHERE item_number = ' + itemNumber + ' ; '
        row = samdb.fetchRow(query)
        buyerNumber = row[0]

        # Delete the buyer for this item
        query = 'UPDATE Items SET item_purchasedby = NULL,' \
                'item_salesprice = NULL \
                WHERE item_number = ' + itemNumber + ';'
        samdb.executeQuery(query)

        if self.buyers.hasBuyerPaid(samdb, buyerNumber):
            self.buyers.cancelBuyerReceipt(samdb, buyerNumber)
            dialogs.displayErrorDialog(
                'Buyer ' + buyerNumber
                + ' has already paid for item number '
                + itemNumber + '.\n '
                + 'Please print a new shopping cart,\n'
                + 'refund the proper amount,\n '
                + 'and print a new receipt.')

