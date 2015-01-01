
import wx
import random
import printingservices

APP_SIZE_X = 400
APP_SIZE_Y = 150

''' This is a non-standard dialog because it gives three choices: Preview,
    Print, and Neither.  I started with a sample dialog program somewhere
    and eventually got this class.  I only use it in the two cases where
    the user has selected a buyer by either name or number.  Thus, there
    is an extra confirmation step before proceeding on to ask whether to
    print or preview.  It seems weird that there's not a standard dialog
    a little more complex than the Yes/No dialog. '''
    
class PrintOrPreviewDialog(wx.Dialog):
    def __init__(self, parent, id, title, query, buyerNum, samdb, whatToPrint):
        wx.Dialog.__init__(self, parent, id, title, \
                size=(APP_SIZE_X, APP_SIZE_Y))

        self.samdb = samdb
        self.parent = parent
        self.buyerNum = buyerNum
        self.whatToPrint = whatToPrint

        wx.StaticText(self, -1, query, (15, 25))
        wx.Button(self, 1, 'Preview', (50, 100))
        wx.Button(self, 2, 'Print', (150, 100))
        wx.Button(self, 3, 'Neither', (250, 100))
        #icon = wx.Icon('interest.ico', wx.BITMAP_TYPE_ICO)
        #self.SetIcon(icon)

        self.Bind(wx.EVT_BUTTON, self.OnPreview, id=1)
        self.Bind(wx.EVT_BUTTON, self.OnPrint, id=2)
        self.Bind(wx.EVT_BUTTON, self.OnClose, id=3)

        self.Centre()
        self.ShowModal()
        self.Destroy()

    def OnPreview(self, event):
        ps = printingservices.PrintingServices(self.samdb)
        ps.previewOneCartOrReceipt(self.buyerNum, self.whatToPrint)
        self.Close(True)

    def OnPrint(self, event):
        ps = printingservices.PrintingServices(self.samdb)
        ps.printOneCartOrReceipt(self.buyerNum, self.whatToPrint)
        self.Close(True)

    def OnClose(self, event):
        self.Close(True)


if __name__ == '__main__':
    app = wx.App(0)
    PrintOrPreviewDialog(None, -1, 'buttons.py')
    app.MainLoop()
