'''
Created on Aug 9, 2010

@author: bob
'''

import wx
import MySQLdb
import dialogs
import items
import console
import chooserlists

class ItemDeleteForm(wx.Panel):
    def __init__(self, parent, samdb):
        super(ItemDeleteForm, self).__init__(parent)
        
        self.samdb = samdb
        self.parent = parent
        self.items = items.Items()
        self.chooserLists = chooserlists.ChooserLists()
        self.con = console.Console()
        
        mainSizer = wx.BoxSizer(wx.VERTICAL)
        
        self.chooserPanel = wx.Panel(self, -1)
        self.BuildChooser(samdb)

        mainSizer.Add(self.chooserPanel)
        
        self.SetSizer(mainSizer)
        mainSizer.Fit(parent)
        mainSizer.SetSizeHints(parent)
           

    def OnItemNumberChoice(self, event):
        indexToDelete = event.GetSelection()
        itemNumber = event.GetString()
        if dialogs.displayYesNoDialog('Delete item number ' + \
                                      itemNumber + '?'):
            try:
                buyerNumber = self.items.checkItemHasBuyer \
                                (itemNumber, self.samdb)
                # If the item hasn't been purchased,
                # then the buyerNumber is None
                if buyerNumber is not None:
                    dialogs.displayErrorDialog \
                        ('This item has been purchased by ' \
                        + 'buyer number ' + buyerNumber + '.')
                    return
                else:
                    self.items.deleteItem(self.samdb, itemNumber)
                    self.itemNumberList.pop(indexToDelete)
                    self.itemNumberChoice.SetItems(self.itemNumberList)
                    indexToDelete = \
                        self.FindItemNumberInItemDescriptionList(itemNumber)
                    self.itemDescriptionList.pop(indexToDelete)
                    self.itemDescriptionChoice.SetItems \
                                (self.itemDescriptionList)
                    self.con.displayItems(self.samdb)
                    return
            except MySQLdb.Error, e:
                dialogs.displayErrorDialog(e.args[1])
                return
            except MySQLdb.Warning, e:
                print("Warning ", e)
        else:
            return
        
    def OnItemDescriptionChoice(self, event):
        indexToDelete = event.GetSelection()
        itemString = event.GetString()
        itemNumber = itemString[:3]
        if dialogs.displayYesNoDialog('Delete item number ' + \
                                      itemNumber + '?'):
            # Positive buyer number implies that item has been purchased
            buyerNumber = self.items.checkItemHasBuyer \
                            (itemNumber, self.samdb)
            if buyerNumber is not None:
                dialogs.displayErrorDialog \
                    ('This item has been purchased by ' \
                    + 'buyer number ' + buyerNumber + '.')
                return
            else:
                self.items.deleteItem(self.samdb, itemNumber)
                self.itemDescriptionList.pop(indexToDelete)
                self.itemDescriptionChoice.SetItems(self.itemDescriptionList)
                self.itemNumberList.remove(itemNumber)
                self.itemNumberChoice.SetItems(self.itemNumberList)
                #self.itemNumberChoice.SetItems(self.itemNumberList)
                self.con.displayItems(self.samdb)
        else:
            return

    def BuildChooser(self, samdb):
        try:
            self.itemNumberList = self.chooserLists.buildChooserNumberList \
                                ('item', samdb)
            wx.StaticText(self.chooserPanel, -1, \
                                "Select an item number:", (15,5))
            self.itemNumberChoice = wx.Choice(self.chooserPanel, \
                                -1, (195, 0), \
                                wx.DefaultSize, self.itemNumberList, \
                                wx.CB_DROPDOWN | wx.CB_READONLY)
            self.Bind(wx.EVT_CHOICE, self.OnItemNumberChoice, \
                  self.itemNumberChoice)

            self.itemDescriptionList = \
                        self.chooserLists.buildChooserNumberAndInfoList \
                                ('item', samdb)
            wx.StaticText(self.chooserPanel, -1, \
                                "Select an item description:", (15,40))
            self.itemDescriptionChoice = \
                                wx.Choice(self.chooserPanel, -1, (195, 40), \
                                wx.DefaultSize, self.itemDescriptionList, \
                                wx.CB_DROPDOWN | wx.CB_READONLY)
            self.Bind(wx.EVT_CHOICE, self.OnItemDescriptionChoice, \
                  self.itemDescriptionChoice)
        except MySQLdb.Error, e:
            dialogs.displayErrorDialog(e.args[1])
            return
        except MySQLdb.Warning, e:
            print("Warning ", e)       

    def FindItemNumberInItemDescriptionList(self, itemNumber):
        indexToDelete = 0
        for row in self.itemDescriptionList:
            if itemNumber == row[:3]:
                return indexToDelete
                self.itemDescriptionList.pop(indexToDelete)
                return
            else:
                indexToDelete += 1
        print "DeleteItemPanel: Couldn't find matching item number ''\
              + 'for item description.  This is bad."
        exit()

        