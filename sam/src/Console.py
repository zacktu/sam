'''
Created on Feb 14, 2010

@author: bob
'''

import MySQLdb

class Console(object):
    '''
    classdocs
    '''


    def __init__(self):
        '''
            Constructor
        '''
        
    ''' Display all of the auction information '''
    def DisplayAuctionData(self, samdb):
        query = "SELECT * FROM Auction"
        rows = self.GetRows(samdb, query)
        for row in rows:
            print (row[0] + ':  ' + row[1]);
       
    ''' Display all of the buyers on the console. '''
    def DisplayBuyers(self, samdb):
        query = "SELECT * FROM Buyers ORDER BY buyer_number"
        rows = self.GetRows(samdb, query)
        print ("{0:3} {1:20} {2:20} {3:40} {4:15} {5:2} {6:10} {7:12} {8:12}"\
            .format("bno", "last", "first", "street", "city", "st", "zip",\
                    "telno1", "telno2"))
        print ("{0} {1} {2} {3} {4} {5} {6} {7} {8}" \
            .format('-'*3, '-'*20, '-'*20, '-'*40, '-'*15, '-'*2,\
                    '-'*10, '-'*12, '-'*12))
        for row in rows:
            print ("{0:3} {1:20} {2:20} {3:40} {4:15} {5:2} {6:10} {7:12} {8:12}" \
                .format(row[0], row[1], row[2], row[3], row[4], row[5],\
                        row[6],row[7], row[8]))

    ''' Display all of the donors on the consolem '''
    def DisplayDonors(self, samdb):
        query = "SELECT * FROM Donors ORDER BY donor_number"
        rows = self.GetRows(samdb, query)
        print ("{0:3} {1:30} {2:30} {3:20} {4:2} {5:5} {6:30} {7:12} {8:30}"\
            .format("dno", "name", "street", "city", "st", "zip", "contact",\
                    "telno", "email"))
        print ("{0} {1} {2} {3} {4} {5} {6} {7} {8}" \
            .format('-'*3, '-'*30, '-'*30, '-'*20, '-'*2, '-'*5, '-'*30,\
                    '-'*12, '-'*30))
        for row in rows:
            print ("{0:3} {1:30} {2:30} {3:20} {4:2} {5:5} {6:30} {7:12} {8:30}" \
                .format(row[0], row[1], row[2], row[3], row[4], row[5],\
                        row[6], row[7], row[8]))

    ''' Display all the items on the console.'''    
    def DisplayItems(self, samdb):
        query = "SELECT * FROM Items ORDER BY item_number"
        rows = self.GetRows(samdb, query)
        print ("{0:3} {1:50} {2:3} {3:6} {4:6} {5:6} {6:3} {7:6}"\
            .format("ino", "description", "dno", "retail", "minbid", "incr",\
                    "bno", "amount", "contact person"))
        print ("{0} {1} {2} {3} {4} {5} {6} {7}" \
            .format('-'*3, '-'*50, '-'*3, '-'*6, '-'*6, '-'*6, '-'*3, '-'*6))
        for row in rows:
            print ("{0:3} {1:50} {2:3} {3:>6} {4:>6} {5:>6} {6:3} {7:>6}" \
                .format(row[0], row[1], row[2], row[3], row[4], row[5],\
                        row[6], row[7]))
            
    def DisplayPurchases(self, samdb, buyerno):
        #print '\nBuyer number', buyerno
        query = "SELECT item_description, item_salesprice FROM Items " \
                + "WHERE item_purchasedby = '" + buyerno + "';"
        #print 'QUERY IN CONSOLE.DISPLAYPURCHASES IS ', query
        rows = self.GetRows(samdb, query)
        if len(rows) > 0:
            #print 'ROWS FROM THE DATABASE', rows
            print ("{0:50} {1:6}".format('description', 'price'))
            print ("{0} {1}".format('-'*50, '-'*6))
            sum = 0
            for row in rows:
                sum += int(row[1])
                print ("{0:50} {1:>6}".format(row[0], row[1]))
            print ("{0:50} {1:>6}".format('TOTAL PURCHASE', str(sum)))
            
    ''' Display all purchases for all buyers on the console '''
    def DisplayAllPurchases(self, samdb):
        print ("PRINTING ALL PURCHASES")
        query = "SELECT buyer_number, buyer_first, buyer_last, buyer_telno1 \
        FROM Buyers;"
        rows = self.GetRows(samdb, query)
        if len(rows) > 0:
            for row in rows:
                print ("\n{0:3} {1:30} {2:12}" \
                   .format(row[0], row[1] + " " + row[2], row[3]))
                buyerno = row[0]
                self.DisplayPurchases(samdb, buyerno)
                
    def GetRows(self, samdb, query):
        try:
            rows = samdb.FetchRows(query)
            return rows
        except MySQLdb.Error, e:
            print "Error %d: %s" % (e.args[0], e.args[1])
            return
        except MySQLdb.Warning, e:
            print("Warning: ", e)
        
                
