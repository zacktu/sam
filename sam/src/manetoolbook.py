
'''
manetoolbook is the first page that is seen after the splash screen and
the database selector.  It has choosers down the left for Donors, Items,
Buyers, Purchases, Carts, and Receipts.

Bob Cannon
module dates from years ago -- header added 19 November 2014
'''

import wx
import buyerstoolbook
import donorstoolbook
import itemstoolbook
import printingtoolbook
import purchasestoolbook

players = ['donors', 'items', 'buyers', 'purchases', 'carts', 'receipts']


#----------------------------------------------------------------------------
wx.Frame
def getNextImageID(count):
    imID = 0
    while True:
        yield imID
        imID += 1
        if imID == count:
            imID = 0
    
    
class manetoolbook(wx.Toolbook):
    def __init__(self, parent, id, samdb):
        wx.Toolbook.__init__(self, parent, id, style=wx.BK_LEFT)

        #### needed?
        self.samdb = samdb

        # make an image list using the LBXX images
        il = wx.ImageList(151, 76)
        for player in players:
            bmp = wx.Bitmap('../otherfiles/images/' + player + '.bmp')
            il.Add(bmp)
        self.AssignImageList(il)
        imageIdGenerator = getNextImageID(il.GetImageCount())
  
        dtb = donorstoolbook.DonorsToolbook(self, -1, self.samdb)
        self.AddPage(dtb, "", imageId=imageIdGenerator.next())

        itb = itemstoolbook.ItemsToolbook(self, -1, self.samdb)
        self.AddPage(itb, "", imageId=imageIdGenerator.next())
        
        btb = buyerstoolbook.BuyersToolbook(self, -1, self.samdb)
        self.AddPage(btb, "", imageId=imageIdGenerator.next())
        
        putb = purchasestoolbook.PurchasesToolbook(self, -1, self.samdb)
        self.AddPage(putb, "", imageId=imageIdGenerator.next())

        self.prtbc = printingtoolbook.PrintingToolbook(self, -1, self.samdb, 'carts')
        self.AddPage(self.prtbc, '', imageId=imageIdGenerator.next())
        
        self.prtbr = printingtoolbook.PrintingToolbook(self, -1, self.samdb, 'receipts')
        self.AddPage(self.prtbr, '', imageId=imageIdGenerator.next())
        
        self.Bind(wx.EVT_TOOLBOOK_PAGE_CHANGED, self.OnPageChanged)
        self.Bind(wx.EVT_TOOLBOOK_PAGE_CHANGING, self.OnPageChanging)

    def OnPageChanged(self, event):
        event.Skip()

    def OnPageChanging(self, event):
        self.evtChanging = event.GetSelection()
        #update the appropriate buyer chooser list in case a buyer has been added
        if (self.evtChanging == 4):
            self.prtbc.pocorp.pbcorf.BuildChooser(self.samdb)
        if (self.evtChanging == 5):
            self.prtbr.pocorp.pbcorf.BuildChooser(self.samdb)
        event.Skip()


