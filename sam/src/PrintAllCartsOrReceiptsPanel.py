'''
Created on Aug 9, 2010
A panel for 
@author: bob
'''

import wx
import buyers
import console
import printingservices


class PrintAllCartsOrReceiptsPanel(wx.Panel):
    def __init__(self, parent, samdb, whatToPrint):
        super(PrintAllCartsOrReceiptsPanel, self).__init__(parent)

        self.samdb = samdb
        self.parent = parent
        self.con = console.Console()
        self.buyers = buyers.Buyers()
        self.whatToPrint = whatToPrint
        
        # First create the controls
        if whatToPrint == 'carts':
            topLbl = wx.StaticText(self, -1, "Print All Carts")
            message = 'Print all shopping carts.  ' \
                      'This is usually\ndone only by the Auction Manager.'
        else:
            topLbl = wx.StaticText(self, -1, "Print All Receipts")
            message = 'Print all receipts.  ' \
                      'This is usually\ndone only by the Auction Manager.'
        topLbl.SetFont(wx.Font(18, wx.SWISS, wx.NORMAL, wx.BOLD))

        # mainSizer is the top-level one that manages everything
        mainSizer = wx.BoxSizer(wx.VERTICAL)
        mainSizer.Add(topLbl, 0, wx.ALL, 5)
        mainSizer.Add(wx.StaticLine(self), 0, wx.EXPAND|wx.TOP|wx.BOTTOM, 5)
        
        buttonPanel = wx.Panel(self, -1)
        instructions = wx.StaticText(buttonPanel, -1, message, (15,5))
        instructions.SetFont(wx.Font(12, wx.SWISS, wx.NORMAL, \
                                     wx.NORMAL, False))
        
        previewButton = wx.Button(buttonPanel, -1, 'Preview', pos=(60,50))
        printButton = wx.Button(buttonPanel, -1, 'Print', pos=(200,50))
        self.Bind(wx.EVT_BUTTON, self.OnPreviewButton, previewButton)
        self.Bind(wx.EVT_BUTTON, self.OnPrintButton, printButton)
        previewButton.SetDefault()
        printButton.SetDefault()
        
        mainSizer.Add(buttonPanel)
        
        self.SetSizer(mainSizer)

        # Fit the frame to the needs of the sizer.  The frame will
        # automatically resize the panel as needed.  Also prevent the
        # frame from getting smaller than this size.
        mainSizer.Fit(parent)
        mainSizer.SetSizeHints(parent)
        
    def OnPreviewButton(self, event):
        self.con.displayAllPurchases(self.samdb)
        ps = printingservices.PrintingServices(self.parent, self.samdb)
        ps.previewAllCartsOrReceipts(self.whatToPrint)
        
    def OnPrintButton(self, event):
        self.con.displayAllPurchases(self.samdb)
        ps = printingservices.PrintingServices(self.parent, self.samdb)
        ps.printAllCartsOrReceipts(self.whatToprint)
        




