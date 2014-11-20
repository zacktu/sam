'''
Created on Jan 3, 2010

@author: bob
'''

import dbservices
import donors
import buyers
import items
import console
import Printer

if __name__ == '__main__':
    samdb = dbservices.Samdb(dbname='mysql')
    samdb.CreateDatabase()
    dd = donors.Donors()
    dd.CreateDonorsTable(samdb)
    db = buyers.Buyers()
    db.CreateBuyersTable(samdb)
    di = items.Items()
    di.CreateItemsTable(samdb)
    
    dd.AddDonor(samdb, '000', 'Williams Jewelry Co.', '257 Main St.', 'Omaha', 'NE', \
                '87972', '892-325-8643', '828-696-2684', 'Marion Williams')
    dd.AddDonor(samdb, '001', 'Nice Guys Cleaning Co.', 'Myrtle Ave.', 'Petaluma', \
                'CA', '63527-2357', '763-230-4527', '', 'Ernest Halverson')
    dd.AddDonor(samdb, '002', 'The Stylist', '29 7th Ave.', 'Orange', 'NJ', \
                '08762-8256', '762-325-1257', '562-325-8907', 'Martha Grimes')
    
    db.AddBuyer(samdb, '000', 'Smith', 'Harold', '113 Stanford', 'Hollywood', 'CA', \
                '23523', '923-123-3241', '')
    db.AddBuyer(samdb, '001', 'Lewis', 'Margaret and Bill', '235 Williston', \
                'Kansas City', 'MO', '32594-3242', '232-827-3294', '232-827-3295')
    db.AddBuyer(samdb, '002', 'Kneifel', 'Ernest and Helen', '123 Oak', 'Chicago', \
                'IL', '89694', '892-325-2379', '892-694-9453')
    db.AddBuyer(samdb, '003', 'Summers', 'Maurice and Ethel', '2325 First St. Apt 24', \
                'Los Angeles', 'CA', '97235-1279', '323-695-2353', '')
    db.AddBuyer(samdb, '004', 'Heath', 'Harold and Maude', '9372 Elm St.', \
                'Monroe', 'AL', '23542', '694-325-5745', '')
    
    di.AddItem(samdb, '0000', '002', 'Condo at Myrtle Beach for a week', \
                '1000', '400', '50', '', '')
    di.AddItem(samdb, '0001', '001', 'Book: Travel Guide to Europe', 
                '25', '5', '1','', '')
    di.AddItem(samdb, '0002', '001', 'Book: Gullivers Travels', '25', '5', '1',
                '', '')
    di.AddItem(samdb, '0003', '002', 'Air fare to Hawaii', '1000', '500', '50',
                '', '')
    di.AddItem(samdb, '0004', '000', 'Chiropractic consult', '100', '40', '5', '', '')
    di.AddItem(samdb, '0005', '001', 'Ten dance lessons', '250', '50', '5', '', '')
    di.AddItem(samdb, '0006', '002', 'South America Travel Book', '25', '5', '1', '', '')
    di.AddItem(samdb, '0007', '000', 'Beauty Consultation', '100', '25', '1', '', '')
    di.AddItem(samdb, '0008', '002', 'Dog Training Lessons', '100', '25', '1', '', '')
    
    print("DATABASE LOADED")
    
    console = console.Console()
    
    print ("NOW SHOW THE BUYERS TABLE ON THE CONSOLE")
    console.DisplayBuyers(samdb)
    
    print ("NOW SHOW THE DONORS TABLE ON THE CONSOLE")
    console.DisplayDonors(samdb)
    
    print ("NOW SHOW THE ITEMS TABLE ON THE CONSOLE")
    console.DisplayItems(samdb)
    
    print ("PURCHASE SOME ITEMS")
    di.PurchaseItem(samdb, '0000', '000', '1250')
    di.PurchaseItem(samdb, '0001', '002', '18')
    di.PurchaseItem(samdb, '0002', '004', '24')
    di.PurchaseItem(samdb, '0003', '000', '975')
    di.PurchaseItem(samdb, '0004', '003', '85')
    di.PurchaseItem(samdb, '0005', '003', '150')
    di.PurchaseItem(samdb, '0007', '002', '65')
    di.PurchaseItem(samdb, '0008', '003', '125')
    
    print ("NOW LOOK AT THE ITEMS TABLE AGAIN")
    console.DisplayItems(samdb)
    
    print ("NOW SHOW SOME PURCHASES ON THE CONSOLE")
    print ("\nPurchases for buyer 000:")
    console.DisplayPurchases(samdb, '000')
    print ("\nPurchases for buyer 001:")    
    console.DisplayPurchases(samdb, '001')
    print ("\nPurchases for buyer 002:")   
    console.DisplayPurchases(samdb, '002')
    print ("\nPurchases for buyer 003:")    
    console.DisplayPurchases(samdb, '003')
    print ("\nPurchases for buyer 004:")    
    console.DisplayPurchases(samdb, '004')
    
    
    print ("DRIVER: NOW SHOW ALL PURCHASES BY ALL BUYERS ON THE CONSOLE")
    console.DisplayAllPurchases(samdb)
    
    print ("DRIVER: NOW SHOW ALL PURCHASES FOR ONE BUYER ON THE CONSOLE")
    pr = Printer.Printer()
    pr.PrintInvoice(samdb, '000')