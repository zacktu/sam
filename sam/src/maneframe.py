
import wx
import MySQLdb
import dbservices
import connectdialog
import manetoolbook
import dialogs

labels = "one two three four".split()

class ManeFrame(wx.Frame):

    def __init__(self):
        wx.Frame.__init__(self, None, -1, 
                          title = "SAM: the Silent Auction Manager",
                          size = (700, 450))
        #self.manePanel = pnl = wx.Panel(self)

        self.CreateStatusBar()

        fileMenu = wx.Menu()
        exitItem = fileMenu.Append(-1, "Exit the program")
        self.Bind(wx.EVT_MENU, self.onExit, exitItem)

        aboutMenu = wx.Menu()
        aboutItem = aboutMenu.Append(-1, "About SAM")
        self.Bind(wx.EVT_MENU, self.OnAboutDialog, aboutItem)

        menuBar = wx.MenuBar()
        menuBar.Append(fileMenu, "File")
        menuBar.Append(aboutMenu, "About")
        self.SetMenuBar(menuBar)

        # Connect to the database
        connected = False
        while not connected:
            dlg = connectdialog.ConnectDialog()
            result = dlg.ShowModal()
            dlg.Destroy()
            if result == wx.ID_OK:
                try:
                    profile = dlg.getProfile()
                    samdb = dbservices.Samdb(dbname = profile['dbname'], \
                                        hostname = profile["host"], \
                                        portnumber = int(profile['port']), \
                                        username = profile["user"], \
                                        password = profile["passwd"])
                    connected = True
                    manetoolbook.manetoolbook(self, -1, samdb)
                except MySQLdb.Error, e:
                    connected = False
                    dialogs.displayErrorDialog("Error %d: %s" % (e.args[0], \
                                                                 e.args[1]))
                    if not dialogs.displayYesNoDialog("Want to try again?"):
                        exit()    
            else:
                exit()
        
    def onExit(self, event):
        self.Close()
        
    def OnAboutDialog(self, event):
        from about import MyAboutDialog
        about = MyAboutDialog(self)
        about.ShowModal()
        about.Destroy()
        return

if __name__ == "__main__":
    app = wx.PySimpleApp()
    frame = ManeFrame()
    frame.Show()
    app.MainLoop()
