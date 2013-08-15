
import  wx
import AddPanel
import DeletePanel
import EditPanel

actions = ['donoradd', 'donoredit', 'donordelete']

ADDCODE = 0
EDITCODE = 1
DELETECODE = 2

#----------------------------------------------------------------------------
    
    
class DonorsToolbook(wx.Toolbook):
    def __init__(self, parent, id, samdb):
        wx.Toolbook.__init__(self, parent, id, style=wx.BK_TOP)
        
        self.samdb = samdb
        
        il = wx.ImageList(201, 51, True)        
        for action in actions:
            bmp = wx.Bitmap('../otherfiles/images/' + action + '.bmp')
            il.Add(bmp)
        self.AssignImageList(il)
        imageIdGenerator = GetNextImageID(il.GetImageCount())
        
        #self.dap = DonorAddPanel.DonorAddPanel(self, self.samdb)
        self.addPanel = AddPanel.AddPanel(self, self.samdb, 'Donor')
        self.AddPage(self.addPanel, "", imageId=imageIdGenerator.next())
        
        self.editPanel = EditPanel.EditPanel(self, self.samdb, 'Donor')
        self.AddPage(self.editPanel, '', imageId=imageIdGenerator.next())
        
        self.deletePanel = DeletePanel.DeletePanel(self, self.samdb, 'Donor')
        self.AddPage(self.deletePanel, '', imageId = imageIdGenerator.next())
        
        self.Bind(wx.EVT_TOOLBOOK_PAGE_CHANGED, self.OnPageChanged)
        self.Bind(wx.EVT_TOOLBOOK_PAGE_CHANGING, self.OnPageChanging)
    
    def OnPageChanged(self, event):
        event.Skip()

    def OnPageChanging(self, event):
        ## 0 ==> Add Donor; 1 ==> Edit Donor; 2 ==> Delete Donor
        new = event.GetSelection()
        if new == DELETECODE:
            self.deletePanel.deleteForm.BuildChooser(self.samdb)
        if new == EDITCODE:
            self.editPanel.BuildDonorChooser(self.samdb)
            self.editPanel.entryForm.ClearAll()
        event.Skip()
        

def GetNextImageID(count):
    imID = 0
    while True:
        yield imID
        imID += 1
        if imID == count:
            imID = 0
