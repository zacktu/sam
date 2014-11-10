##
## Adapted with minimal changes from Tian Xie as shown below.  The principal
## is that this program assumed that the frame code was in this module, and
## my frame code is in a different module.
##
#----------------------------------------------------------------------#
# This is a minimal wxPython program to show a SplashScreen widget.
#
# Tian Xie
# 3/8/2005
#
# http://wiki.wxpython.org/SplashScreen
#
#----------------------------------------------------------------------#

import wx
import maneframe

IMAGEFILEPATH = '/home/bob/src/workspace/SilentAuctionManager/otherfiles/SAMsplash.jpg'

class MySplashScreen(wx.SplashScreen):
    """
    Create a splash screen widget.
    """
    def __init__(self, parent=None):
        # This is a recipe to a the screen.
        # Modify the following variables as necessary.
        aBitmap = wx.Image(name=IMAGEFILEPATH).ConvertToBitmap()
        splashStyle = wx.SPLASH_CENTRE_ON_SCREEN | wx.SPLASH_TIMEOUT
        splashDuration = 2000 # milliseconds
        # Call the constructor with the above arguments in exactly the
        # following order.
        wx.SplashScreen.__init__(self, aBitmap, splashStyle,
                                 splashDuration, parent)
        self.Bind(wx.EVT_CLOSE, self.OnExitSplash)
        wx.Yield()
#----------------------------------------------------------------------#

    def OnExitSplash(self, evt):
        self.Hide()
        MyFrame = maneframe.ManeFrame()
        app.SetTopWindow(MyFrame)
        MyFrame.Show(True)
        # The program will freeze without this line.
        evt.Skip()  # Make sure the default handler runs too...
#----------------------------------------------------------------------#

class MyApp(wx.App):
    def OnInit(self):
        MySplash = MySplashScreen()
        MySplash.Show()

        return True
#----------------------------------------------------------------------#

#app = MyApp(redirect=True, filename = "demo.log")
app = MyApp()
app.MainLoop()

