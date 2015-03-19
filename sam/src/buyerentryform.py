import wx
import MySQLdb
import dialogs
import regularexpression
import buyers
import console
import constants

class buyerentryform(wx.Panel):
    def __init__(self, parent, samdb, function):
        super(buyerentryform, self).__init__(parent)

        self.samdb = samdb
        self.function = function
        self.buyers = buyers.Buyers()
        self.con = console.Console()
        
        # First create the controls

        buyerNumberLabel = wx.StaticText(self, -1, "Buyer #:")
        if function == 'add':
            self.buyerNumberTC = wx.TextCtrl(self, -1, "", size=(40, -1), \
                                    style = wx.TE_RIGHT)
        else:
            self.buyerNumberTC = wx.TextCtrl(self, -1, "", size=(40, -1), \
                                    style = wx.TE_RIGHT | wx.TE_READONLY)
            
        lastNameLabel = wx.StaticText(self, -1, "Last Name:")
        self.lastNameTC = wx.TextCtrl(self, -1, "", size=(280, -1))
        
        firstNameLabel = wx.StaticText(self, -1, "FirstName:")
        self.firstNameTC = wx.TextCtrl(self, -1, "");
        
        streetLabel = wx.StaticText(self, -1, "Street:")
        self.streetTC = wx.TextCtrl(self, -1, "");
        
        cityStateZipLabel = wx.StaticText(self, -1, "City, State, Zip:")
        self.cityStateZipTC  = wx.TextCtrl(self, -1, "")
        
        telnoLabel = wx.StaticText(self, -1, "Telephone:")
        self.telnoTC   = wx.TextCtrl(self, -1, "", size=(110, -1))

        cancelButton = wx.Button(self, -1, "Cancel")
        self.Bind(wx.EVT_BUTTON, self.onCancelButton, cancelButton)
        
        saveButton = wx.Button(self, -1, "Save")
        self.Bind(wx.EVT_BUTTON, self.onSaveButton, saveButton)

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
        
    def onCancelButton(self, event):
        self.clearAll()
        
    def onSaveButton(self, event):
        buyerNumber = self.buyerNumberTC.GetValue()
        if len(buyerNumber) != 3 or \
                    regularexpression.checkBuyerNumber(buyerNumber) is None:
            dialogs.displayErrorDialog(
                    "The buyer number must be a three-digit decimal number.")
            return
        
        lastName = regularexpression.escapeQuotes(self.lastNameTC.GetValue())
        if not (len(lastName) > 0):
            dialogs.displayErrorDialog \
                    ("The buyer's last name must not be null.")
            return
        
        firstName = regularexpression.escapeQuotes(self.firstNameTC.GetValue())
        if not (len(firstName) > 0):
            dialogs.displayErrorDialog \
                    ("The buyer's first name must not be null.")
            return
        
        street = regularexpression.escapeQuotes(self.streetTC.GetValue())
        if ((len(street) == 0) and (constants.REQUIREBUYERADDRESS)):
            dialogs.displayErrorDialog("The street name must not be null.")
            return
        
        city = regularexpression.escapeQuotes(self.cityStateZipTC.GetValue())
        if ((len(city) == 0) and (constants.REQUIREBUYERADDRESS)):
            dialogs.displayErrorDialog("The city name must not be null.")
            return

        telno = self.telnoTC.GetValue()
        if constants.REQUIREBUYERTELNO:
            if len(telno) == 0:
                dialogs.displayErrorDialog(
                    "The telephone number must not be null.")
                return
            elif len(telno) != 12 \
                    or regularexpression.checkTelno(telno) is None:
                dialogs.displayErrorDialog(
                    "The telephone number must be in the format XXX-XXX-XXXX.")
                return
        elif len(telno) > 0:
            if len(telno) != 12 or regularexpression.checkTelno(telno) is None:
                dialogs.displayErrorDialog(
                    "The telephone number must be in the format XXX-XXX-XXXX.")
                return
        
        if self.function == 'add':
            try:
                self.buyers.addBuyer(self.samdb, buyerNumber, lastName, \
                            firstName, street, city, telno)
            except MySQLdb.Error, e:
                dialogs.displayErrorDialog(e.args[1])
                return
            except MySQLdb.Warning, e:
                print("Warning: ", e)
        else:
            try:
                self.buyers.updateBuyer(self.samdb, buyerNumber, lastName, \
                            firstName, street, city, telno)
            except MySQLdb.Error, e:
                dialogs.displayErrorDialog(e.args[1])
                return
            except MySQLdb.Warning, e:
                print("Warning: ", e)
                           
        self.clearAll()
        self.con.displayBuyers(self.samdb)

    def populateForm(self, samdb, buyerNumber):
        self.buyerNumber = buyerNumber
        try:
            row = self.buyers.fetchBuyer(samdb, buyerNumber)
        except MySQLdb.Error, e:
            dialogs.displayErrorDialog(e.args[1])
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

    def clearAll(self):
        self.buyerNumberTC.Clear()
        self.lastNameTC.Clear()
        self.firstNameTC.Clear()
        self.streetTC.Clear()
        self.cityStateZipTC.Clear()
        self.telnoTC.Clear()
    


    