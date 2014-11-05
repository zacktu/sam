'''
Dialog to get user information for connecting to the mysql server and to
the SAMDB database.  At the moment it defaults to bob@localhost with a null
password.  This is adapted from validator2.py from chapter 9 of Rappin.  
'''

import wx

about_txt = """\
Enter the hostname, username, and user
password for connecting to SAMDB."""


class DataXferValidator(wx.PyValidator):
    def __init__(self, data, key):
        wx.PyValidator.__init__(self)
        self.data = data
        self.key = key

    def Clone(self):
        """
        Note that every validator must implement the Clone() method.
        """
        return DataXferValidator(self.data, self.key)

    def Validate(self, win):
        return True

    def TransferToWindow(self):
        textCtrl = self.GetWindow()
        textCtrl.SetValue(self.data.get(self.key, ""))
        return True 

    def TransferFromWindow(self):
        textCtrl = self.GetWindow()
        self.data[self.key] = textCtrl.GetValue()
        return True

class ConnectDialog(wx.Dialog):
    #def __init__(self, data):
    def __init__(self, data):
        wx.Dialog.__init__(self, None, -1, "Connect to SAMDB")

        # Create the text controls
        about = wx.StaticText(self, -1, about_txt)
        host_l = wx.StaticText(self, -1, "Host:")
        port_l = wx.StaticText(self, -1, "Port:")
        user_l = wx.StaticText(self, -1, "User:")
        passwd_l = wx.StaticText(self, -1, "Password:")
        dbname_l = wx.StaticText(self, -1, 'Database Name:')
        
        data["host"] = "localhost"
        data['port'] = '3306'
        data["user"] = "bob"
        data["passwd"] = 'bobspw'
        data['dbname'] = 'test01'
        host_t  = wx.TextCtrl(self, validator=DataXferValidator(data, "host"))
        port_t  = wx.TextCtrl(self, validator=DataXferValidator(data, "port"))
        user_t = wx.TextCtrl(self, validator=DataXferValidator(data, "user"))
        passwd_t = wx.TextCtrl(self, style=wx.TE_PASSWORD, \
                               validator=DataXferValidator(data, "passwd"))
        dbname_t = wx.TextCtrl(self, \
                               validator=DataXferValidator(data, "dbname"))

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
        

if __name__ == '__main__':
    app = wx.PySimpleApp()

    data = { "host" : "localhost" , "port" : '3306', "user" : "bob" , \
                "passwd" : '', 'dbname' : 'SAMDB'}
    dlg = ConnectDialog(data)
    dlg.ShowModal()
    dlg.Destroy()

    print "HOST IS ", data["host"]
    print "USER IS", data['user']
    print 'PORT IS', data['port']
    print "PASSWORD IS ", data['passwd']
    print 'DATABASE NAME IS ', data['dbname']

    app.MainLoop()