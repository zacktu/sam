'''
Created on Aug 9, 2010
A panel for editing donors, items, and buyers.
@author: bob
'''

import wx
import donorentryform
import buyerentryform
import itementryform
import purchaseentryform
import MySQLdb
import dialogs

class EditPanel(wx.Panel):
    def __init__(self, parent, samdb, player):
        super(EditPanel, self).__init__(parent)

        self.samdb = samdb
        
        # First create the controls
        topLbl = wx.StaticText(self, -1, "Edit " + player)
        topLbl.SetFont(wx.Font(18, wx.SWISS, wx.NORMAL, wx.BOLD))

        # mainSizer is the top-level one that manages everything
        mainSizer = wx.BoxSizer(wx.VERTICAL)
        mainSizer.Add(topLbl, 0, wx.ALL, 5)
        mainSizer.Add(wx.StaticLine(self), 0, wx.EXPAND|wx.TOP|wx.BOTTOM, 5)
        
        self.chooserPanel = wx.Panel(self, -1)
        if player == 'Donor':
            donorList = self.buildDonorList(samdb)
            wx.StaticText(self.chooserPanel, -1, \
                            "Select a donor number:", (15,5))
            choice = wx.Choice(self.chooserPanel, -1, (175, 0), \
                               wx.DefaultSize, donorList, \
                               wx.CB_DROPDOWN | wx.CB_READONLY | wx.CB_SORT)
            self.Bind(wx.EVT_CHOICE, self.onChoice, choice)
        elif player == 'Item':
            itemList = self.buildItemList(samdb)
            wx.StaticText(self.chooserPanel, -1, \
                          "Select an item number:", (15,5))
            choice = wx.Choice(self.chooserPanel, -1, (175, 0), \
                               wx.DefaultSize, itemList, \
                               wx.CB_DROPDOWN | wx.CB_READONLY | wx.CB_SORT)
            self.Bind(wx.EVT_CHOICE, self.onChoice, choice)
        elif player == 'Buyer':
            buyerList = self.buildBuyerList(samdb)
            wx.StaticText(self.chooserPanel, -1, \
                          "Select a buyer number:", (15,5))
            choice = wx.Choice(self.chooserPanel, -1, (175, 0), \
                               wx.DefaultSize, buyerList, \
                               wx.CB_DROPDOWN | wx.CB_READONLY | wx.CB_SORT)
            self.Bind(wx.EVT_CHOICE, self.onChoice, choice)
        elif player == 'Purchase':
            purchasedItemList = self.buildPurchasedItemList(samdb)
            wx.StaticText(self.chooserPanel, -1, \
                          "Select an item number:", (15,5))
            choice = wx.Choice(self.chooserPanel, -1, (175, 0), \
                               wx.DefaultSize, purchasedItemList, \
                               wx.CB_DROPDOWN | wx.CB_READONLY | wx.CB_SORT)
            self.Bind(wx.EVT_CHOICE, self.onChoice, choice)
            
        mainSizer.Add(self.chooserPanel)
        
        if player == 'Donor':
            self.entryForm = donorentryform.DonorEntryForm \
                        (self, samdb, 'edit')
        elif player == 'Item':
            self.entryForm = itementryform.itementryform \
                        (self, samdb, 'edit')
        elif player == 'Buyer':
            self.entryForm = buyerentryform.buyerentryform \
                        (self, samdb, 'edit')
        elif player == 'Purchase':
            self.entryForm = purchaseentryform.PurchaseEntryForm \
                        (self, samdb, 'edit')
       
        mainSizer.Add(self.entryForm)
             
        self.SetSizer(mainSizer)

        # Fit the frame to the needs of the sizer.  The frame will
        # automatically resize the panel as needed.  Also prevent the
        # frame from getting smaller than this size.
        mainSizer.Fit(parent)
        mainSizer.SetSizeHints(parent)
        
        '''  D O N O R S  '''

    def buildDonorChooser(self, samdb):
        donorList = self.buildDonorList(samdb)
        choice = wx.Choice(self.chooserPanel, -1, (175, 0), wx.DefaultSize, \
                               donorList, \
                               wx.CB_DROPDOWN | wx.CB_READONLY | wx.CB_SORT)
        self.Bind(wx.EVT_CHOICE, self.onChoice, choice)

    def buildDonorList(self, samdb):
        query = "SELECT donor_Number FROM Donors ORDER BY donor_number;"
        try:
            rows = samdb.fetchRows(query)
        except MySQLdb.Error, e:
            dialogs.displayErrorDialog(e.args[1])
            return
        except MySQLdb.Warning, e:
            print("Warning: ", e)
        donorList = []
        for row in rows:
            donorList.append(row[0])
        return donorList
        
    def clearDonorForm(self):
        self.donorForm.clearAll()
        
    ''' I T E M S '''
 
    def buildItemChooser(self, samdb):
        itemList = self.buildItemList(samdb)
        choice = wx.Choice(self.chooserPanel, -1, (175, 0), wx.DefaultSize, \
                               itemList, \
                               wx.CB_DROPDOWN | wx.CB_READONLY | wx.CB_SORT)
        self.Bind(wx.EVT_CHOICE, self.onChoice, choice)
        
    def buildItemList(self, samdb):
        query = "SELECT item_Number FROM Items ORDER BY item_number;"
        try:
            rows = samdb.fetchRows(query)
        except MySQLdb.Error, e:
            dialogs.displayErrorDialog(e.args[1])
            return
        except MySQLdb.Warning, e:
            print("Warning: ", e)
        itemList = []
        for row in rows:
            itemList.append(row[0])
        return itemList
        
    ''' BUYERS '''
        
    def buildBuyerChooser(self, samdb):
        buyerList = self.buildBuyerList(samdb)
        choice = wx.Choice(self.chooserPanel, -1, (175, 0), wx.DefaultSize, \
                               buyerList, \
                               wx.CB_DROPDOWN | wx.CB_READONLY | wx.CB_SORT)
        self.Bind(wx.EVT_CHOICE, self.onChoice, choice)

    def buildBuyerList(self, samdb):
        query = "SELECT buyer_Number FROM Buyers ORDER BY buyer_number;"
        try:
            rows = samdb.fetchRows(query)
        except MySQLdb.Error, e:
            dialogs.displayErrorDialog(e.args[1])
            return
        except MySQLdb.Warning, e:
            print("Warning: ", e)
        buyerList = []
        for row in rows:
            buyerList.append(row[0])
        return buyerList       
        
    def ClearForm(self):
        self.entryForm.ClearAll()
        
    ''' PURCHASES '''
    
    def buildPurchasedItemChooser(self, samdb):
        purchasedItemList = self.buildPurchasedItemList(samdb)
        choice = wx.Choice(self.chooserPanel, -1, (175, 0), wx.DefaultSize, \
                               purchasedItemList, \
                               wx.CB_DROPDOWN | wx.CB_READONLY | wx.CB_SORT)
        self.Bind(wx.EVT_CHOICE, self.onChoice, choice)
        
    def buildPurchasedItemList(self, samdb):
        query = "SELECT item_Number FROM Items \
            WHERE item_purchasedby IS NOT NULL \
            AND item_salesprice IS NOT NULL \
            ORDER BY item_number;"
        try:
            rows = samdb.fetchRows(query)
        except MySQLdb.Error, e:
            dialogs.displayErrorDialog(e.args[1])
            return
        except MySQLdb.Warning, e:
            print("Warning: ", e)
        itemList = []
        for row in rows:
            itemList.append(row[0])
        return itemList
        
    '''
    User chooses the donor for whom changes will be made.  Will populate the same
    form that is used for adding donors.
    '''
    def onChoice(self, event):
        dbKey = event.GetString()
        self.entryForm.populateForm(self.samdb, dbKey)

