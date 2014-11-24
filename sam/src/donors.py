'''
Created on Jan 3, 2010

@author: bob
'''

import warnings
import MySQLdb
import dbservices
warnings.simplefilter("error", MySQLdb.Warning)

class Donors(object):
    '''
    classdocs
    '''
    
    def createDonorsTable(self, samdb):
        rows = "( \
            donor_number      char(3)     NOT NULL PRIMARY KEY, \
            donor_name        char(40)    NOT NULL, \
            donor_street      char(30)    NOT NULL, \
            donor_city        char(40)    NOT NULL, \
            donor_contact     char(30)    NOT NULL, \
            donor_telno       char(12)    NOT NULL, \
            donor_email       char(30)    NULL \
            )"
        samdb.createTable("Donors", rows, "donor_number")

    def addDonor(self, samdb, donor_number, donor_name, donor_street, donor_city,
                 donor_contact, donor_telno, donor_email):
        fields = "donor_number, donor_name, donor_street, donor_city, \
                    donor_contact, donor_telno, donor_email"
        values = "'" + donor_number + "'" + ',' \
               + "'" + donor_name + "'" + ',' \
               + "'" + donor_street + "'" + ',' \
               + "'" + donor_city + "'" + ',' \
               + "'" + donor_contact + "'" ',' \
               + "'" + donor_telno + "'" + ',' \
               + "'" + donor_email + "'"
        samdb.insertRow("Donors", fields, values)
        
    def fetchDonor(self, samdb, donorNumber):
        query = "SELECT donor_name, donor_street, donor_city, \
                donor_contact, donor_telno, donor_email \
                FROM Donors WHERE donor_number = " + donorNumber + ";"
        return samdb.fetchRow(query)
        
    def updateDonor(self, samdb, donorNumber, name, street, city, state, \
                    zip, contact, telno, email):
        query = "UPDATE Donors  \
                    SET donor_name = '" + name + "' , \
                        donor_street = '"  + street + "' , \
                        donor_city = '" + city + "' , \
                        donor_contact = '" + contact + "' , \
                        donor_telno = '" + telno + "' , \
                        donor_email = '" + email + "' \
                    WHERE donor_number = '" + donorNumber + "' ; "
        samdb.executeQuery(query)
        
    def deleteDonor(self, samdb, donorNumber):
        samdb.deleteRow("Donors", "donor_number", donorNumber)
        
    # Confirm whether a donor number is in the database.
    def isValidDonorNumber(self, samdb, donorNumber):
        query = "SELECT donor_name FROM Donors \
                WHERE donor_number = '" + donorNumber + "' ; "
        rows = samdb.fetchRows(query)
        if len(rows) > 0:
            return True
        else:
            return False
        
    def getDonorsItems(self, donorNumber, samdb):
        query = 'SELECT item_number FROM Items WHERE item_donatedby = ' \
                + donorNumber + ';'
        items = samdb.fetchRows(query)
        itemList = []
        for item in items:
            itemList.append(item[0])
        return itemList

if __name__ == '__main__':
    samdb = dbservices.Samdb()
    samdb.createDatabase()
    dt = Donors()
    dt.createDonorsTable(samdb)
    print("CREATED THE DONORS TABLE")