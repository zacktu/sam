'''

SetUpAuction -- a program to set up a silent auction 

Data collected
    hostname and port number
    username and password
    database name
    title, subtitle, and date of auction -- used for invoice and receipt
    
Created on 15 August 2011

Author Bob Cannon

'''

import os
import createauction
import dialogs
import profileservices
import sys
import wx

ID_EXIT = 98
ID_OK = 99

class SetUpAuction(wx.Frame):
    
    def __init__(self):
        wx.Frame.__init__(self, None, wx.ID_ANY, title = 'Set Up Auction')
        self.panel = wx.Panel(self, wx.ID_ANY)
        font = wx.Font(12, wx.SWISS, wx.NORMAL, wx.BOLD)
        title = wx.StaticText(self.panel, wx.ID_ANY, 'Set up Auction')
        title.SetFont(font)
        
        titleSizer = wx.BoxSizer(wx.HORIZONTAL)
        titleSizer.Add(title, 0, wx.ALL, 5)
        
        ## Widgets for 1st row
        hostNameLabel = wx.StaticText(self.panel, -1, 'Host name')
        self.hostNameTC = wx.TextCtrl(self.panel, -1, '')
        portNumberLabel = wx.StaticText(self.panel, -1, 'Port number')
        self.portNumberTC = wx.TextCtrl(self.panel, -1, '3306')        
        ## Widgets for 2nd row
        userNameLabel = wx.StaticText(self.panel, -1, 'User name')
        self.userNameTC = wx.TextCtrl(self.panel, -1, '')
        passwordLabel = wx.StaticText(self.panel, -1, 'Password')
        self.passwordTC = wx.TextCtrl(self.panel, -1, '')
        
        ## Widgets for 3rd row
        dbNameLabel = wx.StaticText(self.panel, -1, 'Database name')
        self.dbNameTC = wx.TextCtrl(self.panel, -1, '')
        
        # Widgets for the 4th row
        titleLabel = wx.StaticText(self.panel, -1, 'Auction title')
        self.titleTC = wx.TextCtrl(self.panel, -1, '')
        
        # Widgets for the 5th row
        subtitleLabel = wx.StaticText(self.panel, -1, 'Auction subtitle')
        self.subtitleTC = wx.TextCtrl(self.panel, -1, '')
        
        # Widgets for the 6th row
        dateLabel = wx.StaticText(self.panel, -1, 'Auction date')
        self.dateTC = wx.TextCtrl(self.panel, -1, '')
        
        exitButton = wx.Button(self.panel, ID_EXIT, 'Exit')
        self.Bind(wx.EVT_BUTTON, self.OnExitButton, id=ID_EXIT)
        
        okayButton = wx.Button(self.panel, ID_OK, 'OK')
        self.Bind(wx.EVT_BUTTON, self.OnOKButton, id=ID_OK)
        okayButton.SetDefault()
        
        # Now create the sizer for all the data entry widgets
        selectionSizer = wx.GridBagSizer(hgap=5, vgap=5)
        selectionSizer.AddGrowableCol(1)
        selectionSizer.AddGrowableCol(3)
        
        # First row of selectionSizer
        row = 0
        selectionSizer.Add(hostNameLabel, pos=(row, 0), \
            flag=wx.ALL | wx.ALIGN_RIGHT, border=5)
        selectionSizer.Add(self.hostNameTC, pos=(row, 1), \
            flag=wx.ALL | wx.LEFT | wx.EXPAND, border=5)
        selectionSizer.Add(portNumberLabel, pos=(row, 2), \
            flag=wx.ALL | wx.ALIGN_RIGHT, border=5)
        selectionSizer.Add(self.portNumberTC, pos=(row, 3), \
            flag=wx.ALL | wx.LEFT | wx.EXPAND, border=5)

        
        # Second row of selectionSizer
        row += 1
        selectionSizer.Add(userNameLabel, pos=(row, 0), \
            flag=wx.ALL | wx.ALIGN_RIGHT, border=5)
        selectionSizer.Add(self.userNameTC, pos=(row, 1), \
            flag=wx.ALL | wx.LEFT | wx.EXPAND, border=5)
        selectionSizer.Add(passwordLabel, pos=(row, 2), \
            flag=wx.ALL | wx.ALIGN_RIGHT, border=5)
        selectionSizer.Add(self.passwordTC, pos=(row, 3), \
            flag=wx.ALL | wx.LEFT | wx.EXPAND, border=5)

        # Third row of selectionSizer
        row += 1
        selectionSizer.Add(dbNameLabel, pos=(row, 0), \
            flag=wx.ALL | wx.ALIGN_RIGHT, border=5)
        selectionSizer.Add(self.dbNameTC, pos=(row, 1), \
            flag=wx.ALL | wx.LEFT | wx.EXPAND, border=5)
        
        # Fourth row of selectionSizer
        row += 1
        selectionSizer.Add(titleLabel, pos=(row, 0), \
            flag=wx.ALL | wx.ALIGN_RIGHT, border=5)
        selectionSizer.Add(self.titleTC, pos=(row, 1), span=(1,4), \
            flag=wx.ALL | wx.LEFT | wx.EXPAND, border=5)
        
        # Fifth row of selectionSizer
        row += 1
        selectionSizer.Add(subtitleLabel, pos=(row, 0), \
            flag=wx.ALL | wx.ALIGN_RIGHT, border=5)
        selectionSizer.Add(self.subtitleTC, pos=(row, 1), span=(1,4), \
            flag=wx.ALL | wx.LEFT | wx.EXPAND, border=5)
        
        # Sixth row of selectionSizer
        row += 1
        selectionSizer.Add(dateLabel, pos=(row, 0), \
            flag=wx.ALL | wx.ALIGN_RIGHT, border=5)
        selectionSizer.Add(self.dateTC, pos=(row, 1), \
            flag=wx.ALL | wx.LEFT | wx.EXPAND, border=5)
        
        # And now a sizer for the exit and OK buttons
        buttonSizer = wx.BoxSizer(wx.HORIZONTAL)
        buttonSizer.Add((0,0), 1)
        buttonSizer.Add(exitButton, 0, wx.ALL, 5)
        buttonSizer.Add(okayButton, 0, wx.ALL, 5)
        
        ## Define a BoxSizer and assemble all the sizers in it
        mainSizer = wx.BoxSizer(wx.VERTICAL)
        mainSizer.Add(titleSizer, 0, wx.CENTER)
        mainSizer.Add(wx.StaticLine(self.panel), 0, wx.ALL | wx.EXPAND, 5)
        mainSizer.Add(selectionSizer, 0, wx.ALL | wx.EXPAND, 5)
        mainSizer.Add(buttonSizer, 0, wx.ALL| wx.EXPAND, 5)

        # Place mainSizer into the panel and you're finished
        self.panel.SetSizer(mainSizer)
        #self.SetSizeHints(250, 200, 800, 500)
        self.SetSizeHints(500, 200, 800, 500)
        mainSizer.Fit(self)
        
    def OnOKButton(self, event):
        
        hostName = self.hostNameTC.GetValue()
        if not (len(hostName) > 0):
            dialogs.displayErrorDialog("The host name must not be null.")
            return
        
        portNumber = self.portNumberTC.GetValue()
        
        userName = self.userNameTC.GetValue()
        if not (len(userName) > 0):
            dialogs.displayErrorDialog("The user name must not be null.")
            return
        
        password = self.passwordTC.GetValue()
        
        dbName = self.dbNameTC.GetValue()
        if not (len(dbName) > 0):
            dialogs.displayErrorDialog("The database name must not be null.")
            return
        
        title = self.titleTC.GetValue()
        
        subtitle = self.subtitleTC.GetValue()
        
        date = self.dateTC.GetValue()
        
        print hostName, portNumber, userName, password, dbName, \
              title, subtitle, date
        createauction.createAuction(hostName, portNumber, userName, password, \
                                    dbName, title, subtitle, date)
        dialogs.displayInfoDialog("The auction was created successfully.")

        # Now write the profile to the user's directory
        profileservices.createProfile(dbName, hostName, portNumber,
                        userName, password, title, subtitle, date)
        sys.exit()

    def OnExitButton(self, event):
        if dialogs.displayYesNoDialog('Are you sure you want to exit?'):
            sys.exit()
        else:
            okayButton.SetDefault()
            return
        
## Run the program
if __name__ == '__main__':
    app = wx.PySimpleApp()
    frame = SetUpAuction()
    frame.Centre()
    frame.Show()
    app.MainLoop()
        