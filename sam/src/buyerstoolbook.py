
import  wx
import addpanel
import deletepanel
import editpanel

actions = ['buyeradd', 'buyeredit', 'buyerdelete']

ADDCODE = 0
EDITCODE = 1
DELETECODE = 2

#----------------------------------------------------------------------------
    
    
class BuyersToolbook(wx.Toolbook):
    def __init__(self, parent, id, samdb):
        wx.Toolbook.__init__(self, parent, id, style=wx.BK_TOP)
        
        self.samdb = samdb
        
        il = wx.ImageList(201, 51, True)        
        for action in actions:
            bmp = wx.Bitmap('../otherfiles/images/' + action + '.bmp')
            il.Add(bmp)
        self.AssignImageList(il)
        imageIdGenerator = getNextImageID(il.GetImageCount())
        
        self.addPanel = addpanel.AddPanel(self, self.samdb, 'Buyer')
        self.AddPage(self.addPanel, "", imageId=imageIdGenerator.next())
        
        self.editPanel = editpanel.EditPanel(self, self.samdb, 'Buyer')
        self.AddPage(self.editPanel, '', imageId=imageIdGenerator.next())
     
        self.deletePanel = deletepanel.DeletePanel(self, self.samdb, 'Buyer')
        self.AddPage(self.deletePanel, '', imageId = imageIdGenerator.next())
        
        self.Bind(wx.EVT_TOOLBOOK_PAGE_CHANGED, self.OnPageChanged)
        self.Bind(wx.EVT_TOOLBOOK_PAGE_CHANGING, self.OnPageChanging)
    
    def OnPageChanged(self, event):
        event.Skip()

    def OnPageChanging(self, event):
        ## 0 ==> Add Buyer; 1 ==> Edit Buyer; 2 ==> Buyer Buyer
        new = event.GetSelection()
        if new == EDITCODE:
            self.editPanel.buildBuyerChooser(self.samdb)
            self.editPanel.entryForm.clearAll()
        if new == DELETECODE:
            self.deletePanel.deleteForm.BuildChooser(self.samdb)
        event.Skip()
        

def getNextImageID(count):
    imID = 0
    while True:
        yield imID
        imID += 1
        if imID == count:
            imID = 0


