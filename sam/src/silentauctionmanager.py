##
## Bob Cannon -- 15 October 2014
##
# Adapted with minimal changes from Tian Xie as shown below.  The principal
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
import sys

SPLASHFILEPATH = '../otherfiles/images/SAMsplash.jpg'

class MySplashScreen(wx.SplashScreen):
    """
    Create a splash screen widget.
    """
    def __init__(self, parent=None):
        # This is a recipe to a the screen.
        # sys.path.append("/opt/sam/src")
        # print ('SYS.PATH = ', sys.path)
        # Modify the following variables as necessary.
        aBitmap = wx.Image(name=SPLASHFILEPATH).ConvertToBitmap()
        splashStyle = wx.SPLASH_CENTRE_ON_SCREEN | wx.SPLASH_TIMEOUT
        splashDuration = 2000 # milliseconds
        # Call the constructor with the above arguments in exactly the
        # following order.
        wx.SplashScreen.__init__(self, aBitmap, splashStyle,
                                 splashDuration, parent)
        self.Bind(wx.EVT_CLOSE, self.onExitSplash)
        wx.Yield()
#----------------------------------------------------------------------#

    def onExitSplash(self, evt):
        self.Hide()
        MyFrame = maneframe.ManeFrame()
        app.SetTopWindow(MyFrame)
        MyFrame.Show(True)
        # The program will freeze without this line.
        evt.Skip()  # Make sure the default handler runs too...
#----------------------------------------------------------------------#

class myApp(wx.App):
    def OnInit(self):
        MySplash = MySplashScreen()
        MySplash.Show()

        return True
#----------------------------------------------------------------------#

#app = myApp(redirect=True, filename = "demo.log")
app = myApp()
app.MainLoop()
