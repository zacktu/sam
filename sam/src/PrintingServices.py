'''
Created on Oct 26, 2009

@author: bob

Construct various troff reports to be printed by the Silent Auction Manager.
The separate lines required by troff are built here.  The header lines are
taken from the Auction table.  Information about purchases, etc., is taken
from the Buyers table.

'''

import Auction
import buyers
import os
import subprocess
from random import sample
from string import digits, ascii_uppercase, ascii_lowercase
from tempfile import gettempdir

class PrintingServices():
    
    def __init__(self, parent, samdb):
        self.parent = parent
        self.samdb = samdb
        self.auction = Auction.Auction()
        self.buyers = buyers.Buyers()
        self.fname = self.rand_fname('xxx', 8)
        
    def PreviewOneInvoiceOrReceipt(self, buyerNum, whatToPrint):
        lines = self.BuildOneInvoiceOrReceipt(buyerNum, whatToPrint)
        self.WriteFile(self.fname, lines)
        self.PreviewFile(self.fname)
        
    def PrintOneInvoiceOrReceipt(self, buyerNum, whatToPrint):
        lines = self.BuildOneInvoiceOrReceipt(buyerNum, whatToPrint)
        self.WriteFile(self.fname, lines)
        self.PrintFile(self.fname)
        
    def PreviewAllInvoicesOrReceipts(self, whatToPrint):
        lines = self.BuildAllInvoicesOrReceipts(whatToPrint)
        self.WriteFile(self.fname, lines)
        self.PreviewFile(self.fname)
        
    def PrintAllInvoicesOrReceipts(self, whatToprint):
        lines = self.BuildAllInvoicesOrReceipts(whatToPrint)
        self.WriteFile(self.fname, lines)
        self.PrintFile(self.fname)
        
    def BuildOneInvoiceOrReceipt(self, buyerNum, whatToPrint):
        lines = self.BuildInvoiceOrReceiptHeader(buyerNum, whatToPrint)
        lines = lines + self.BuildInvoiceOrReceiptTable(buyerNum)
        lines.append('.sp 2\n')
        lines.append('Thank you for your participation.\n')
        return lines
    
    def BuildAllInvoicesOrReceipts(self, whatToPrint):
        firstTime = True
        allBuyers = self.buyers.GetAllBuyers(self.samdb)
        for buyer in allBuyers:
            moreLines = self.BuildOneInvoiceOrReceipt(buyer[0], whatToPrint)
            if firstTime:
                lines = moreLines
                firstTime = False
            else:
                lines = lines + ['.pn 1\n'] + ['.bp\n'] + moreLines
        return lines
        
    def PreviewSummaryOfPurchases(self):
        lines = self.BuildSummaryOfPurchases()
        self.WriteFile(self.fname, lines)
        self.PreviewFile(self.fname)
        
    def PrintSummaryOfPurchases(self):
        lines = self.BuildSummaryOfPurchases()
        self.WriteFile(self.fname, lines)
        self.PrintFile(self.fname)

    def BuildSummaryOfPurchases(self):
        lines = self.BuildSummaryHeader()
        allBuyers = self.buyers.GetAllBuyers(self.samdb)
        for buyer in allBuyers:
            lines = lines + self.BuildSummaryBuyer(buyer[0])
            lines = lines + self.BuildInvoiceOrReceiptTable(buyer[0])
        return lines
    
    def BuildSummaryHeader(self):
        lines = []
        lines.append('.sp 0.5i\n')
        lines.append('.ft B\n')
        lines.append('.ce 3\n')
        try:
            lines.append(self.auction.GetAuctionTitle(self.samdb) + '\n')
            lines.append(self.auction.GetAuctionSubtitle(self.samdb) + '\n')
            lines.append(self.auction.GetAuctionDate(self.samdb) + '\n')
        except MySQLdb.Error, e:
            print "PrintingServices.BuildSummaryHeader: Error %d: %s" \
                    % (e.args[0], e.args[1])
            sys.exit (1)
        except MySQLdb.Warning, e:
            print("PrintingServices.BuildSummaryHeader: Warning: ", e)
        lines.append('.ft R\n')
        return lines
    
    def BuildSummaryBuyer(self, buyerNum):
        buyerInfo = self.buyers.FetchBuyer(self.samdb, buyerNum)
        lines = []
        lines.append('.sp 2\n')
        lines.append('.ft B\n')
        lines.append(buyerNum + '\n')
        lines.append('.br\n')
        lines.append(buyerInfo[0] + ', ' + buyerInfo[1] + '\n')
        lines.append('.ft R\n')
        lines.append('.sp\n')
        return lines
    
    def BuildInvoiceOrReceiptHeader(self, buyerNum, whatToPrint):
        buyerInfo = self.buyers.FetchBuyer(self.samdb, buyerNum)
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
            print "PrintingServices.BuildInvoiceOrReceiptHeader: Error %d: %s" \
                    % (e.args[0], e.args[1])
            sys.exit (1)
        except MySQLdb.Warning, e:
            print("PrintingServices.BuildInvoiceOrReceiptHeader: Warning: ", e)
        lines.append('.sp 0.5i\n')
        lines.append('.ce\n')
        if whatToPrint == 'carts':
            lines.append('INVOICE\n')
        else:
            lines.append('RECEIPT\n')
        lines.append('.ps -2\n')
        lines.append('.ft R\n')
        lines.append('.sp 1.0i\n')
        lines.append(buyerInfo[1] + ' ' + buyerInfo[0] + '\n')
        lines.append('.br\n')
        lines.append(buyerInfo[2] + '\n')
        lines.append('.br\n')
        lines.append(buyerInfo[3] + ', ' + buyerInfo[4] +  \
                     ' ' + buyerInfo[5] + '\n')
        lines.append('.br\n')
        lines.append(buyerInfo[6] + '\n')
        lines.append('.br\n')
        lines.append('Buyer number ' + buyerNum + '\n')
        lines.append('.sp 3\n')
        return lines
    
    def BuildInvoiceOrReceiptTable(self, buyerNum):
        buyerInfo = self.buyers.FetchBuyer(self.samdb, buyerNum)
        lines = []
        lines.append('.TS\n')
        lines.append('box, expand, tab(`);\n')
        lines.append('cI cI cI.\n')
        lines.append('Item Number`Description`Winning Bid\n')
        lines.append('_\n')
        lines.append('.T&\n')
        lines.append('n l n.\n')
        rows = self.buyers.GetBuyersPurchases(self.samdb, buyerNum)  
        totalPurchase = 0
        for row in rows:
            lines.append(row[0] + '`' + row[1] + '`' + str(row[2]) + '\n')
            totalPurchase += int(row[2])
        lines.append('.T&\n')
        lines.append('n rI n.\n')
        lines.append('`TOTAL`$' + str(totalPurchase) + '\n')
        lines.append('.TE\n')
        return lines
    
    def WriteFile(self, fname, lines):
        try:
            #fout = None
            fout = open(fname, 'w')
            for line in lines:
                fout.write(line)
            fout.close()
        except (IOError, OSError) as e:
            Dialogs.DisplayErrorDialog(e.args[1])
            return

    def PreviewFile(self, fname):
        command = 'groff -ms -t -f H -Tps -X ' + fname + ' 2> /dev/null; rm ' +fname
        subprocess.Popen(command, shell=True)
               
    def PrintFile(self, fname):
        command = 'groff -ms -t -f H -Tps -l ' + fname + ' 2> /dev/null; rm ' +fname
        subprocess.Popen(command, shell=True)


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
