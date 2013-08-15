
import wx
import sys
import PrintOneCartOrReceiptPanel
import PrintAllCartsOrReceiptsPanel
import PrintCartOrReceiptSummaryPanel

actions = ['printone', 'printall', 'printsummary']

#----------------------------------------------------------------------------
    
    
class PrintingToolbook(wx.Toolbook):
    def __init__(self, parent, id, samdb, whatToPrint):
        
        wx.Toolbook.__init__(self, parent, id, style=wx.BK_TOP)
        
        self.samdb = samdb
        
        il = wx.ImageList(201, 51, True)        
        for action in actions:
            bmp = wx.Bitmap('../otherfiles/images/' + action + '.bmp')
            il.Add(bmp)
        self.AssignImageList(il)
        imageIdGenerator = getNextImageID(il.GetImageCount())
        
        self.printOneCartOrReceiptPanel = \
                    PrintOneCartOrReceiptPanel.PrintOneCartOrReceiptPanel( \
                    self, self.samdb, whatToPrint)
        self.AddPage(self.printOneCartOrReceiptPanel, "", \
                     imageId=imageIdGenerator.next())
        
        self.PrintAllCartsOrReceiptsPanel = \
            PrintAllCartsOrReceiptsPanel.PrintAllCartsOrReceiptsPanel( \
                    self, self.samdb, whatToPrint)
        self.AddPage(self.PrintAllCartsOrReceiptsPanel, "", \
                    imageId=imageIdGenerator.next())
        
        self.PrintCartOrReceiptSummaryPanel = \
            PrintCartOrReceiptSummaryPanel.PrintCartOrReceiptSummaryPanel( \
                    self, self.samdb, whatToPrint)
        self.AddPage(self.PrintCartOrReceiptSummaryPanel, "", \
                     imageId=imageIdGenerator.next())
        
        self.Bind(wx.EVT_TOOLBOOK_PAGE_CHANGED, self.OnPageChanged)
        self.Bind(wx.EVT_TOOLBOOK_PAGE_CHANGING, self.OnPageChanging)
    
    def OnPageChanged(self, event):
        event.Skip()

    def OnPageChanging(self, event):
        event.Skip()
        

def getNextImageID(count):
    imID = 0
    while True:
        yield imID
        imID += 1
        if imID == count:
            imID = 0


