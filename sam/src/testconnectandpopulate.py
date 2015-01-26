'''
testconnectandpopulate.py

Created on Jan 3, 2010

@author: bob
'''

import sys
import MySQLdb
import dbservices
import profileservices
import auction
import donors
import buyers
import items
import purchases
import console


''' Connect to the database and then populate it --- This program assumes
    that a database already exists.  That database has been created
    either by the batch program createAuction or the GUI program
    SetUpAuction. '''

def testConnectAndPopulate():

    profile = profileservices.getProfile()
    samdb = dbservices.Samdb(profile['dbName'],
                             profile['hostName'],
                             int(profile['portNumber']),
                             profile['userName'],
                             profile['password'])
    samdb.useDatabase(profile['dbName'])
    ## Create objects for Auction, Donors, Buyers, Items, and Purchases
    da = auction.Auction()
    dd = donors.Donors()
    db = buyers.Buyers()
    di = items.Items()
    dp = purchases.Purchases()
    populate(samdb, da, dd, db, di, dp)


''' Set the details of the auction needed for printing an invoice and then
    populate the database with donors, then buyers, then items.  Next
    print the contents of the tables.  After that, make some purchaes
    and print the contents of the tables again.  This is some of the first
    code that I wrote, so it has lots of redundant try -- except stuff.
    It needs a rewrite.
'''
def populate(samdb, da, dd, db, di, dp):

    try:
        dd.addDonor(samdb, '000', 'Williams Jewelry Co.', '257 Main St.',
                    'Omaha, NE  87972', 'Marion Williams',
                    '892-325-8643', 'williams@yahoo.com')
        print 'ADDED DONOR WILLIAMS'
    except MySQLdb.Error, e:
        print "Error %d: %s" % (e.args[0], e.args[1])
        exit (1)
    except MySQLdb.Warning, e:
        print("Warning: ", e)

    try:
        dd.addDonor(samdb, '001', 'Nice Guys Cleaning Co.', 'Myrtle Ave.', \
                    'Petaluma, CA  63257', 'Ernest Halverson', \
                    '763-230-4527', 'ernest@aol.com')
        print 'ADDED DONOR HALVERSON'
    except MySQLdb.Error, e:
        print "Error %d: %s" % (e.args[0], e.args[1])
        exit (1)
    except MySQLdb.Warning, e:
        print("Warning: ", e)

    try:
        dd.addDonor(samdb, '002', 'The Stylist', '29 7th Ave.', \
                    'Orange, NJ  08762', 'Martha Grimes', \
                    '762-325-1257', 'martha@thestylist.com')
        print 'ADDED DONOR GRIMES'
    except MySQLdb.Error, e:
        print "Error %d: %s" % (e.args[0], e.args[1])
        exit (1)
    except MySQLdb.Warning, e:
        print("Warning: ", e)
 
    try:
        dd.addDonor(samdb, '235', 'Ace Hardware', 'Greenville Highway', \
                    'Hendersonville, NC  28739', 'Martha Wilkinson', \
                    '828-325-1257', 'martha@acehvl.com')
        print 'ADDED DONOR WILKINSON'
    except MySQLdb.Error, e:
        print "Error %d: %s" % (e.args[0], e.args[1])
        exit (1)
    except MySQLdb.Warning, e:
        print("Warning: ", e)
        
    try:
        dd.addDonor(samdb, '152', 'Flowers by Janine', '29 7th Ave.', \
                    'Hendersonville, NC  28739', 'Janine Watkins', \
                    '828-325-7892', 'janine@janinesflowers.com')
        print 'ADDED DONOR JANINE'
    except MySQLdb.Error, e:
        print "Error %d: %s" % (e.args[0], e.args[1])
        exit (1)
    except MySQLdb.Warning, e:
        print("Warning: ", e)
           
    try:
        db.addBuyer(samdb, '000', 'Smith', 'Harold', '113 Stanford', \
                    'Hollywood, CA 23523', '923-123-3241')
        print 'ADDED BUYER SMITH'

    except MySQLdb.Error, e:
        print "Error %d: %s" % (e.args[0], e.args[1])
        exit (1)
    except MySQLdb.Warning, e:
        print("Warning: ", e)
        
    try:
        db.addBuyer(samdb, '001', 'Lewis', 'Margaret and Bill', \
                    '235 Williston', 'Kansas City, MO 32594-3242', \
                    '232-827-3294')
        print 'ADDED BUYER LEWIS'
    except MySQLdb.Error, e:
        print "Error %d: %s" % (e.args[0], e.args[1])
        exit (1)
    except MySQLdb.Warning, e:
        print("Warning: ", e)

    try:
        db.addBuyer(samdb, '002', 'Kneifel', 'Ernest and Helen', \
                    '123 Oak', 'Chicago, IL 89694', \
                    '892-325-2379')
        print 'ADDED BUYER KNEIFEL'
    except MySQLdb.Error, e:
        print "Error %d: %s" % (e.args[0], e.args[1])
        exit (1)
    except MySQLdb.Warning, e:
        print("Warning: ", e)

    try:
        db.addBuyer(samdb, '003', 'Summers', 'Maurice and Ethel', \
                    '2325 First St. Apt 24', 'Los Angeles, CA 9725-1279', \
                    '323-695-2353')
        print 'ADDED BUYER SUMMERS'
    except MySQLdb.Error, e:
        print "Error %d: %s" % (e.args[0], e.args[1])
        exit (1)
    except MySQLdb.Warning, e:
        print("Warning: ", e)

    try:
        db.addBuyer(samdb, '004', 'Heath', 'Harold and Maude', \
                    '9372 Elm St.', 'Monroe, AL 23542', \
                    '694-325-5745')
        print 'ADDED BUYER HEATH'
    except MySQLdb.Error, e:
        print "Error %d: %s" % (e.args[0], e.args[1])
        exit (1)
    except MySQLdb.Warning, e:
        print("Warning: ", e)
   
    di.addItem(samdb, '000', 'Condo at Myrtle Beach for a week', \
               '002', '1000', '400', '50')
    di.addItem(samdb, '001', 'Book: Travel Guide to Europe',
               '001', '25', '5', '1')
    di.addItem(samdb, '002', 'Book: Gullivers Travels', \
               '001', '25', '5', '1')
    di.addItem(samdb, '003', 'Air fare to Hawaii', \
               '002', '1000', '500', '50')
    di.addItem(samdb, '004', 'Chiropractic consult', \
               '000', '100', '40', '5')
    di.addItem(samdb, '005', 'Ten dance lessons', \
               '001', '250', '50', '5')
    di.addItem(samdb, '006', 'South America Travel Book', \
               '002', '25', '5', '1')
    di.addItem(samdb, '007', 'Beauty Consultation', \
               '000', '100', '25', '1')
    di.addItem(samdb, '008', 'Dog Training Lessons', \
               '002', '100', '25', '1')
    
    print("DATABASE LOADED")

    cnsole = console.Console()

    print ("\nNOW SHOW THE AUCTION INFORMATION ON THE CONSOLE")
    cnsole.displayAuctionData(samdb)

    print ("\nNOW SHOW THE BUYERS TABLE ON THE CONSOLE")
    cnsole.displayBuyers(samdb)
    
    print ("\nNOW SHOW THE DONORS TABLE ON THE CONSOLE")
    cnsole.displayDonors(samdb)
    
    print ("\nNOW SHOW THE ITEMS TABLE ON THE CONSOLE")
    cnsole.displayItems(samdb)
    
    print ("\nPURCHASE SOME ITEMS")
    dp.purchaseItem(samdb, '000', '000', '1250')
    dp.purchaseItem(samdb, '001', '002', '18')
    dp.purchaseItem(samdb, '002', '004', '24')
    dp.purchaseItem(samdb, '003', '000', '975')
    dp.purchaseItem(samdb, '004', '003', '85')
    dp.purchaseItem(samdb, '005', '003', '150')
    dp.purchaseItem(samdb, '007', '002', '65')
    dp.purchaseItem(samdb, '008', '003', '125')

    print("\nNOW TWO BUYERS PAY FORM ITEMS IN THEIR CART")
    db.updateBuyerPaid(samdb,  '002')
    db.updateBuyerPaid(samdb,  '003')

    print ("\nNOW LOOK AT THE ITEMS TABLE AGAIN")
    cnsole.displayItems(samdb)
    
    '''
    print ("\nNOW SHOW SOME PURCHASES ON THE CONSOLE")
    print ("\nPurchases for buyer 000:")
    cnsole.displayPurchases(samdb, '000')
    print ("\nPurchases for buyer 001:")    
    cnsole.displayPurchases(samdb, '001')
    print ("\nPurchases for buyer 002:")   
    cnsole.displayPurchases(samdb, '002')
    print ("\nPurchases for buyer 003:")    
    cnsole.displayPurchases(samdb, '003')
    print ("\nPurchases for buyer 004:")    
    cnsole.displayPurchases(samdb, '004')
    '''

    print ("\nDRIVER: NOW SHOW ALL PURCHASES BY ALL BUYERS ON THE CONSOLE")
    cnsole.displayAllPurchases(samdb)

if __name__ == '__main__':
    testConnectAndPopulate()