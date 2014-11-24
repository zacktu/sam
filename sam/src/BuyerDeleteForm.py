
import wx
import MySQLdb
import dialogs
import buyers
import console
import ChooserLists

class BuyerDeleteForm(wx.Panel):
    def __init__(self, parent, samdb):
        super(BuyerDeleteForm, self).__init__(parent)
        
        self.samdb = samdb
        self.parent = parent
        self.buyers = buyers.Buyers()
        self.chooserLists = ChooserLists.ChooserLists()
        self.con = console.Console()
        
        mainSizer = wx.BoxSizer(wx.VERTICAL)
        
        self.chooserPanel = wx.Panel(self, -1)
        self.BuildChooser(samdb)

        mainSizer.Add(self.chooserPanel)
        
        self.SetSizer(mainSizer)
        mainSizer.Fit(parent)
        mainSizer.SetSizeHints(parent)

    def OnBuyerNumberChoice(self, event):
        indexToDelete = event.GetSelection()
        buyerNumber = event.GetString()
        if dialogs.DisplayYesNoDialog('Delete buyer number ' + \
                                      buyerNumber + '?'):
            try:
                purchasedItems = self.buyers.getBuyersItems \
                                (self.samdb, buyerNumber)
                if len(purchasedItems) > 0:
                    errorMessage = self.BuildErrorMessage(buyerNumber, \
                                                          purchasedItems)
                    dialogs.DisplayErrorDialog(errorMessage)
                    return
                else:
                    self.buyers.DeleteBuyer(self.samdb, buyerNumber)
                    self.buyerNumberList.pop(indexToDelete)
                    self.buyerNumberChoice.SetItems(self.buyerNumberList)
                    self.DeleteBuyerNumberInBuyerNameList(buyerNumber)
                    self.buyerNameChoice.SetItems(self.buyerNameList)
                    self.con.DisplayBuyers(self.samdb)
                    return
            except MySQLdb.Error, e:
                dialogs.DisplayErrorDialog(e.args[1])
                return
            except MySQLdb.Warning, e:
                print("Warning ", e)
        else:
            return
        
    def OnBuyerNameChoice(self, event):
        indexToDelete = event.GetSelection()
        buyerString = event.GetString()
        buyerNumber = buyerString[:3]
        if dialogs.DisplayYesNoDialog('Delete buyer number ' + \
                                      buyerNumber + '?'):
            try:
                purchasedItems = self.buyers.getBuyersItems \
                                (self.samdb, buyerNumber)
                if len(purchasedItems) > 0:
                    errorMessage = self.BuildErrorMessage(buyerNumber,\
                                                          purchasedItems)
                    dialogs.DisplayErrorDialog(errorMessage)
                    return
                else:
                    self.buyers.DeleteBuyer(self.samdb, buyerNumber)
                    self.buyerNameList.pop(indexToDelete)
                    self.buyerNameChoice.SetItems(self.buyerNameList)
                    self.buyerNumberList.remove(buyerNumber)
                    self.buyerNumberChoice.SetItems(self.buyerNumberList)
                    self.buyerNumberChoice.SetItems(self.buyerNumberList)
                    self.con.DisplayBuyers(self.samdb)
            except MySQLdb.Error, e:
                dialogs.DisplayErrorDialog(e.args[1])
                return
            except MySQLdb.Warning, e:
                print("Warning ", e)
        else:
            return

    def BuildChooser(self, samdb):
        try:
            self.buyerNumberList = self.chooserLists.BuildChooserNumberList \
                            ('buyer', samdb)
            wx.StaticText(self.chooserPanel, -1, \
                          "Select a buyer number:", (15,5))
            self.buyerNumberChoice = wx.Choice(self.chooserPanel, \
                                     -1, (175, 0), \
                                     wx.DefaultSize, self.buyerNumberList, \
                                     wx.CB_DROPDOWN | wx.CB_READONLY)
            self.Bind(wx.EVT_CHOICE, self.OnBuyerNumberChoice, \
                                     self.buyerNumberChoice)
    
            self.buyerNameList = \
                self.chooserLists.BuildChooserNumberAndInfoList('buyer', samdb)
            wx.StaticText(self.chooserPanel, -1, \
                          "Select a buyer name:", (15,40))
            self.buyerNameChoice = wx.Choice(self.chooserPanel, \
                                   -1, (175, 40), \
                                   wx.DefaultSize, self.buyerNameList, \
                                   wx.CB_DROPDOWN | wx.CB_READONLY)
            self.Bind(wx.EVT_CHOICE, self.OnBuyerNameChoice, \
                                     self.buyerNameChoice)
        except MySQLdb.Error, e:
            dialogs.DisplayErrorDialog(e.args[1])
            return
        except MySQLdb.Warning, e:
            print("Warning ", e)

    def DeleteBuyerNumberInBuyerNameList(self, buyerNumber):
        indexToDelete = 0
        for row in self.buyerNameList:
            if buyerNumber == row[:3]:
                self.buyerNameList.pop(indexToDelete)
                return
            else:
                indexToDelete += 1
        print "DeleteBuyerPanel: Couldn't find matching buyer number ''\
              + 'for buyer name.  This is bad."
        exit()

    def BuildErrorMessage(self, buyerNumber, purchasedItems):
        errorMessage = "Can't delete buyer " + buyerNumber + '.'
        errorMessage += \
            "\nThe following items must be deleted from the buyer's cart."
        for item in purchasedItems:
            errorMessage += '\n     ' + item
        return errorMessage