import wx
import MySQLdb
import dialogs
import regularexpression
import donors
import console

class DonorEntryForm(wx.Panel):
    def __init__(self, parent, samdb, function):
        super(DonorEntryForm, self).__init__(parent)

        self.samdb = samdb
        self.function = function
        self.donors = donors.Donors()
        self.con = console.Console()
        
        # First create the controls

        donorNumberLabel = wx.StaticText(self, -1, "Donor #:")
        if function == 'add':
            self.donorNumberTC = wx.TextCtrl(self, -1, "", size=(40, -1), \
                                    style = wx.TE_RIGHT)
        else:
            self.donorNumberTC = wx.TextCtrl(self, -1, "", size=(40, -1), \
                                    style = wx.TE_RIGHT | wx.TE_READONLY)
            
        nameLabel = wx.StaticText(self, -1, "Name:")
        self.nameTC = wx.TextCtrl(self, -1, "", size=(280, -1))
        
        streetLabel = wx.StaticText(self, -1, "Street:")
        self.streetTC = wx.TextCtrl(self, -1, "");
        
        cityStateZipLabel = wx.StaticText(self, -1, "City, State, Zip:")
        self.cityStateZipTC  = wx.TextCtrl(self, -1, "", size=(150, -1))

        contactLabel = wx.StaticText(self, -1, "Contact:")
        self.contactTC   = wx.TextCtrl(self, -1, "")
        
        telnoLabel = wx.StaticText(self, -1, "Telephone:")
        self.telnoTC   = wx.TextCtrl(self, -1, "", size=(110, -1))

        emailLabel = wx.StaticText(self, -1, "Email:")
        self.emailTC   = wx.TextCtrl(self, -1, "")

        cancelButton = wx.Button(self, -1, "Cancel")
        self.Bind(wx.EVT_BUTTON, self.onCancelButton, cancelButton)
        
        saveButton = wx.Button(self, -1, "Save")
        self.Bind(wx.EVT_BUTTON, self.onSaveButton, saveButton)

        # Now do the layout.

        # mainSizer is the top-level one that manages everything
        mainSizer = wx.BoxSizer(wx.VERTICAL)

        # addrSizer is a grid that holds all of the donor info
        addrSizer = wx.FlexGridSizer(cols=2, hgap=5, vgap=5)
        addrSizer.AddGrowableCol(1)
        
        addrSizer.Add(donorNumberLabel, 0,
                      wx.ALIGN_RIGHT, wx.ALIGN_CENTER_VERTICAL)
        addrSizer.Add(self.donorNumberTC, 0)
        
        addrSizer.Add(nameLabel, 0,
                      wx.ALIGN_RIGHT, wx.ALIGN_CENTER_VERTICAL)
        addrSizer.Add(self.nameTC, 0, wx.EXPAND)

        addrSizer.Add(streetLabel, 0,
                      wx.ALIGN_RIGHT, wx.ALIGN_CENTER_VERTICAL)
        addrSizer.Add(self.streetTC, 0, wx.EXPAND)

        addrSizer.Add(cityStateZipLabel, 0,
                      wx.ALIGN_RIGHT, wx.ALIGN_CENTER_VERTICAL)
        addrSizer.Add(self.cityStateZipTC, 0, wx.EXPAND)
      
        addrSizer.Add(contactLabel, 0,
                      wx.ALIGN_RIGHT, wx.ALIGN_CENTER_VERTICAL)
        addrSizer.Add(self.contactTC, 0, wx.EXPAND)  

        addrSizer.Add(telnoLabel, 0,
                      wx.ALIGN_RIGHT, wx.ALIGN_CENTER_VERTICAL)
        addrSizer.Add(self.telnoTC, 0)  
        
        addrSizer.Add(emailLabel, 0,
                      wx.ALIGN_RIGHT, wx.ALIGN_CENTER_VERTICAL)
        addrSizer.Add(self.emailTC, 0, wx.EXPAND)
        
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
        donorNumber = self.donorNumberTC.GetValue()
        if len(donorNumber) != 3 or \
                    regularexpression.checkDonorNumber(donorNumber) is None:
            dialogs.displayErrorDialog(
                    "The donor number must be a three-digit decimal number.")
            return
        name = regularexpression.escapeQuotes(self.nameTC.GetValue())
        if not (len(name) > 0):
            dialogs.displayErrorDialog("The donor name must not be null.")
            return
        street = regularexpression.escapeQuotes(self.streetTC.GetValue())
        if not (len(street) > 0):
            dialogs.displayErrorDialog("The street name must not be null.")
            return
        city = regularexpression.escapeQuotes(self.cityStateZipTC.GetValue())
        if not (len(city) > 0):
            dialogs.displayErrorDialog(
                "The city name and state must not be null.")
            return
        contact = regularexpression.escapeQuotes(self.contactTC.GetValue())
        if not (len(contact) > 0):
            dialogs.displayErrorDialog("The contact name must not be null.")
            return
        telno = self.telnoTC.GetValue()
        if len(telno) != 12 or regularexpression.checkTelno(telno) is None:
            dialogs.displayErrorDialog(
                    "The telephone number must be in the format XXX-XXX-XXXX.")
            return
        email = self.emailTC.GetValue()
        
        if self.function == 'add':
            try:
                self.donors.addDonor(self.samdb, donorNumber, name, street,
                            city, contact, telno, email)
            except MySQLdb.Error, e:
                dialogs.displayErrorDialog(e.args[1])
                return
            except MySQLdb.Warning, e:
                print("Warning: ", e)
        else:
            try:
                self.donors.updateDonor(self.samdb, donorNumber, name, street,
                               city, contact, telno, email)
            except MySQLdb.Error, e:
                dialogs.displayErrorDialog(e.args[1])
                return
            except MySQLdb.Warning, e:
                print("Warning: ", e)
                           
        self.clearAll()
        self.con.displayDonors(self.samdb)

    def populateForm(self, samdb, donorNumber):
        self.donorNumber = donorNumber
        try:
            row = self.donors.fetchDonor(samdb, donorNumber)
        except MySQLdb.Error, e:
            dialogs.displayErrorDialog(e.args[1])
            return
        except MySQLdb.Warning, e:
            print("Warning: ", e)

        # Now put all the values into the form
        self.donorNumberTC.SetValue(donorNumber)
        self.nameTC.SetValue(row[0])
        self.streetTC.SetValue(row[1])
        self.cityStateZipTC.SetValue(row[2])
        self.contactTC.SetValue(row[3])
        self.telnoTC.SetValue(row[4])
        self.emailTC.SetValue(row[5])
    

    def clearAll(self):
        self.donorNumberTC.Clear()
        self.nameTC.Clear()
        self.streetTC.Clear()
        self.cityStateZipTC.Clear()
        self.contactTC.Clear()
        self.telnoTC.Clear()
        self.emailTC.Clear()
    


    