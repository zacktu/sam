
import wx
import BuyersToolbook
import DonorsToolbook
import ItemsToolbook
import PrintingToolbook
import PurchasesToolbook

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
    
    
class ManeToolbook(wx.Toolbook):
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
  
        dtb = DonorsToolbook.DonorsToolbook(self, -1, self.samdb)
        self.AddPage(dtb, "", imageId=imageIdGenerator.next())

        itb = ItemsToolbook.ItemsToolbook(self, -1, self.samdb)
        self.AddPage(itb, "", imageId=imageIdGenerator.next())
        
        btb = BuyersToolbook.BuyersToolbook(self, -1, self.samdb)
        self.AddPage(btb, "", imageId=imageIdGenerator.next())
        
        putb = PurchasesToolbook.PurchasesToolbook(self, -1, self.samdb)
        self.AddPage(putb, "", imageId=imageIdGenerator.next())

        self.prtbc = PrintingToolbook.PrintingToolbook(self, -1, self.samdb, 'carts')
        #self.prtbc.trythis()
        self.AddPage(self.prtbc, '', imageId=imageIdGenerator.next())
        
        self.prtbr = PrintingToolbook.PrintingToolbook(self, -1, self.samdb, 'receipts')
        self.AddPage(self.prtbr, '', imageId=imageIdGenerator.next())
        
        self.Bind(wx.EVT_TOOLBOOK_PAGE_CHANGED, self.OnPageChanged)
        self.Bind(wx.EVT_TOOLBOOK_PAGE_CHANGING, self.OnPageChanging)

    def OnPageChanged(self, event):
        event.Skip()

    def OnPageChanging(self, event):
        self.evtChanging = event.GetSelection()
        print("evtChanging = ", self.evtChanging)
        if (self.evtChanging == 4):
            print("Carts button pressed")
            self.prtbc.tryThis("carts")
            self.prtbc.pocorp.tryThis("carts")
            self.prtbc.pocorp.pbcorf.tryThis("carts")
            self.prtbc.pocorp.pbcorf.BuildChooser(self.samdb)
        if (self.evtChanging == 5):
            print("Receipts button pressed")
            self.prtbr.tryThis("receipts")
            self.prtbr.pocorp.tryThis("receipts")
            self.prtbr.pocorp.pbcorf.BuildChooser(self.samdb)
        event.Skip()


