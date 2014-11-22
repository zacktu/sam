
import wx
import MySQLdb
import dialogs
import donors
import console
import ChooserLists

class DonorDeleteForm(wx.Panel):
    def __init__(self, parent, samdb):
        super(DonorDeleteForm, self).__init__(parent)
        
        self.samdb = samdb
        self.parent = parent
        self.donors = donors.Donors()
        self.chooserLists = ChooserLists.ChooserLists()
        self.con = console.Console()
        
        mainSizer = wx.BoxSizer(wx.VERTICAL)
        
        self.chooserPanel = wx.Panel(self, -1)
        self.BuildChooser(samdb)

        mainSizer.Add(self.chooserPanel)
        
        self.SetSizer(mainSizer)
        mainSizer.Fit(parent)
        mainSizer.SetSizeHints(parent)

    def OnDonorNumberChoice(self, event):
        indexToDelete = event.GetSelection()
        donorNumber = event.GetString()
        if dialogs.DisplayYesNoDialog('Delete donor number ' + \
                                      donorNumber + '?'):
            try:
                donatedItems = self.donors.GetDonorsItems \
                                (donorNumber, self.samdb)
                if len(donatedItems) > 0:
                    errorMessage = self.BuildErrorMessage(donorNumber, donatedItems)
                    dialogs.DisplayErrorDialog(errorMessage)
                    return
                else:
                    self.donors.DeleteDonor(self.samdb, donorNumber)
                    self.donorNumberList.pop(indexToDelete)
                    self.donorNumberChoice.SetItems(self.donorNumberList)
                    self.DeleteDonorNumberInDonorNameList(donorNumber)
                    self.donorNameChoice.SetItems(self.donorNameList)
                    self.con.DisplayDonors(self.samdb)
                    return
            except MySQLdb.Error, e:
                dialogs.DisplayErrorDialog(e.args[1])
                return
            except MySQLdb.Warning, e:
                print("Warning ", e)
        else:
            return
        
    def OnDonorNameChoice(self, event):
        indexToDelete = event.GetSelection()
        donorString = event.GetString()
        donorNumber = donorString[:3]
        if dialogs.DisplayYesNoDialog('Delete donor number ' + \
                                      donorNumber + '?'):
            donatedItems = self.donors.GetDonorsItems \
                            (donorNumber, self.samdb)
            if len(donatedItems) > 0:
                errorMessage = self.BuildErrorMessage(donorNumber, donatedItems)
                dialogs.DisplayErrorDialog(errorMessage)
                return
            else:
                self.donors.DeleteDonor(self.samdb, donorNumber)
                self.donorNameList.pop(indexToDelete)
                self.donorNameChoice.SetItems(self.donorNameList)
                self.donorNumberList.remove(donorNumber)
                self.donorNumberChoice.SetItems(self.donorNumberList)
                self.donorNumberChoice.SetItems(self.donorNumberList)
                self.con.DisplayDonors(self.samdb)
        else:
            return

    def BuildChooser(self, samdb):
        try:
            self.donorNumberList = self.chooserLists.BuildChooserNumberList \
                                    ('donor', samdb)
            wx.StaticText(self.chooserPanel, -1, \
                          "Select a donor number:", (15,5))
            self.donorNumberChoice = wx.Choice(self.chooserPanel, \
                                -1, (175, 0), \
                                wx.DefaultSize, self.donorNumberList, \
                                wx.CB_DROPDOWN | wx.CB_READONLY)
            self.Bind(wx.EVT_CHOICE, self.OnDonorNumberChoice, \
                                     self.donorNumberChoice)

            self.donorNameList = \
                self.chooserLists.BuildChooserNumberAndInfoList \
                                ('donor', samdb)
            wx.StaticText(self.chooserPanel, -1, \
                          "Select a donor name:", (15,40))
            self.donorNameChoice = wx.Choice(self.chooserPanel, \
                                   -1, (175, 40), \
                                   wx.DefaultSize, self.donorNameList, \
                                   wx.CB_DROPDOWN | wx.CB_READONLY)
            self.Bind(wx.EVT_CHOICE, self.OnDonorNameChoice, \
                                     self.donorNameChoice)
        except MySQLdb.Error, e:
            dialogs.DisplayErrorDialog(e.args[1])
            return
        except MySQLdb.Warning, e:
            print("Warning ", e)

    def DeleteDonorNumberInDonorNameList(self, donorNumber):
        indexToDelete = 0
        for row in self.donorNameList:
            if donorNumber == row[:3]:
                self.donorNameList.pop(indexToDelete)
                return
            else:
                indexToDelete += 1
        print "DeleteDonorPanel: Couldn't find matching donor number ''\
              + 'for donor name.  This is bad."
        exit()

    def BuildErrorMessage(self, donorNumber, donatedItems):
        errorMessage = "Can't delete donor " + donorNumber + '.'
        errorMessage += '\nThe following items must be deleted.'
        for item in donatedItems:
            errorMessage += '\n     ' + item
        return errorMessage