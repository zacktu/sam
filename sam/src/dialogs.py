'''
Created on Aug 1, 2009

@author: Bob Cannon, bob@nean.net
'''

import wx


def displayErrorDialog(message):
    dlg = wx.MessageDialog(None, message, 'Error', wx.OK | wx.ICON_ERROR)
    dlg.ShowModal()
    
def displayInfoDialog(message):
    dlg = wx.MessageDialog(None, message, '', wx.OK | wx.ICON_INFORMATION)
    dlg.ShowModal()
    
def displayYesNoDialog(message):
    dlg = wx.MessageDialog(None, message, 'Is this action OK?', \
                            wx.YES_NO | wx.ICON_QUESTION)
    result = dlg.ShowModal()
    if result == wx.ID_YES:
        return True
    else:
        return False