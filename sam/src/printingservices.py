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
import dialogs

##### the next imports are for TEST SCAFFOLDING
import sys
import MySQLdb
import dbservices
###### END OF SPECIAL IMPORTS

class PrintingServices():

    def __init__(self, samdb):
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
        if whatToPrint == 'receipts':
            if self.buyers.hasBuyerBoughtAnything(self.samdb, buyerNum):
                self.buyers.updateBuyerPaid(self.samdb, buyerNum)
                self.printPortraitWithOverlay(self.fname)
            else:
                dialogs.displayErrorDialog \
                        ("Buyer " + buyerNum + "'s cart is empty.")
        else:
            self.printPortrait(self.fname)

    def previewAllCartsOrReceipts(self, whatToPrint):
        if ((whatToPrint == 'carts')
                and (self.items.areAllCartsEmpty(self.samdb))):
            dialogs.displayErrorDialog \
                    ("All shopping carts are empty.")
            return
        elif ((whatToPrint == 'receipts')
                and (self.buyers.thereAreNoReceipts(self.samdb))):
            dialogs.displayErrorDialog \
                    ("No buyer has been given a receipt.")
            return
        else:
            lines = self.buildAllCartsOrReceipts(whatToPrint)
            self.writeFile(self.fname, lines)
            self.previewPortrait(self.fname)
        
    def printAllCartsOrReceipts(self, whatToPrint):
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
            if ((whatToPrint == 'carts') or
                    (self.buyers.hasBuyerPaid(self.samdb, buyer[0]))):
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
            if ((whatToPrint == 'carts') or
                    (self.buyers.hasBuyerPaid(self.samdb, buyer[0]))):
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
            lines.append(self.auction.getAuctionTitle(self.samdb) + '\n')
            lines.append(self.auction.getAuctionSubtitle(self.samdb) + '\n')
            lines.append(self.auction.getAuctionDate(self.samdb) + '\n')
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
            lines.append(self.auction.getAuctionTitle(self.samdb) + '\n')
            lines.append('.sp\n')
            lines.append('.ce\n')
            lines.append('.ps -2\n')
            lines.append(self.auction.getAuctionSubtitle(self.samdb) + '\n')
            lines.append('.ps -2\n')
            lines.append('.sp\n')
            lines.append('.ce\n')
            lines.append(self.auction.getAuctionDate(self.samdb) + '\n')
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

    def printPortraitWithOverlay(self, fname):
        pdfname = fname +'.pdf'
        overlayfname = fname + '.olay'
        command = 'groff -t ' + fname \
                      + ' | ps2pdf - ' + pdfname + ' ; ' \
                      + ' pdftk ' + pdfname \
                      + ' background ../otherfiles/images/paid.pdf ' \
                      + ' output ' + overlayfname + ' ; ' \
                      + ' lpr ' + overlayfname
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

    def OnExit(self, evt):
        self.Close()

    def OnClearSelection(self, evt):
        evt.Skip()
        wx.CallAfter(self.tc.SetInsertionPoint,
                     self.tc.GetInsertionPoint())

    ### Generate unique name for a temporary file
    def rand_fname(self, suffix, length=8):
        chars = ascii_lowercase + ascii_uppercase + digits

        fname = os.path.join(gettempdir(), 'tmp-'+ 
            ''.join(sample(chars, length)) + suffix)

        return fname if not os.path.exists(fname) \
            else rand_fname(suffix, length)

    def checkBuyerPurchases(self, samdb, buyerNumber):
        return self.buyers.hasBuyerBoughtAnything(samdb, buyerNumber)

if __name__ == '__main__':
    samdb = dbservices.connect(sys.argv)
    prs = PrintingServices(samdb)
    #prs.printOrPreviewBuyerReport(samdb, 'preview')
    #prs.donorReport(samdb, 'print')
    #prs.printOrPreviewItemReport(samdb, 'preview')
    #prs.doCSV(samdb, 'Buyers')
    #prs.doCSV(samdb, 'Donors')
    #prs.doCSV(samdb, 'Items')



