'''
Created on Feb 13, 2010
Not a mainstream program.
But a noble experiment!
Still making sure!!
Trying once again!!!
@author: bob
'''
import MySQLdb

class Printer(object):
    '''
    classdocs
    '''

    def __init__(self):
        '''
        Constructor
        '''
        
    def PrintInvoice(self, samdb, buyerno):
        query = "SELECT item_description, item_salesprice FROM Items " \
                + "WHERE item_purchasedby = '" + buyerno + "';"
        try:
            rows = samdb.fetchRows(query)
        except MySQLdb.Error, e:
            print "Error %d: %s" % (e.args[0], e.args[1])
            return
        except MySQLdb.Warning, e:
            print("Warning: ", e)
        if len(rows) > 0:
            print ("{0:50} {1:6}".format('description', 'price'))
            print ("{0} {1}".format('-'*50, '-'*6))
            sum = 0
            for row in rows:
                sum += int(row[1])
                print ("{0:50} {1:>6}".format(row[0], row[1]))
            print ("{0:50} {1:>6}".format('TOTAL PURCHASE', str(sum)))
            
        try:
            rows = samdb.fetchRows(query)
        except MySQLdb.Error, e:
            print "Error %d: %s" % (e.args[0], e.args[1])
            return
        except MySQLdb.Warning, e:
            print("Warning: ", e)