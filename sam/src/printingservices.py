'''
Created on Oct 26, 2009

@author: bob

Construct various troff reports to be printed by the Silent Auction Manager.
The separate lines required by troff are built here.  The header lines are
taken from the Auction table.  Information about purchases, etc., is taken
from the Buyers table.

'''

import os
import subprocess
from random import sample
from string import digits, ascii_uppercase, ascii_lowercase
import csv
from tempfile import gettempdir
import buyers
import auction
import donors
import items

##### the next imports are for TEST SCAFFOLDING
import sys
import MySQLdb
import dbservices
###### END OF SPECIAL IMPORTS

class PrintingServices():

    def __init__(self, parent, samdb):
        self.parent = parent
        self.samdb = samdb
        self.auction = auction.Auction()
        self.buyers = buyers.Buyers()
        self.donors = donors.Donors()
        self.items = items.Items()
        self.fname = self.rand_fname('xxx', 8)
        lines = []
        
    def previewOneCartOrReceipt(self, buyerNum, whatToPrint):
        lines = self.buildOneCartOrReceipt(buyerNum, whatToPrint)
        self.writeFile(self.fname, lines)
        self.previewPortrait(self.fname)
        
    def printOneCartOrReceipt(self, buyerNum, whatToPrint):
        lines = self.buildOneCartOrReceipt(buyerNum, whatToPrint)
        self.writeFile(self.fname, lines)
        self.printPortrait(self.fname)
        
    def previewAllCartsOrReceipts(self, whatToPrint):
        lines = self.buildAllCartsOrReceipts(whatToPrint)
        self.writeFile(self.fname, lines)
        self.previewPortrait(self.fname)
        
    def printAllCartsOrReceipts(self, whatToprint):
        lines = self.buildAllCartsOrReceipts(whatToPrint)
        self.writeFile(self.fname, lines)
        self.printPortrait(self.fname)
        
    def buildOneCartOrReceipt(self, buyerNum, whatToPrint):
        lines = self.buildCartOrReceiptHeader(buyerNum, whatToPrint)
        lines = lines + self.buildCartOrReceiptTable(buyerNum)
        lines.append('.sp 2\n')
        lines.append('Thank you for your participation.\n')
        return lines
    
    def buildAllCartsOrReceipts(self, whatToPrint):
        firstTime = True
        allBuyers = self.buyers.getAllBuyers(self.samdb)
        for buyer in allBuyers:
            moreLines = self.buildOneCartOrReceipt(buyer[0], whatToPrint)
            if firstTime:
                lines = moreLines
                firstTime = False
            else:
                lines = lines + ['.pn 1\n'] + ['.bp\n'] + moreLines
        return lines
        
    def previewSummaryOfPurchases(self, whatToPrint):
        lines = self.buildSummaryOfPurchases(whatToPrint)
        self.writeFile(self.fname, lines)
        self.previewPortrait(self.fname)
        
    def printSummaryOfPurchases(self, whatToPrint):
        lines = self.buildSummaryOfPurchases(whatToPrint)
        self.writeFile(self.fname, lines)
        self.printPortrait(self.fname)

    def buildSummaryOfPurchases(self, whatToPrint):
        lines = self.buildSummaryHeader(whatToPrint)
        allBuyers = self.buyers.getAllBuyers(self.samdb)
        for buyer in allBuyers:
            lines = lines + self.buildSummaryOfBuyers(buyer[0])
            lines = lines + self.buildCartOrReceiptTable(buyer[0])
        return lines
    
    def buildSummaryHeader(self, whatToPrint):
        lines = []
        ###lines.append('.ll 120\n')  #IS THIS OKAY?
        lines.append('.sp 0.5i\n')
        lines.append('.ft B\n')
        lines.append('.ce 4\n')
        try:
            lines.append(self.auction.GetAuctionTitle(self.samdb) + '\n')
            lines.append(self.auction.GetAuctionSubtitle(self.samdb) + '\n')
            lines.append(self.auction.GetAuctionDate(self.samdb) + '\n')
            if whatToPrint == 'carts':
                lines.append('\nShopping Cart Summary\n')
            elif whatToPrint == 'receipts':
                lines.append('\nReceipt Summary\n')
            elif whatToPrint == 'donors':
                lines.append('\nDonors Report\n\n')
            elif whatToPrint == 'buyers':
                lines.append('\nBuyers Report\n\n')
            elif whatToPrint == 'items':
                lines.append('\nItems Report\n\n')
        except MySQLdb.Error, e:
            print "PrintingServices.buildSummaryHeader: Error %d: %s" \
                    % (e.args[0], e.args[1])
            sys.exit (1)
        except MySQLdb.Warning, e:
            print("PrintingServices.buildSummaryHeader: Warning: ", e)
        lines.append('.ft R\n')
        return lines
    
    '''
        This is the set of buyers needed for showing a summary of
        shopping carts or receipts
    '''
    def buildSummaryOfBuyers(self, buyerNum):
        buyerInfo = self.buyers.fetchBuyer(self.samdb, buyerNum)
        lines = []
        lines.append('.sp 2\n')
        lines.append('.ft B\n')
        lines.append(buyerNum + '\n')
        lines.append('.br\n')
        lines.append(buyerInfo[0] + ', ' + buyerInfo[1] + '\n')
        lines.append('.ft R\n')
        lines.append('.sp\n')
        return lines

    def buildCartOrReceiptHeader(self, buyerNum, whatToPrint):
        buyerInfo = self.buyers.fetchBuyer(self.samdb, buyerNum)

        lines = []
        lines.append('.ps 15\n')
        lines.append('.ft B\n')
        lines.append('.sp 1.5i\n')
        lines.append('.ce\n')
        try:
            lines.append(self.auction.GetAuctionTitle(self.samdb) + '\n')
            lines.append('.sp\n')
            lines.append('.ce\n')
            lines.append('.ps -2\n')
            lines.append(self.auction.GetAuctionSubtitle(self.samdb) + '\n')
            lines.append('.ps -2\n')
            lines.append('.sp\n')
            lines.append('.ce\n')
            lines.append(self.auction.GetAuctionDate(self.samdb) + '\n')
        except MySQLdb.Error, e:
            print "PrintingServices.buildCartOrReceiptHeader: Error %d: %s" \
                    % (e.args[0], e.args[1])
            sys.exit (1)
        except MySQLdb.Warning, e:
            print("PrintingServices.buildCartOrReceiptHeader: Warning: ", e)
        lines.append('.sp 0.5i\n')
        lines.append('.ce\n')
        if whatToPrint == 'carts':
            lines.append('SHOPPING CART\n')
        elif whatToPrint == 'receipts':
            lines.append('RECEIPT\n')
        lines.append('.ps -2\n')
        lines.append('.ft R\n')
        lines.append('.sp 1.0i\n')
        lines.append(buyerInfo[1] + ' ' + buyerInfo[0] + '\n')
        lines.append('.br\n')
        lines.append(buyerInfo[2] + '\n')
        lines.append('.br\n')
        lines.append(buyerInfo[3]  + '\n')
        lines.append('.br\n')
        lines.append(buyerInfo[4] + '\n')
        lines.append('.br\n')
        lines.append('Buyer number ' + buyerNum + '\n')
        lines.append('.sp 3\n')
        return lines
    
    def buildCartOrReceiptTable(self, buyerNum):
        buyerInfo = self.buyers.fetchBuyer(self.samdb, buyerNum)
        lines = []
        lines.append('.TS\n')
        lines.append('box, expand, tab(`);\n')
        lines.append('cI cI cI.\n')
        lines.append('Item Number`Description`Winning Bid\n')
        lines.append('_\n')
        lines.append('.T&\n')
        lines.append('n l n.\n')
        rows = self.buyers.getBuyersPurchases(self.samdb, buyerNum)
        totalPurchase = 0
        for row in rows:
            lines.append(row[0] + '`' + row[1] + '`' + str(row[2]) + '\n')
            totalPurchase += int(row[2])
        lines.append('.T&\n')
        lines.append('n rI n.\n')
        lines.append('`TOTAL`$' + str(totalPurchase) + '\n')
        lines.append('.TE\n')
        return lines

    def buildDonorReport(self, samdb):
        lines = self.buildSummaryHeader('donors')
        lines.append('.TS\n')
        lines.append('box, expand, tab(`);\n')
        lines.append('cI cI cI cI cI cI cI.\n')
        lines.append('Donor`Name`Street`City`Contact`Telephone`Email\n')
        lines.append('_\n')
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
        lines = self.buildSummaryHeader('buyers')
        lines.append('.TS\n')
        lines.append('box, expand, tab(`);\n')
        lines.append('cI cI cI cI cI cI.\n')
        lines.append('Buyer`Last`First`Street`City`Telephone\n')
        lines.append('_\n')
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
        lines = self.buildSummaryHeader('items')
        lines.append('.TS\n')
        lines.append('box, expand, tab(`);\n')
        lines.append('cI cI cI cI cI cI cI cI.\n')
        lines.append(
            'Item`Description`Donor`Retail`Min Bid`Increment`Buyer`Price\n')
        lines.append('_\n')
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

    def printDonorReport(self, samdb, printOrPreview):
        lines = self.buildDonorReport(samdb)
        #landscape lines are 9i wide
        lines.insert(0, '.ll 9i\n')
        if (printOrPreview == 'print'):
            #page offset determined by experimentation
            lines.insert(1, '.po 1.75i\n')  #needed for centering printed file
            self.writeFile(self.fname, lines)
            self.printLandscape(self.fname)
        elif (printOrPreview == 'preview'):
            self.writeFile(self.fname, lines)
            self.previewLandscape(self.fname)
        else:
            print('printingservices.printDonorReport: invalid parameter '
                  + 'printOrPreview = ' + printOrPreview)
            print('Bugout!')
            sys.exit()

    def printBuyerReport(self, samdb, printOrPreview):
        lines = self.buildBuyerReport(samdb)
        #landscape lines are 9i wide
        lines.insert(0, '.ll 9i\n')
        if (printOrPreview == 'print'):
            #page offset determined by experimentation
            lines.insert(1, '.po 1.75i\n')  #needed for centering printed file
            self.writeFile(self.fname, lines)
            self.printLandscape(self.fname)
        elif (printOrPreview == 'preview'):
            self.writeFile(self.fname, lines)
            self.previewLandscape(self.fname)
        else:
            print('printingservices.printBuyerReport: invalid parameter '
                  + 'printOrPreview = ' + printOrPreview)
            print('Bugout!')
            sys.exit()

    def printItemReport(self, samdb, printOrPreview):
            lines = self.buildItemReport(samdb)
            #landscape lines are 9i wide
            lines.insert(0, '.ll 9i\n')
            if (printOrPreview == 'print'):
                #page offset determined by experimentation
                lines.insert(1, '.po 1.75i\n')  #needed for centering printed file
                self.writeFile(self.fname, lines)
                self.printLandscape(self.fname)
            elif (printOrPreview == 'preview'):
                self.writeFile(self.fname, lines)
                self.previewLandscape(self.fname)
            else:
                print('printingservices.printItemReport: invalid parameter '
                      + 'printOrPreview = ' + printOrPreview)
                print('Bugout!')
                sys.exit()

    def writeFile(self, fname, lines):
        try:
            fout = open(fname, 'w')
            for line in lines:
                fout.write(line)
            fout.close()
        except (IOError, OSError) as e:
            Dialogs.DisplayErrorDialog(e.args[1])
            return

    def previewPortrait(self, fname):
        pdfname = fname +'.pdf'
        command = 'groff -t -t ' + fname \
                      + ' | ps2pdf - ' + pdfname + ' ; ' \
                      + 'evince ' + pdfname
        subprocess.Popen(command, shell=True)
               
    def printPortrait(self, fname):
        command = 'groffer -l ' + fname + ' 2>/dev/null'
        subprocess.Popen(command, shell=True)

    def previewLandscape(self, fname):
        pdfname = fname +'.pdf'
        command = 'groff -t -P-l -t ' + fname \
                      + ' | ps2pdf - ' + pdfname + ' ; ' \
                      + 'evince ' + pdfname
        subprocess.Popen(command, shell=True)

    def printLandscape(self, fname):
        command = 'groffer -P-l -l ' + fname + ' 2>/dev/null '
        subprocess.Popen(command, shell=True)

    def doCSV(self, samdb, tableName):
        columnHeaders = samdb.getColumnHeaders(tableName)
        csvFile = csv.writer(open('/home/bob/Desktop/csv/buyers.csv', "wb"))
        csvFile.writerow(columnHeaders)
        allBuyers = self.buyers.getAllBuyers(self.samdb)
        for buyer in allBuyers:
            buyerRow = self.buyers.fetchBuyer(self.samdb, buyer[0])
            fullRow = list(buyerRow)
            fullRow.insert(0, buyer[0])
            csvFile.writerow(fullRow)

    def OnExit(self, evt):
        self.Close()

    def OnClearSelection(self, evt):
        evt.Skip()
        wx.CallAfter(self.tc.SetInsertionPoint,
                     self.tc.GetInsertionPoint())

    def rand_fname(self, suffix, length=8):
        chars = ascii_lowercase + ascii_uppercase + digits

        fname = os.path.join(gettempdir(), 'tmp-'+ 
            ''.join(sample(chars, length)) + suffix)

        return fname if not os.path.exists(fname) \
            else rand_fname(suffix, length)

if __name__ == '__main__':
    dummy = buyers.Buyers()
    samdb = dbservices.connect(sys.argv)
    pr = PrintingServices(dummy, samdb)
    #pr.printBuyerReport(samdb, 'preview')
    #pr.printDonorReport(samdb, 'preview')
    #pr.printItemReport(samdb, 'preview')
    pr.doCSV(samdb, 'Buyers')
