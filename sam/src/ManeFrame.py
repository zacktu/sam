
import wx
import MySQLdb
import SAMDB
import ConnectDialog
import ManeToolbook
import Dialogs

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
        self.Bind(wx.EVT_MENU, self.OnExit, exitItem)

        aboutMenu = wx.Menu()
        aboutItem = aboutMenu.Append(-1, "About the program")
        self.Bind(wx.EVT_MENU, self.OnAboutDialog, aboutItem)

        menuBar = wx.MenuBar()
        menuBar.Append(fileMenu, "File")
        menuBar.Append(aboutMenu, "About")
        self.SetMenuBar(menuBar)

        # Connect to the database
        connected = False
        while not connected:
            data = {}
            dlg = ConnectDialog.ConnectDialog(data)
            result = dlg.ShowModal()
            dlg.Destroy()
            if result == wx.ID_OK:
                try:
                    samdb = SAMDB.SAMDB(dbname = data['dbname'], \
                                        hostname = data["host"], \
                                        portnumber = int(data['port']), \
                                        username = data["user"], \
                                        password = data["passwd"])
                    connected = True
                    ManeToolbook.ManeToolbook(self, -1, samdb)
                except MySQLdb.Error, e:
                    connected = False
                    Dialogs.DisplayErrorDialog("Error %d: %s" % (e.args[0], \
                                                                 e.args[1]))
                    if not Dialogs.DisplayYesNoDialog("Want to try again?"):
                        exit()    
            else:
                exit()
        
    def OnExit(self, event):
        self.Close()
        
    def OnAboutDialog(self, event):
        from About import MyAboutDialog
        about = MyAboutDialog(self)
        about.ShowModal()
        about.Destroy()
        return

if __name__ == "__main__":
    app = wx.PySimpleApp()
    frame = ManeFrame()
    frame.Show()
    app.MainLoop()
