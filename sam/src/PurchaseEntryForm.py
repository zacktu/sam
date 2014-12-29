import wx
import MySQLdb
import dialogs
import regularexpression
import buyers
import items
import purchases
import console

class PurchaseEntryForm(wx.Panel):
    def __init__(self, parent, samdb, function):
        super(PurchaseEntryForm, self).__init__(parent)

        self.parent = parent
        self.samdb = samdb
        self.function = function
        self.items = items.Items()
        self.buyers = buyers.Buyers()
        self.purchases = purchases.Purchases()
        self.con = console.Console()
        
        # First create the controls

        itemNumberLabel = wx.StaticText(self, -1, "Item #:")
        self.itemNumberTC = wx.TextCtrl(self, -1, "", size=(40, -1), \
                                        style=wx.TE_RIGHT)
        
        buyerNumberLabel = wx.StaticText(self, -1, "Buyer #:")
        self.buyerNumberTC = wx.TextCtrl(self, -1, "", size=(40, -1), \
                                        style=wx.TE_RIGHT)
        
        winningBidLabel = wx.StaticText(self, -1, "Winning Bid:")
        self.winningBidTC = wx.TextCtrl(self, -1, "", size=(50, -1), \
                                         style=wx.TE_RIGHT)

        cancelButton = wx.Button(self, -1, "Cancel")
        self.Bind(wx.EVT_BUTTON, self.OnCancelButton, cancelButton)
        
        saveButton = wx.Button(self, -1, "Save")
        self.Bind(wx.EVT_BUTTON, self.OnSaveButton, saveButton)

        # Now do the layout.

        # mainSizer is the top-level one that manages everything
        mainSizer = wx.BoxSizer(wx.VERTICAL)

        # addrSizer is a grid that holds all of the item info
        addrSizer = wx.GridBagSizer(5, 5)
        #addrSizer.AddGrowableCol(1)
        
        addrSizer.Add(itemNumberLabel, (0, 0), (1, 1),
                      wx.ALIGN_RIGHT, wx.ALIGN_CENTER_VERTICAL)
        addrSizer.Add(self.itemNumberTC, (0, 1), (1, 1))

        addrSizer.Add(buyerNumberLabel, (1, 0), (1, 1),
                      wx.ALIGN_RIGHT, wx.ALIGN_CENTER_VERTICAL)
        addrSizer.Add(self.buyerNumberTC, (1, 1), (1, 1))
        
        addrSizer.Add(winningBidLabel, (2, 0), (1, 1),
                      wx.ALIGN_RIGHT, wx.ALIGN_CENTER_VERTICAL)
        addrSizer.Add(self.winningBidTC, (2, 1), (1, 1))
        
        mainSizer.Add(addrSizer, 0, wx.EXPAND | wx.ALL, 10)
        
        # Now a buttonSizer for the two buttons.
        buttonSizer = wx.BoxSizer(wx.HORIZONTAL)
        buttonSizer.Add((20, 20), 1)
        buttonSizer.Add(cancelButton)
        buttonSizer.Add((20, 20), 1)
        buttonSizer.Add(saveButton)
        buttonSizer.Add((20, 20), 1)
        
        # Now add the addrSizer to the mainSizer
        mainSizer.Add(buttonSizer, 0, wx.EXPAND | wx.BOTTOM, 10)

        self.SetSizer(mainSizer)

        # Fit the frame to the needs of the sizer.  The frame will
        # automatically resize the panel as needed.  Also prevent the
        # frame from getting smaller than this size.
        mainSizer.Fit(parent)
        mainSizer.SetSizeHints(parent)
        
    def OnCancelButton(self, event):
        self.ClearAll()

        
    def OnSaveButton(self, event):
        try:
            itemNumber = self.itemNumberTC.GetValue()
            if len(itemNumber) != 3 or \
                    regularexpression.CheckItemNumber(itemNumber) is None:
                dialogs.displayErrorDialog(
                    "The Item number must be a three-digit decimal number.")
                return
                
            ## Can't add or change the item number to a value 
            ## not in the database.
            if not self.items.isValidItemNumber(self.samdb, itemNumber):
                dialogs.displayErrorDialog ('Item number ' + \
                                itemNumber + ' is not registered.')
                if self.function == 'edit':
                    self.itemNumberTC.SetValue(self.oldItemNumber)
                return

            buyerNumber = self.buyerNumberTC.GetValue()
            if len(buyerNumber) != 3 or \
                        regularexpression.CheckBuyerNumber(buyerNumber) \
                            is None:
                dialogs.displayErrorDialog \
                    ("The buyer number must be a three-digit decimal number.")
                return
     
            # Can't change buyer number to a value thats not in the database.
            if not self.buyers.isValidBuyerNumber(self.samdb, buyerNumber):
                dialogs.displayErrorDialog ('Buyer number ' + \
                                buyerNumber + ' is not registered.')
                if self.function == 'edit':
                    self.buyerNumberTC.SetValue(self.oldBuyerNumber)
                return
            
            ### ENSURE THAT THE SAME ITEM CANt BE PURCHASED BY TWO BUYERS!!!
            if self.function == 'add':
                otherBuyerNumber = self.items.checkItemHasBuyer \
                                (itemNumber, self.samdb)
                if otherBuyerNumber is not None:
                    dialogs.displayErrorDialog ('Item number ' + itemNumber + \
                                ' has already been purchased by buyer ' + \
                                otherBuyerNumber)
                    self.itemNumberTC.Clear()
                    return
            ''' Don't know why this is here
            elif self.function == 'edit':
                self.buyerNumberTC.SetValue(self.oldBuyerNumber)
            '''
             
            winningBid = self.winningBidTC.GetValue()
            if len(winningBid) == 0 or \
                        regularexpression.CheckMoney(winningBid) == False:
                dialogs.displayErrorDialog \
                    ("The winning bid must be a decimal number "\
                     + "greater than zero.")
                return

            ''' Now that all the data are valid, we can do the most
                straightforward task, which is to purchase the item. '''
            if self.function == 'add':
                self.purchases.purchaseItem(self.samdb, itemNumber, \
                            buyerNumber, winningBid)
                self.ClearAll()
                return
            
            ## It's a bit trickier for editing because we can't change
            ## the item number to a nonexistent value (already chaecked)
            ## or to the number of an item already purchased
            if self.function == 'edit':
                if not itemNumber == self.oldItemNumber:
                    ## if new item number is registered and not purchased, 
                    ## then it's okay to change to new item number
                    if self.purchases.hasBeenPurchased \
                                (self.samdb, itemNumber):
                        dialogs.displayErrorDialog \
                            ('Item number ' + itemNumber + \
                             ' has already been purchased.')
                        self.itemNumberTC = self.oldItemNumber
                        return
                if not dialogs.displayYesNoDialog('Change purchase to '
                        + '\n   Item number  ' + itemNumber
                        + '\n   Buyer number ' + buyerNumber
                        + '\n   Winning bid  ' + '$' + winningBid):
                    self.ClearAll()
                    return
                    
            if self.function == 'edit' and \
                        itemNumber == self.oldItemNumber:
                self.purchases.purchaseItem(self.samdb, itemNumber, \
                            buyerNumber, winningBid)
            else:
                ### Item number changes so delete, add, and update chooser
                self.purchases.deletePurchase(self.samdb, self.oldItemNumber)
                self.purchases.purchaseItem(self.samdb, itemNumber, \
                            buyerNumber, winningBid)
                self.parent.BuildPurchasedItemChooser(self.samdb)
            # Write all fields for the affected item number.
            self.ClearAll()
            self.con.displayAllPurchases(self.samdb)
        
        except MySQLdb.Error, e:
            dialogs.displayErrorDialog(e.args[1])
            return
        except MySQLdb.Warning, e:
            print("Warning: ", e)
       
    def PopulateForm(self, samdb, itemNumber):
        try:
            row = self.purchases.fetchPurchase(samdb, itemNumber)
        except MySQLdb.Error, e:
            dialogs.displayErrorDialog(e.args[1])
            return
        except MySQLdb.Warning, e:
            print("Warning: ", e)

        # Now put all the values into the form
        self.itemNumberTC.SetValue(itemNumber)
        self.buyerNumberTC.SetValue(row[0])
        self.winningBidTC.SetValue(str(row[1]))
        self.oldItemNumber = itemNumber
        self.oldBuyerNumber = row[0]  # can't change to an invalid buyer #
        self.oldWinningBid = row[1]
   
    def ClearAll(self):
        self.itemNumberTC.Clear()
        self.buyerNumberTC.Clear()
        self.winningBidTC.Clear()
    
