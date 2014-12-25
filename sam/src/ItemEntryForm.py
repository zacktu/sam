import wx
import MySQLdb
import dialogs
import regularexpression
import donors
import items
import console

class ItemEntryForm(wx.Panel):
    def __init__(self, parent, samdb, function):
        super(ItemEntryForm, self).__init__(parent)

        self.samdb = samdb
        self.function = function
        self.items = items.Items()
        self.donors = donors.Donors()
        self.con = console.Console()
        
        # First create the controls

        itemNumberLabel = wx.StaticText(self, -1, "Item #:")
        if function == 'add':
            self.itemNumberTC = wx.TextCtrl(self, -1, "", size=(40, -1), \
                                        style = wx.TE_RIGHT)
        else:
            self.itemNumberTC = wx.TextCtrl(self, -1, "", size=(40, -1), \
                                        style = wx.TE_RIGHT | wx.TE_READONLY)
        
        itemDescriptionLabel = wx.StaticText(self, -1, "Description:")
        #self.itemDescriptionTC = wx.TextCtrl(self, -1, "", size=(200, -1))
        self.itemDescriptionTC = wx.TextCtrl(self, -1, "")
        
        donorNumberLabel = wx.StaticText(self, -1, "Donor #:")
        self.donorNumberTC = wx.TextCtrl(self, -1, "", size=(40,-1), \
                                         style = wx.TE_RIGHT)
        
        retailPriceLabel = wx.StaticText(self, -1, "Retail Price:")
        self.retailPriceTC = wx.TextCtrl(self, -1, "", size=(50, -1), \
                                         style = wx.TE_RIGHT)
        
        minimumBidLabel = wx.StaticText(self, -1, "Minimum Bid:")
        self.minimumBidTC = wx.TextCtrl(self, -1, "", size=(50, -1), \
                                        style = wx.TE_RIGHT)
        
        incrementLabel = wx.StaticText(self, -1, "Increment:")
        self.incrementTC = wx.TextCtrl(self, -1, "", size=(50, -1), \
                                        style = wx.TE_RIGHT)

        cancelButton = wx.Button(self, -1, "Cancel")
        self.Bind(wx.EVT_BUTTON, self.OnCancelButton, cancelButton)
        
        saveButton = wx.Button(self, -1, "Save")
        self.Bind(wx.EVT_BUTTON, self.OnSaveButton, saveButton)

        # Now do the layout.

        # mainSizer is the top-level one that manages everything
        mainSizer = wx.BoxSizer(wx.VERTICAL)

        # addrSizer is a grid that holds all of the item info
        addrSizer = wx.GridBagSizer(5,5)
        #addrSizer.AddGrowableCol(1)
        
        addrSizer.Add(itemNumberLabel, (0, 0), (1, 1),
                      wx.ALIGN_RIGHT, wx.ALIGN_CENTER_VERTICAL)
        addrSizer.Add(self.itemNumberTC, (0,1), (1,1))

        addrSizer.Add(itemDescriptionLabel, (1,0), (1,1),
                      wx.ALIGN_RIGHT, wx.ALIGN_CENTER_VERTICAL)
        addrSizer.Add(self.itemDescriptionTC, (1,1), (1,5), wx.EXPAND)

        addrSizer.Add(donorNumberLabel, (2,0), (1,1),
                      wx.ALIGN_RIGHT, wx.ALIGN_CENTER_VERTICAL)
        addrSizer.Add(self.donorNumberTC, (2,1), (1,1))

        addrSizer.Add(retailPriceLabel, (3,0), (1,1),
                      wx.ALIGN_RIGHT, wx.ALIGN_CENTER_VERTICAL)
        addrSizer.Add(self.retailPriceTC, (3,1), (1,1))
        
        addrSizer.Add(minimumBidLabel, (3,2), (1, 1),
                      wx.ALIGN_RIGHT, wx.ALIGN_CENTER_VERTICAL)
        addrSizer.Add(self.minimumBidTC, (3,3), (1,1))
        
        addrSizer.Add(incrementLabel, (3,4), (1, 1),
                      wx.ALIGN_RIGHT, wx.ALIGN_CENTER_VERTICAL)
        addrSizer.Add(self.incrementTC, (3,5), (1,1))
        
        mainSizer.Add(addrSizer, 0, wx.EXPAND|wx.ALL, 10)
        
        # Now a buttonSizer for the two buttons.
        buttonSizer = wx.BoxSizer(wx.HORIZONTAL)
        buttonSizer.Add((20,20), 1)
        buttonSizer.Add(cancelButton)
        buttonSizer.Add((20,20), 1)
        buttonSizer.Add(saveButton)
        buttonSizer.Add((20,20), 1)
        
        # Now add the addrSizer to the mainSizer
        mainSizer.Add(buttonSizer, 0, wx.EXPAND|wx.BOTTOM, 10)

        self.SetSizer(mainSizer)

        # Fit the frame to the needs of the sizer.  The frame will
        # automatically resize the panel as needed.  Also prevent the
        # frame from getting smaller than this size.
        mainSizer.Fit(parent)
        mainSizer.SetSizeHints(parent)
        
    def OnCancelButton(self, event):
        self.ClearAll()

        
    def OnSaveButton(self, event):
        itemNumber = self.itemNumberTC.GetValue()
        if len(itemNumber) != 3 or \
                    regularexpression.CheckItemNumber(itemNumber) is None:
            dialogs.displayErrorDialog(
                    "The Item number must be a three-digit decimal number.")
            return
        description = self.itemDescriptionTC.GetValue()
        if not (len(description) > 0):
            dialogs.displayErrorDialog \
                        ("The item description must not be null.")
            return
        donorNumber = self.donorNumberTC.GetValue()
        if len(donorNumber) != 3 or \
                    regularexpression.CheckDonorNumber(donorNumber) \
                        is None:
            dialogs.displayErrorDialog \
                    ("The Donor number must be a three-digit decimal number.")
            return
 
        # Can't change the donor number to a value thats not in the database.
        try:
            if not self.donors.isValidDonorNumber(self.samdb, donorNumber):
                dialogs.displayErrorDialog ('Donor number ' + \
                                donorNumber + ' is not registered.')
                if self.function == 'edit':
                    self.donorNumberTC.SetValue(self.oldDonorNumber)
                return
        except MySQLdb.Error, e:
            dialogs.displayErrorDialog(e.args[1])
            return
        except MySQLdb.Warning, e:
            print("Warning: ", e)
            
        retailPrice = self.retailPriceTC.GetValue()
        if regularexpression.CheckMoney(retailPrice) == False:
            dialogs.displayErrorDialog \
                    ("The retail price must be a decimal number.")
            return
        minimumBid = self.minimumBidTC.GetValue()
        if regularexpression.CheckMoney(minimumBid) == False:
            dialogs.displayErrorDialog \
                ("The minimum bid must be a decimal number.")
            return
        increment = self.incrementTC.GetValue()
        if regularexpression.CheckMoney(increment) == False:
            dialogs.displayErrorDialog \
                ("The increment must be a decimal number.")
            return
 
        if self.function == 'add':
            try:
                self.items.addItem(self.samdb, itemNumber, description, \
                           donorNumber, retailPrice, minimumBid, increment)
            except MySQLdb.Error, e:
                dialogs.displayErrorDialog(e.args[1])
                return
            except MySQLdb.Warning, e:
                print("Warning: ", e)
        elif self.function == 'edit':
            try:
                self.items.updateItem(self.samdb, itemNumber, description, \
                              donorNumber, retailPrice, minimumBid, increment)
            except MySQLdb.Error, e:
                dialogs.displayErrorDialog(e.args[1])
                return
            except MySQLdb.Warning, e:
                print("Warning: ", e) 
        else:
            print "IN EDITENTRYFORM DANGLING ELSE"
            exit()        

        self.ClearAll()
        self.con.displayItems(self.samdb)
       
    def PopulateForm(self, samdb, itemNumber):
        try:
            row = self.items.fetchItem(samdb, itemNumber)
        except MySQLdb.Error, e:
            dialogs.displayErrorDialog(e.args[1])
            return
        except MySQLdb.Warning, e:
            print("Warning: ", e)

        # Now put all the values into the form
        self.itemNumberTC.SetValue(itemNumber)
        self.itemDescriptionTC.SetValue(row[0])
        self.donorNumberTC.SetValue(row[1])
        self.oldDonorNumber = str(row[1])  # can't change to an invalid donor #
        self.retailPriceTC.SetValue(str(row[2]))
        self.minimumBidTC.SetValue(str(row[3]))
        self.incrementTC.SetValue(str(row[4]))
   
    def ClearAll(self):
        self.itemNumberTC.Clear()
        self.itemDescriptionTC.Clear()
        self.donorNumberTC.Clear()
        self.retailPriceTC.Clear()
        self.minimumBidTC.Clear()
        self.incrementTC.Clear()
    