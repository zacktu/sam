
import wx
import MySQLdb
import dialogs
import buyers
import console
import chooserlists
import printingservices
import PrintOrPreviewDialog

''' This is for printing the shopping cart for a single buyer.  The init sets
    up PrintingServices and a chooser.  Two other methods in this class
    allow choice of the buyer by either buyer number or buyer name. '''

class PrintBuyerCartOrReceiptForm(wx.Panel):
    def __init__(self, parent, samdb, whatToPrint):
        super(PrintBuyerCartOrReceiptForm, self).__init__(parent)
        
        self.samdb = samdb
        self.parent = parent
        self.buyers = buyers.Buyers()
        self.chooserLists = chooserlists.ChooserLists()
        self.whatToPrint = whatToPrint
        self.con = console.Console()
        
        mainSizer = wx.BoxSizer(wx.VERTICAL)
        
        self.chooserPanel = wx.Panel(self, -1)
        self.BuildChooser(samdb)

        mainSizer.Add(self.chooserPanel)
        
        self.SetSizer(mainSizer)
        mainSizer.Fit(parent)
        mainSizer.SetSizeHints(parent)

        if self.whatToPrint == 'carts':
            self.message = 'Preview or print shopping cart for buyer '
        else:
            self.message = 'Preview or print receipt for buyer '
            
    ''' Allows selection of a buyer by buyer number.  A selection widget
        displays all of the buyer numbers.  This code is used elsewhere. 
        I should refactor so that there is only one copy.'''
    def OnBuyerNumberChoice(self, event):
        self.buyerNumber = event.GetString()
        try:
            self.con.displayPurchases(self.samdb, self.buyerNumber)
            PrintOrPreviewDialog.PrintOrPreviewDialog(self, -1, \
                                'Preview or Print?',
                                self.message + self.buyerNumber + '?',
                                self.buyerNumber, self.samdb, self.whatToPrint)
        except MySQLdb.Error, e:
            dialogs.displayErrorDialog(e.args[1])
            return
        except MySQLdb.Warning, e:
            print("Warning ", e)

        
    ''' Allows selection of a buyer by buyer name.  A selection widget
        displays all of the buyer last names.  This code is used elsewhere. 
        I should refactor so that there is only one copy.'''        
    def OnBuyerNameChoice(self, event):
        buyerString = event.GetString()
        self.buyerNumber = buyerString[:3]
        try:
            self.con.displayPurchases(self.samdb, self.buyerNumber)
            PrintOrPreviewDialog.PrintOrPreviewDialog(self, -1, \
                                'Preview or Print?',
                                self.message + self.buyerNumber + '?',
                                self.buyerNumber, self.samdb, self.whatToPrint)
        except MySQLdb.Error, e:
            dialogs.displayErrorDialog(e.args[1])
            return
        except MySQLdb.Warning, e:
            print("Warning ", e)   
        
    def BuildChooser(self, samdb):
        try:
            self.buyerNumberList = self.chooserLists.buildChooserNumberList \
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
                self.chooserLists.buildChooserNumberAndInfoList('buyer', samdb)
            wx.StaticText(self.chooserPanel, -1, \
                          "Select a buyer name:", (15,40))
            self.buyerNameChoice = wx.Choice(self.chooserPanel, \
                                   -1, (175, 40), \
                                   wx.DefaultSize, self.buyerNameList, \
                                   wx.CB_DROPDOWN | wx.CB_READONLY)
            self.Bind(wx.EVT_CHOICE, self.OnBuyerNameChoice, \
                                     self.buyerNameChoice)
        except MySQLdb.Error, e:
            dialogs.displayErrorDialog(e.args[1])
            return
        except MySQLdb.Warning, e:
            print("Warning ", e)


