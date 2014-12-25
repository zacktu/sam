'''
Created on Aug 9, 2010

@author: bob
'''

import wx
import MySQLdb
import dialogs
import items
import purchases
import console
import ChooserLists

class PurchaseDeleteForm(wx.Panel):
    def __init__(self, parent, samdb):
        super(PurchaseDeleteForm, self).__init__(parent)
        
        self.samdb = samdb
        self.parent = parent
        self.items = items.Items()
        self.purchases = purchases.Purchases()
        self.chooserLists = ChooserLists.ChooserLists()
        self.con = console.Console()
        
        mainSizer = wx.BoxSizer(wx.VERTICAL)
        
        self.chooserPanel = wx.Panel(self, -1)
        self.BuildChooser(samdb)

        mainSizer.Add(self.chooserPanel)
        
        self.SetSizer(mainSizer)
        mainSizer.Fit(parent)
        mainSizer.SetSizeHints(parent)
           

    def OnPurchasedItemNumberChoice(self, event):
        indexToDelete = event.GetSelection()
        purchasedItemNumber = event.GetString()

        try:
            row = self.purchases.FetchPurchase \
                        (self.samdb, purchasedItemNumber)
            buyerNumber = row[0]
            winningBid = str(row[1])
            if not dialogs.displayYesNoDialog('Delete purchase:'
                    + '\n   Item number  ' + purchasedItemNumber
                    + '\n   Buyer number ' + buyerNumber
                    + '\n   Winning bid  ' + '$' + winningBid):
                return
            self.purchases.DeletePurchase(self.samdb, purchasedItemNumber)
            self.purchasedItemNumberList.pop(indexToDelete)
            self.purchasedItemNumberChoice.SetItems \
                    (self.purchasedItemNumberList)
            indexToDelete = \
                    self.FindItemNumberInItemDescriptionList \
                    (purchasedItemNumber)
            self.purchasedItemDescriptionList.pop(indexToDelete)
            self.purchasedItemDescriptionChoice.SetItems \
                        (self.purchasedItemDescriptionList)
            self.con.displayAllPurchases(self.samdb)
        except MySQLdb.Error, e:
            dialogs.displayErrorDialog(e.args[1])
            return
        except MySQLdb.Warning, e:
            print("Warning ", e)
        
    def OnPurchasedItemDescriptionChoice(self, event):
        indexToDelete = event.GetSelection()
        purchasedItemString = event.GetString()
        purchasedItemNumber = purchasedItemString[:3]
        if dialogs.displayYesNoDialog('Delete purchase for item number ' + \
                                      purchasedItemNumber + '?'):
            # Positive buyer number implies that item has been purchased
            buyerNumber = self.items.checkItemHasBuyer \
                            (purchasedItemNumber, self.samdb)
            print 'IN ONPURCHASEDITEMDESCRIPTIONLIST buyerNumber = ', buyerNumber
            if buyerNumber is None:
                dialogs.displayErrorDialog \
                    ('This item has not been purchased.')
                return
            else:
                self.purchases.DeletePurchase    \
                            (self.samdb, purchasedItemNumber)
                self.purchasedItemDescriptionList.pop(indexToDelete)
                self.purchasedItemDescriptionChoice.SetItems \
                            (self.purchasedItemDescriptionList)
                self.purchasedItemNumberList.remove(purchasedItemNumber)
                self.purchasedItemNumberChoice.SetItems \
                            (self.purchasedItemNumberList)
                self.con.displayAllPurchases(self.samdb)
        else:
            return

    def BuildChooser(self, samdb):
        try:
            self.purchasedItemNumberList = \
                            self.chooserLists.BuildChooserNumberList \
                                ('purchase', samdb)
            wx.StaticText(self.chooserPanel, -1, \
                                "Select an item number:", (15,5))
            self.purchasedItemNumberChoice = wx.Choice(self.chooserPanel, \
                                -1, (195, 0), \
                                wx.DefaultSize, \
                                self.purchasedItemNumberList, \
                                wx.CB_DROPDOWN | wx.CB_READONLY)
            self.Bind(wx.EVT_CHOICE, self.OnPurchasedItemNumberChoice, \
                  self.purchasedItemNumberChoice)

            self.purchasedItemDescriptionList = \
                        self.chooserLists.BuildChooserNumberAndInfoList \
                                ('purchase', samdb)
            wx.StaticText(self.chooserPanel, -1, \
                                "Select an item description:", (15,40))
            self.purchasedItemDescriptionChoice = \
                                wx.Choice(self.chooserPanel, -1, (195, 40), \
                                wx.DefaultSize, \
                                self.purchasedItemDescriptionList, \
                                wx.CB_DROPDOWN | wx.CB_READONLY)
            self.Bind(wx.EVT_CHOICE, self.OnPurchasedItemDescriptionChoice, \
                  self.purchasedItemDescriptionChoice)
        except MySQLdb.Error, e:
            dialogs.displayErrorDialog(e.args[1])
            return
        except MySQLdb.Warning, e:
            print("Warning ", e)       

    def FindItemNumberInItemDescriptionList(self, itemNumber):
        indexToDelete = 0
        for row in self.purchasedItemDescriptionList:
            if itemNumber == row[:3]:
                return indexToDelete
                self.purchasedItemDescriptionList.pop(indexToDelete)
                return
            else:
                indexToDelete += 1
        print "DeleteItemPanel: Couldn't find matching item number ''\
              + 'for item description.  This is bad."
        exit()

        