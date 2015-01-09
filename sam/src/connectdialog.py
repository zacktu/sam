'''
Dialog to get user information for connecting to the mysql server and to
the Samdb database.  At the moment it defaults to bob@localhost with a null
password.  This is adapted from validator2.py from chapter 9 of Rappin.  
'''

import os
import sys
import wx
import dialogs
import profileservices

about_txt = """\
Enter the hostname, username, and user
password for connecting to Samdb."""


class DataXferValidator(wx.PyValidator):
    def __init__(self, data, key):
        wx.PyValidator.__init__(self)
        self.profile = data
        self.key = key

    def Clone(self):
        """
        Note that every validator must implement the Clone() method.
        """
        return DataXferValidator(self.profile, self.key)

    def Validate(self, win):
        return True

    def TransferToWindow(self):
        textCtrl = self.GetWindow()
        textCtrl.SetValue(self.profile.get(self.key, ""))
        return True 

    def TransferFromWindow(self):
        textCtrl = self.GetWindow()
        self.profile[self.key] = textCtrl.GetValue()
        return True

class ConnectDialog(wx.Dialog):

    def __init__(self):
        wx.Dialog.__init__(self, None, -1, "Connect to Samdb")

        # Create the text controls
        about = wx.StaticText(self, -1, about_txt)
        host_l = wx.StaticText(self, -1, "Host:")
        port_l = wx.StaticText(self, -1, "Port:")
        user_l = wx.StaticText(self, -1, "User:")
        passwd_l = wx.StaticText(self, -1, "Password:")
        dbname_l = wx.StaticText(self, -1, 'Database Name:')

        if len(sys.argv) == 2:
            self.profile = {
               'dbName': sys.argv[1],
               'hostName': 'localhost',
               'portNumber': '3306',
               'userName': 'bob',
               'password': 'bobspw'}
        elif len(sys.argv) == 6:
            self.profile = {
               'dbName': sys.argv[1],
               'hostName': sys.argv[2],
               'portNumber': sys.argv[3],
               'userName': sys.argv[4],
               'password': sys.argv[5]}
        elif len(sys.argv) == 1:
            self.profile = profileservices.getProfile()
        else:
            dialogs.displayErrorDialog(
                'Can''t get your profile.\nPlease see the auction manager')
            sys.exit()

        # So we have the profile.  Now show it and allow temporary changes.
        host_t  = wx.TextCtrl \
            (self, validator=DataXferValidator(self.profile, "hostName"))
        port_t  = wx.TextCtrl\
            (self, validator=DataXferValidator(self.profile, "portNumber"))
        user_t = wx.TextCtrl\
            (self, validator=DataXferValidator(self.profile, "userName"))
        passwd_t = wx.TextCtrl\
            (self, style=wx.TE_PASSWORD, \
             validator=DataXferValidator(self.profile, "password"))
        dbname_t = wx.TextCtrl\
            (self, validator=DataXferValidator(self.profile, "dbName"))

        # Use standard button IDs
        okayButton   = wx.Button(self, wx.ID_OK)
        okayButton.SetDefault()
        # I'm using "cancel" as "exit".
        exitButton = wx.Button(self, wx.ID_CANCEL, 'Exit')

        # Layout with sizers
        sizer = wx.BoxSizer(wx.VERTICAL)
        sizer.Add(about, 0, wx.ALL, 5)
        sizer.Add(wx.StaticLine(self), 0, wx.EXPAND|wx.ALL, 5)

        fgs = wx.FlexGridSizer(5, 2, 5, 5)
        fgs.Add(host_l, 0, wx.ALIGN_RIGHT)
        fgs.Add(host_t, 0, wx.EXPAND)
        fgs.Add(port_l, 0, wx.ALIGN_RIGHT)
        fgs.Add(port_t, 0, wx.EXPAND)
        fgs.Add(user_l, 0, wx.ALIGN_RIGHT)
        fgs.Add(user_t, 0, wx.EXPAND)
        fgs.Add(passwd_l, 0, wx.ALIGN_RIGHT)
        fgs.Add(passwd_t, 0, wx.EXPAND)
        fgs.Add(dbname_l, 0, wx.ALIGN_RIGHT)
        fgs.Add(dbname_t, 0, wx.EXPAND)
        fgs.AddGrowableCol(1)
        sizer.Add(fgs, 0, wx.EXPAND|wx.ALL, 5)

        btns = wx.StdDialogButtonSizer()
        btns.AddButton(okayButton)
        btns.AddButton(exitButton)
        btns.Realize()
        sizer.Add(btns, 0, wx.EXPAND|wx.ALL, 5)

        self.SetSizer(sizer)
        sizer.Fit(self)

    def getProfile(self):
        return self.profile

if __name__ == '__main__':
    app = wx.PySimpleApp()
    connectDialog = ConnectDialog()
    connectDialog.ShowModal()
    profile = profileservices.getProfile()
    connectDialog.Destroy()

    print "HOST IS ", profileservices["host"]
    print "USER IS", profileservices['user']
    print 'PORT IS', profileservices['port']
    print "PASSWORD IS ", profileservices['passwd']
    print 'DATABASE NAME IS ', profileservices['dbname']

    app.MainLoop()