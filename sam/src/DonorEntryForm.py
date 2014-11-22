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
        self.nameTC = wx.TextCtrl(self, -1, "");
        
        streetLabel = wx.StaticText(self, -1, "Street:")
        self.streetTC = wx.TextCtrl(self, -1, "");
        
        cityStateZipLabel = wx.StaticText(self, -1, "City, State, Zip:")
        self.cityTC  = wx.TextCtrl(self, -1, "", size=(150, -1))
        self.stateTC = wx.TextCtrl(self, -1, "", size=(50, -1))
        self.zipTC   = wx.TextCtrl(self, -1, "", size=(70, -1))

        contactLabel = wx.StaticText(self, -1, "Contact:")
        self.contactTC   = wx.TextCtrl(self, -1, "")
        
        telnoLabel = wx.StaticText(self, -1, "Telephone:")
        self.telnoTC   = wx.TextCtrl(self, -1, "", size=(110, -1))

        emailLabel = wx.StaticText(self, -1, "Email:")
        self.emailTC   = wx.TextCtrl(self, -1, "")

        cancelButton = wx.Button(self, -1, "Cancel")
        self.Bind(wx.EVT_BUTTON, self.OnCancelButton, cancelButton)
        
        saveButton = wx.Button(self, -1, "Save")
        self.Bind(wx.EVT_BUTTON, self.OnSaveButton, saveButton)

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
        
        # Now a subsizer for city, state, and zip
        cityStateZipSizer = wx.BoxSizer(wx.HORIZONTAL)
        cityStateZipSizer.Add(self.cityTC, 1)
        cityStateZipSizer.Add(self.stateTC, 0, wx.LEFT|wx.RIGHT, 5)
        cityStateZipSizer.Add(self.zipTC)
        addrSizer.Add(cityStateZipSizer, 0, wx.EXPAND)
      
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
        
    def OnCancelButton(self, event):
        self.ClearAll()

        
    def OnSaveButton(self, event):
        donorNumber = self.donorNumberTC.GetValue()
        if len(donorNumber) != 3 or \
                    regularexpression.CheckDonorNumber(donorNumber) is None:
            dialogs.DisplayErrorDialog(
                    "The donor number must be a three-digit decimal number.")
            return
        name = self.nameTC.GetValue()
        if not (len(name) > 0):
            dialogs.DisplayErrorDialog("The donor name must not be null.")
            return
        street = self.streetTC.GetValue()
        if not (len(street) > 0):
            dialogs.DisplayErrorDialog("The street name must not be null.")
            return
        city = self.cityTC.GetValue()
        if not (len(city) > 0):
            dialogs.DisplayErrorDialog("The city name must not be null.")
            return
        state = self.stateTC.GetValue().upper()
        if len(state )!= 2 or not (state.isalpha()):
            dialogs.DisplayErrorDialog(
                    "The state must be two alphabetic characters.")
            return
        zip = self.zipTC.GetValue()
        if len(zip) != 5 or regularexpression.CheckZipCode(zip) is None:
            dialogs.DisplayErrorDialog(
                    "The zip code must be a five-digit decimal number.")
            return
        contact = self.contactTC.GetValue()
        if not (len(contact) > 0):
            dialogs.DisplayErrorDialog("The contact name must not be null.")
            return
        telno = self.telnoTC.GetValue()
        if len(telno) != 12 or regularexpression.CheckTelno(telno) is None:
            dialogs.DisplayErrorDialog(
                    "The telephone number must be in the format XXX-XXX-XXXX.")
            return
        email = self.emailTC.GetValue()
        
        if self.function == 'add':
            try:
                self.donors.AddDonor(self.samdb, donorNumber, name, street, \
                            city, state, zip, contact, telno, email)
            except MySQLdb.Error, e:
                dialogs.DisplayErrorDialog(e.args[1])
                return
            except MySQLdb.Warning, e:
                print("Warning: ", e)
        else:
            try:
                self.donors.UpdateDonor(self.samdb, donorNumber, name, street, \
                               city, state, zip, contact, telno, email)
            except MySQLdb.Error, e:
                dialogs.DisplayErrorDialog(e.args[1])
                return
            except MySQLdb.Warning, e:
                print("Warning: ", e)
                           
        self.ClearAll()
        self.con.DisplayDonors(self.samdb)

    def PopulateForm(self, samdb, donorNumber):
        self.donorNumber = donorNumber
        try:
            row = self.donors.FetchDonor(samdb, donorNumber)
        except MySQLdb.Error, e:
            dialogs.DisplayErrorDialog(e.args[1])
            return
        except MySQLdb.Warning, e:
            print("Warning: ", e)

        # Now put all the values into the form
        self.donorNumberTC.SetValue(donorNumber)
        self.nameTC.SetValue(row[0])
        self.streetTC.SetValue(row[1])
        self.cityTC.SetValue(row[2])
        self.stateTC.SetValue(row[3])
        self.zipTC.SetValue(row[4])
        self.contactTC.SetValue(row[5])
        self.telnoTC.SetValue(row[6])
        self.emailTC.SetValue(row[7])
    

    def ClearAll(self):
        self.donorNumberTC.Clear()
        self.nameTC.Clear()
        self.streetTC.Clear()
        self.cityTC.Clear()
        self.stateTC.Clear()
        self.zipTC.Clear()
        self.contactTC.Clear()
        self.telnoTC.Clear()
        self.emailTC.Clear()
    


    