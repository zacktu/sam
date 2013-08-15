'''
Created on Jan 3, 2010

@author: bob
'''

import warnings
import MySQLdb
import SAMDB
warnings.simplefilter("error", MySQLdb.Warning)

class Donors(object):
    '''
    classdocs
    '''
    
    def CreateDonorsTable(self, samdb):
        rows = "( \
            donor_number      char(3)     NOT NULL PRIMARY KEY, \
            donor_name        char(30)    NOT NULL, \
            donor_street      char(30)    NOT NULL, \
            donor_city        char(20)    NOT NULL, \
            donor_state       char(2)     NOT NULL, \
            donor_zip         char(5)     NOT NULL, \
            donor_contact     char(30)    NOT NULL, \
            donor_telno       char(12)    NOT NULL, \
            donor_email       char(30)    NULL \
            )"
        samdb.CreateTable("Donors", rows, "donor_number")

    def AddDonor(self, samdb, donor_number, donor_name, donor_street, donor_city,
                 donor_state, donor_zip, donor_contact, donor_telno, donor_email):
        fields = "donor_number, donor_name, donor_street, donor_city, \
                    donor_state, donor_zip, donor_contact, donor_telno, donor_email"
        values = "'" + donor_number + "'" + ',' \
               + "'" + donor_name + "'" + ',' \
               + "'" + donor_street + "'" + ',' \
               + "'" + donor_city + "'" + ',' \
               + "'" + donor_state + "'" + ',' \
               + "'" + donor_zip + "'" + ',' \
               + "'" + donor_contact + "'" ',' \
               + "'" + donor_telno + "'" + ',' \
               + "'" + donor_email + "'"
        samdb.InsertRow("Donors", fields, values)
        
    def FetchDonor(self, samdb, donorNumber):
        query = "SELECT donor_name, donor_street, donor_city, donor_state, \
                donor_zip, donor_contact, donor_telno, donor_email \
                FROM Donors WHERE donor_number = " + donorNumber + ";"
        return samdb.FetchRow(query)
        
    def UpdateDonor(self, samdb, donorNumber, name, street, city, state, \
                    zip, contact, telno, email):
        query = "UPDATE Donors  \
                    SET donor_name = '" + name + "' , \
                        donor_street = '"  + street + "' , \
                        donor_city = '" + city + "' , \
                        donor_state = '" + state + "' , \
                        donor_zip = '" + zip + "' , \
                        donor_contact = '" + contact + "' , \
                        donor_telno = '" + telno + "' , \
                        donor_email = '" + email + "' \
                    WHERE donor_number = '" + donorNumber + "' ; "
        samdb.ExecuteQuery(query)
        
    def DeleteDonor(self, samdb, donorNumber):
        samdb.DeleteRow("Donors", "donor_number", donorNumber)
        
    # Confirm whether a donor number is in the database.
    def IsValidDonorNumber(self, samdb, donorNumber):
        query = "SELECT donor_name FROM Donors \
                WHERE donor_number = '" + donorNumber + "' ; "
        rows = samdb.FetchRows(query)
        if len(rows) > 0:
            return True
        else:
            return False
        
    def GetDonorsItems(self, donorNumber, samdb):
        query = 'SELECT item_number FROM Items WHERE item_donatedby = ' \
                + donorNumber + ';'
        items = samdb.FetchRows(query)
        itemList = []
        for item in items:
            itemList.append(item[0])
        return itemList

if __name__ == '__main__':
    samdb = SAMDB.SAMDB()
    samdb.CreateDatabase()
    dt = Donors()
    dt.CreateDonorsTable(samdb)
    print("CREATED THE DONORS TABLE")