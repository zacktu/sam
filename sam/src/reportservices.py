'''
Created on Jan 1, 2015

@author: bob

Construct various troff reports to be printed by the Silent Auction Manager.
The separate lines required by troff are built here.  The header lines are
taken from the Auction table.  Information about purchases, etc., is taken
from the Buyers table.

'''

import os
import sys
import wx
import MySQLdb
import subprocess
from random import sample
from string import digits, ascii_uppercase, ascii_lowercase
import csv
from tempfile import gettempdir
import dbservices
import printingservices
import profileservices
import buyers
import auction
import donors
import items
import dialogs
import cups

class ReportServices():

    def __init__(self, samdb):
    #def __init__(self, parent, samdb):
        #self.parent = parent
        self.samdb = samdb
        self.auction = auction.Auction()
        self.buyers = buyers.Buyers()
        self.donors = donors.Donors()
        self.items = items.Items()
        self.prs = printingservices.PrintingServices(samdb)

    def buildReportHeader(self, whatToPrint):
        lines = []
        lines.append('.nr LL 9i\n')
        lines.append('.pl 8.5i\n')
        lines.append('.ds CH\n')
        #lines.append('.ds CH -\\n[PN]\n') If you want page number in footer
        lines.append('.sp 0.5i\n')
        lines.append('.ft B\n')
        lines.append('.TS\n')
        lines.append('center, expand;\n')
        lines.append('c.\n')
        try:
            lines.append(self.auction.getAuctionTitle(self.samdb) + '\n')
            lines.append(self.auction.getAuctionSubtitle(self.samdb) + '\n')
            lines.append(self.auction.getAuctionDate(self.samdb) + '\n')
            if whatToPrint == 'donors':
                lines.append('\nDonors Report\n\n')
            elif whatToPrint == 'buyers':
                lines.append('\nBuyers Report\n\n')
            elif whatToPrint == 'items':
                lines.append('\nItems Report\n\n')
        except MySQLdb.Error, e:
            print "PrintingServices.buildReportHeader: Error %d: %s" \
                    % (e.args[0], e.args[1])
            sys.exit (1)
        except MySQLdb.Warning, e:
            print("ReportServices.buildReportHeader: Warning: ", e)
        lines.append('.TE\n')
        lines.append('.ft R\n')
        lines.append('.br\n')
        return lines

    def printOrPreviewDonorReport(self, samdb, printOrPreview):
        fname = self.prs.rand_fname('xxx', 8)
        lines = self.buildDonorReport(samdb)
        #lines.insert(0, '.ll 9i\n')
        if (printOrPreview == 'print'):
            self.prs.writeFile(fname, lines)
            self.prs.printLandscape(fname)
        elif (printOrPreview == 'preview'):
            self.prs.writeFile(fname, lines)
            self.prs.previewLandscape(fname)
        else:
            print('printingservices.printOrPreviewDonorReport: '
                  + 'invalid parameter '
                  + 'printOrPreview = ' + printOrPreview)
            print('Bugout!')
            sys.exit()

    def printOrPreviewBuyerReport(self, samdb, printOrPreview):
        fname = self.prs.rand_fname('xxx', 8)
        lines = self.buildBuyerReport(samdb)
        #landscape lines are 9i wide
        lines.insert(0, '.ll 9i\n')
        if (printOrPreview == 'print'):
            self.prs.writeFile(fname, lines)
            self.prs.printLandscape(fname)
        elif (printOrPreview == 'preview'):
            self.prs.writeFile(fname, lines)
            self.prs.previewLandscape(fname)
        else:
            print('printingservices.printOrPreviewBuyerReport: '
                  + 'invalid parameter '
                  + 'printOrPreview = ' + printOrPreview)
            print('Bugout!')
            sys.exit()

    def printOrPreviewItemReport(self, samdb, printOrPreview):
        fname = self.prs.rand_fname('xxx', 8)
        lines = self.buildItemReport(samdb)
        #landscape lines are 9i wide
        lines.insert(0, '.ll 9i\n')
        if (printOrPreview == 'print'):
            self.prs.writeFile(fname, lines)
            self.prs.printLandscape(fname)
        elif (printOrPreview == 'preview'):
            self.prs.writeFile(fname, lines)
            self.prs.previewLandscape(fname)
        else:
            print('printingservices.printOrPreviewItemReport: '
                  + 'invalid parameter '
                  + 'printOrPreview = ' + printOrPreview)
            print('Bugout!')
            sys.exit()

    def buildDonorReport(self, samdb):
        lines = self.buildReportHeader('donors')
        lines.append('.ps -2\n')
        lines.append('.TS H\n')
        lines.append('box, expand, tab(`);\n')
        lines.append('cI cI cI cI cI cI cI.\n')
        lines.append('Donor`Name`Street`City`Contact`Telephone`Email\n')
        lines.append('_\n')
        lines.append('.TH\n')
        lines.append('.T&\n')
        lines.append('n l l l l c l.\n')
        allDonors = self.donors.getAllDonors(self.samdb)
        for donor in allDonors:
            donorInfo = self.donors.fetchDonor(self.samdb, donor[0])
            lines.append(donor[0] + '`' + donorInfo[0] + '`' + donorInfo[1]
                         + '`' + donorInfo[2] + '`' + donorInfo[3]
                         + '`' + donorInfo[4] + '`' + donorInfo[5] + '\n')
        lines.append('.TE\n')
        return lines

    def buildBuyerReport(self, samdb):
        lines = self.buildReportHeader('buyers')
        lines.append('.TS H\n')
        lines.append('box, expand, tab(`);\n')
        lines.append('cI cI cI cI cI cI.\n')
        lines.append('Buyer`Last`First`Street`City`Telephone\n')
        lines.append('_\n')
        lines.append('.TH\n')
        lines.append('.T&\n')
        lines.append('n l l l l c.\n')
        allBuyers = self.buyers.getAllBuyers(self.samdb)
        for buyer in allBuyers:
            buyerInfo = self.buyers.fetchBuyer(self.samdb, buyer[0])
            lines.append(buyer[0] + '`' + buyerInfo[0] + '`' + buyerInfo[1]
                         + '`' + buyerInfo[2] + '`' + buyerInfo[3] + '`'
                         + buyerInfo[4] + '\n')
        lines.append('.TE\n')
        return lines

    def buildItemReport(self, samdb):
        lines = self.buildReportHeader('items')
        lines.append('.TS H\n')
        lines.append('box, expand, tab(`);\n')
        lines.append('cI cI cI cI cI cI cI cI.\n')
        lines.append(
            'Item`Description`Donor`Retail`Min Bid`Increment`Buyer`Price\n')
        lines.append('_\n')
        lines.append('.TH\n')
        lines.append('.T&\n')
        lines.append('n l n n n n n n.\n')
        allItems = self.items.getAllItems(self.samdb)
        for item in allItems:
            itemInfo = self.items.fetchItem(self.samdb, item[0])
            lines.append(item[0] + '`' + itemInfo[0] + '`' + itemInfo[1] \
                           + '`' + str(itemInfo[2]) + '`' + str(itemInfo[3]) \
                           + '`' + str(itemInfo[4]) + '`' + str(itemInfo[5]) \
                           + '`' + str(itemInfo[6]) + '\n')
        lines.append('.TE\n')
        return lines

    def doCSV(self, samdb, whichTable):
        try:
            dialog = wx.FileDialog(None,
                                   message='Select the file location',
                                   defaultDir='/home/bob/Desktop/csv',
                                   defaultFile=whichTable,
                                   wildcard='.csv',
                                   style=wx.SAVE)
            if dialog.ShowModal() == wx.ID_OK:
                fname = dialog.GetPath() + '.csv'
            dialog.Destroy()
            csvFile = csv.writer(
                open(fname, "wb"))
        except IOError:
            dialogs.ErrorDialog('Unable to create the CSV file.')
            return
        columnHeaders = samdb.getColumnHeaders(whichTable)
        csvFile.writerow(columnHeaders)
        if whichTable == 'Buyers':
            allBuyers = self.buyers.getAllBuyers(self.samdb)
            for buyer in allBuyers:
                buyerRow = self.buyers.fetchBuyer(self.samdb, buyer[0])
                fullRow = list(buyerRow)
                fullRow.insert(0, buyer[0])
                csvFile.writerow(fullRow)
        elif whichTable == 'Donors':
            allDonors = self.donors.getAllDonors(self.samdb)
            for donor in allDonors:
                donorRow = self.donors.fetchDonor(self.samdb, donor[0])
                fullRow = list(donorRow)
                fullRow.insert(0, donor[0])
                csvFile.writerow(fullRow)
        elif whichTable == 'Items':
            allItems = self.items.getAllItems(self.samdb)
            for item in allItems:
                itemRow = self.items.fetchItem(self.samdb, item[0])
                fullRow = list(itemRow)
                fullRow.insert(0, item[0])
                csvFile.writerow(fullRow)

    def getPrinterModel(self):
        try:
            conn = cups.Connection ()
            defaultPrinter = conn.getDefault()
            printers = conn.getPrinters ()
            printerInfo = printers[defaultPrinter]['printer-info']
            # Should be something such as 'Brother 2270'
            return printerInfo[printerInfo.index(' ')+1:]
        except KeyError:
            errorMessage = \
                'Unable to access information about the default printer.\n' \
                + 'The program must exit.'
            dialogs.displayErrorDialog(errorMessage)
            sys.exit()

if __name__ == '__main__':
    app = wx.PySimpleApp()
    if not (len(sys.argv) == 3):
        print('Usage: reportservices.py action tablename')
        sys.exit()
    profile = profileservices.getProfile()
    samdb = dbservices.Samdb(profile['dbName'],
                             profile['hostName'],
                             int(profile['portNumber']),
                             profile['userName'],
                             profile['password'])
    printPreviewOrCSV = sys.argv[1]
    tableName = sys.argv[2]
    if ((not printPreviewOrCSV in ('preview', 'print', 'csv'))
            or (not tableName in ('Donors', 'Items', 'Buyers'))):
        print('Usage: reportservices.py action tablename')
    else:
        rs = ReportServices(samdb)
        if printPreviewOrCSV == 'csv':
            rs.doCSV(samdb, tableName)
        elif tableName == 'Buyers':
            rs.printOrPreviewBuyerReport(samdb, printPreviewOrCSV)
        elif tableName == 'Donors':
            rs.printOrPreviewDonorReport(samdb, printPreviewOrCSV)
        elif tableName == 'Items':
            rs.printOrPreviewItemReport(samdb, printPreviewOrCSV)