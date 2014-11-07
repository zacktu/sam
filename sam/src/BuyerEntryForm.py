import wx
import MySQLdb
import Dialogs
import RegularExpression
import buyers
import Console

class BuyerEntryForm(wx.Panel):
    def __init__(self, parent, samdb, function):
        super(BuyerEntryForm, self).__init__(parent)

        self.samdb = samdb
        self.function = function
        self.buyers = buyers.Buyers()
        self.con = Console.Console()
        
        # First create the controls

        buyerNumberLabel = wx.StaticText(self, -1, "Buyer #:")
        if function == 'add':
            self.buyerNumberTC = wx.TextCtrl(self, -1, "", size=(40, -1), \
                                    style = wx.TE_RIGHT)
        else:
            self.buyerNumberTC = wx.TextCtrl(self, -1, "", size=(40, -1), \
                                    style = wx.TE_RIGHT | wx.TE_READONLY)
            
        lastNameLabel = wx.StaticText(self, -1, "Last Name:")
        self.lastNameTC = wx.TextCtrl(self, -1, "", size=(280, -1));
        
        firstNameLabel = wx.StaticText(self, -1, "FirstName:")
        self.firstNameTC = wx.TextCtrl(self, -1, "");
        
        streetLabel = wx.StaticText(self, -1, "Street:")
        self.streetTC = wx.TextCtrl(self, -1, "");
        
        cityStateZipLabel = wx.StaticText(self, -1, "City, State, Zip:")
        self.cityStateZipTC  = wx.TextCtrl(self, -1, "")
        
        telnoLabel = wx.StaticText(self, -1, "Telephone:")
        self.telnoTC   = wx.TextCtrl(self, -1, "", size=(110, -1))

        cancelButton = wx.Button(self, -1, "Cancel")
        self.Bind(wx.EVT_BUTTON, self.OnCancelButton, cancelButton)
        
        saveButton = wx.Button(self, -1, "Save")
        self.Bind(wx.EVT_BUTTON, self.OnSaveButton, saveButton)

        # Now do the layout.

        # mainSizer is the top-level one that manages everything
        mainSizer = wx.BoxSizer(wx.VERTICAL)

        # addrSizer is a grid that holds all of the buyer info
        addrSizer = wx.FlexGridSizer(cols=2, hgap=5, vgap=5)
        addrSizer.AddGrowableCol(1)
        
        addrSizer.Add(buyerNumberLabel, 0,
                      wx.ALIGN_RIGHT, wx.ALIGN_CENTER_VERTICAL)
        addrSizer.Add(self.buyerNumberTC, 0)
        
        addrSizer.Add(lastNameLabel, 0,
                      wx.ALIGN_RIGHT, wx.ALIGN_CENTER_VERTICAL)
        addrSizer.Add(self.lastNameTC, 0, wx.EXPAND)

        addrSizer.Add(firstNameLabel, 0,
                      wx.ALIGN_RIGHT, wx.ALIGN_CENTER_VERTICAL)
        addrSizer.Add(self.firstNameTC, 0, wx.EXPAND)
        
        addrSizer.Add(streetLabel, 0,
                      wx.ALIGN_RIGHT, wx.ALIGN_CENTER_VERTICAL)
        addrSizer.Add(self.streetTC, 0, wx.EXPAND)

        addrSizer.Add(cityStateZipLabel, 0,
                      wx.ALIGN_RIGHT, wx.ALIGN_CENTER_VERTICAL)
        addrSizer.Add(self.cityStateZipTC, 0, wx.EXPAND)

        addrSizer.Add(telnoLabel, 0,
                      wx.ALIGN_RIGHT, wx.ALIGN_CENTER_VERTICAL)
        addrSizer.Add(self.telnoTC, 0)

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
        buyerNumber = self.buyerNumberTC.GetValue()
        if len(buyerNumber) != 3 or \
                    RegularExpression.CheckBuyerNumber(buyerNumber) is None:
            Dialogs.DisplayErrorDialog(
                    "The buyer number must be a three-digit decimal number.")
            return
        
        lastName = self.lastNameTC.GetValue()
        if not (len(lastName) > 0):
            Dialogs.DisplayErrorDialog \
                    ("The buyer's last name must not be null.")
            return
        
        firstName = self.firstNameTC.GetValue()
        if not (len(firstName) > 0):
            Dialogs.DisplayErrorDialog \
                    ("The buyer's first name must not be null.")
            return
        
        street = self.streetTC.GetValue()
        if not (len(street) > 0):
            Dialogs.DisplayErrorDialog("The street name must not be null.")
            return
        
        city = self.cityStateZipTC.GetValue()
        if not (len(city) > 0):
            Dialogs.DisplayErrorDialog("The city name and state must not be null.")
            return
        
        telno = self.telnoTC.GetValue()
        if len(telno) != 12 or RegularExpression.CheckTelno(telno) is None:
            Dialogs.DisplayErrorDialog(
                    "The telephone number must be in the format XXX-XXX-XXXX.")
            return
        
        if self.function == 'add':
            try:
                self.buyers.AddBuyer(self.samdb, buyerNumber, lastName, \
                            firstName, street, city, telno)
            except MySQLdb.Error, e:
                Dialogs.DisplayErrorDialog(e.args[1])
                return
            except MySQLdb.Warning, e:
                print("Warning: ", e)
        else:
            try:
                self.buyers.UpdateBuyer(self.samdb, buyerNumber, lastName, \
                            firstName, street, city, telno)
            except MySQLdb.Error, e:
                Dialogs.DisplayErrorDialog(e.args[1])
                return
            except MySQLdb.Warning, e:
                print("Warning: ", e)
                           
        self.ClearAll()
        self.con.DisplayBuyers(self.samdb)

    def PopulateForm(self, samdb, buyerNumber):
        self.buyerNumber = buyerNumber
        try:
            row = self.buyers.FetchBuyer(samdb, buyerNumber)
        except MySQLdb.Error, e:
            Dialogs.DisplayErrorDialog(e.args[1])
            return
        except MySQLdb.Warning, e:
            print("Warning: ", e)

        # Now put all the values into the form
        self.buyerNumberTC.SetValue(buyerNumber)
        self.lastNameTC.SetValue(row[0])
        self.firstNameTC.SetValue(row[1])
        self.streetTC.SetValue(row[2])
        self.cityStateZipTC.SetValue(row[3])
        self.telnoTC.SetValue(row[4])

    def ClearAll(self):
        self.buyerNumberTC.Clear()
        self.lastNameTC.Clear()
        self.firstNameTC.Clear()
        self.streetTC.Clear()
        self.cityStateZipTC.Clear()
        self.telnoTC.Clear()
    


    