
import  wx
import addpanel
import DeletePanel
import editpanel

actions = ['itemadd', 'itemedit', 'itemdelete']

ADDCODE = 0
EDITCODE = 1
DELETECODE = 2

#----------------------------------------------------------------------------

def getNextImageID(count):
    imID = 0
    while True:
        yield imID
        imID += 1
        if imID == count:
            imID = 0
    
    
class ItemsToolbook(wx.Toolbook):
    def __init__(self, parent, id, samdb):
        wx.Toolbook.__init__(self, parent, id, style=wx.BK_TOP)
        
        self.samdb = samdb
        
        il = wx.ImageList(201, 51, True)        
        for action in actions:
            bmp = wx.Bitmap('../otherfiles/images/' + action + '.bmp')
            il.Add(bmp)
        self.AssignImageList(il)
        imageIdGenerator = getNextImageID(il.GetImageCount())
        
        self.addPanel = addpanel.AddPanel(self, self.samdb, 'Item')
        self.AddPage(self.addPanel, "", imageId=imageIdGenerator.next())
        
        self.editPanel = editpanel.EditPanel(self, self.samdb, 'Item')
        self.AddPage(self.editPanel, '', imageId=imageIdGenerator.next())
        
        self.deletePanel = DeletePanel.DeletePanel(self, self.samdb, 'Item')
        self.AddPage(self.deletePanel, '', imageId = imageIdGenerator.next())
        
        self.Bind(wx.EVT_TOOLBOOK_PAGE_CHANGED, self.OnPageChanged)
        self.Bind(wx.EVT_TOOLBOOK_PAGE_CHANGING, self.OnPageChanging)
    
    def OnPageChanged(self, event):
        event.Skip()

    def OnPageChanging(self, event):
        ## 0 ==> Add Item; 1 ==> Edit Item; 2 ==> Delete Item
        new = event.GetSelection()
        if new == DELETECODE:
            self.deletePanel.deleteForm.BuildChooser(self.samdb)
        if new == EDITCODE:
            self.editPanel.buildItemChooser(self.samdb)
            self.editPanel.entryForm.ClearAll()
        event.Skip()
