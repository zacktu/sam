'''
Created on Aug 9, 2010
A panel for 
@author: bob
'''


import wx
import PrintBuyerCartOrReceiptForm

class PrintOneCartOrReceiptPanel(wx.Panel):
    def __init__(self, parent, samdb, whatToPrint):
        super(PrintOneCartOrReceiptPanel, self).__init__(parent)

        #self.samdb = samdb
        
        # First create the controls
        if whatToPrint == 'carts':
            topLbl = wx.StaticText(self, -1, "Print One Cart")
        else:
            topLbl = wx.StaticText(self, -1, "Print One Receipt")
        topLbl.SetFont(wx.Font(18, wx.SWISS, wx.NORMAL, wx.BOLD))

        # mainSizer is the top-level one that manages everything
        mainSizer = wx.BoxSizer(wx.VERTICAL)
        mainSizer.Add(topLbl, 0, wx.ALL, 5)
        mainSizer.Add(wx.StaticLine(self), 0, wx.EXPAND|wx.TOP|wx.BOTTOM, 5)

        self.pbcorf = PrintBuyerCartOrReceiptForm.PrintBuyerCartOrReceiptForm(
            self, samdb, whatToPrint)

        mainSizer.Add(self.pbcorf)
        
        self.SetSizer(mainSizer)

        # Fit the frame to the needs of the sizer.  The frame will
        # automatically resize the panel as needed.  Also prevent the
        # frame from getting smaller than this size.
        mainSizer.Fit(parent)
        mainSizer.SetSizeHints(parent)

