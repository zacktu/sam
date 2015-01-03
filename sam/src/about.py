##
## about.py
## Bob Cannon
## 30 October 2014
## This file is still an old About file that I copied from
## elsewhere.  I need to do my own graphics and content.

import sys

import wx            # This module uses the new wx namespace
import wx.html
import wx.lib.wxpTag

#---------------------------------------------------------------------------

class MyAboutDialog(wx.Dialog):
    text = '''
<html>
<body bgcolor="#AC76DE">
    <center>
    </br>
    <p>
        <b>Silent Auction Manager</b> is an application that assists
        in setting up and managing a silent auction.
    </p>

    <p>
        <b>Donors</b> have contributed <b>Items</b>
        to the auction.  <b>Buyers</b> bid on
        and purchase them.
    </p>

    <p>
        The author of the program is Bob Cannon.
        Copyright (c) 2010-2014.
    </p>

    <p>
        <font size="-1">Please see <i>license.txt</i> for licensing information.</font>
    </p>

    <p>
        <wxp module="wx" class="Button">
            <param name="label" value="Okay">
            <param name="id"    value="ID_OK">
        </wxp>
    </p>
    </center>
</body>
</html>
'''
    # TODO: Replace this with your own code -- example from Mouse vs. Python
    def __init__(self, parent):
        wx.Dialog.__init__(self, parent, -1,
                           'Beginning to adapt the wxPython demo',)
        html = wx.html.HtmlWindow(self, -1, size=(420, -1))
        if "gtk2" in wx.PlatformInfo:
            html.SetStandardFonts()
        py_version = sys.version.split()[0]
        '''
        txt = self.text % (wx.VERSION_STRING,
                           ", ".join(wx.PlatformInfo[1:]),
                           py_version
                           )
        html.SetPage(txt)
        '''
        html.SetPage(self.text)
        btn = html.FindWindowById(wx.ID_OK)
        ir = html.GetInternalRepresentation()
        html.SetSize( (ir.GetWidth()+25, ir.GetHeight()+25) )
        self.SetClientSize(html.GetSize())
        self.CentreOnParent(wx.BOTH)

#---------------------------------------------------------------------------



if __name__ == '__main__':
    app = wx.PySimpleApp()
    dlg = MyAboutDialog(None)
    dlg.ShowModal()
    dlg.Destroy()
    app.MainLoop()
