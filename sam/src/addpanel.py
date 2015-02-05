'''
Created on Aug 9, 2010
A panel for 
@author: bob
'''

import wx
import buyerentryform
import donorentryform
import itementryform
import PurchaseEntryForm

class AddPanel(wx.Panel):
    def __init__(self, parent, samdb, player):
        super(AddPanel, self).__init__(parent)

        self.samdb = samdb
        
        # First create the controls
        topLbl = wx.StaticText(self, -1, "Add " + player)
        topLbl.SetFont(wx.Font(18, wx.SWISS, wx.NORMAL, wx.BOLD))

        # mainSizer is the top-level one that manages everything
        mainSizer = wx.BoxSizer(wx.VERTICAL)
        mainSizer.Add(topLbl, 0, wx.ALL, 5)
        mainSizer.Add(wx.StaticLine(self), 0, wx.EXPAND|wx.TOP|wx.BOTTOM, 5)

        if player == 'Donor':
            self.entryForm = donorentryform.DonorEntryForm \
                        (self, samdb, 'add')
        elif player == 'Item':
            self.entryForm = itementryform.itementryform(self, samdb, 'add')
        elif player == 'Buyer':
            self.entryForm = buyerentryform.buyerentryform  \
                        (self, samdb, 'add')
        elif player == 'Purchase':
            self.entryForm = PurchaseEntryForm.PurchaseEntryForm \
                        (self, samdb, 'add')            
        else:
            'ADDPANEL GOT INVALID PLAYER = ', player
            exit()
            
        mainSizer.Add(self.entryForm)
        
        self.SetSizer(mainSizer)

        # Fit the frame to the needs of the sizer.  The frame will
        # automatically resize the panel as needed.  Also prevent the
        # frame from getting smaller than this size.
        mainSizer.Fit(parent)
        mainSizer.SetSizeHints(parent)
