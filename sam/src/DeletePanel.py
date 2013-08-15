'''
Created on Aug 9, 2010
A panel for 
@author: bob
'''

### This is almost just a placeholder.  I plan for it to do a lot more.

import wx
import BuyerDeleteForm
import DonorDeleteForm
import ItemDeleteForm
import PurchaseDeleteForm

class DeletePanel(wx.Panel):
    def __init__(self, parent, samdb, player):
        super(DeletePanel, self).__init__(parent)

        self.samdb = samdb
        
        # First create the controls
        topLbl = wx.StaticText(self, -1, "Delete " + player)
        topLbl.SetFont(wx.Font(18, wx.SWISS, wx.NORMAL, wx.BOLD))

        # mainSizer is the top-level one that manages everything
        mainSizer = wx.BoxSizer(wx.VERTICAL)
        mainSizer.Add(topLbl, 0, wx.ALL, 5)
        mainSizer.Add(wx.StaticLine(self), 0, wx.EXPAND|wx.TOP|wx.BOTTOM, 5)

        if player == 'Donor':
            self.deleteForm = DonorDeleteForm.DonorDeleteForm(self, samdb)
        elif player == 'Item':
            self.deleteForm = ItemDeleteForm.ItemDeleteForm(self, samdb)
        elif player == 'Buyer':
            self.deleteForm = BuyerDeleteForm.BuyerDeleteForm(self, samdb)
        elif player == 'Purchase':
            self.deleteForm = PurchaseDeleteForm.PurchaseDeleteForm(self,samdb)
  
        mainSizer.Add(self.deleteForm)
        
        self.SetSizer(mainSizer)

        # Fit the frame to the needs of the sizer.  The frame will
        # automatically resize the panel as needed.  Also prevent the
        # frame from getting smaller than this size.
        mainSizer.Fit(parent)
        mainSizer.SetSizeHints(parent)
