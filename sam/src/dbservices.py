'''
Created on Jan 1, 2010

This is the lowest level program with respect to mysql.  It can create, use,
and drop databases, create tables, and insert and delete rows in a table.

When the Samdb object is instantiated, it connects to the database using
the dbname 'mysql'.  That database always exists, so we will at least
have a connection.  

The logic of the CreateDatabase is most essential:
1) The name of the database to be created is received as a parameter (dbname)
2) drop dbname if it exists
3) create dbname
4) use dbname

Step 4 is essential because the Samdb object is passed around among all of
the modules that do anything with the database.  All of the mysql commands
will "use" the database that has been set at the time the database was
created.

Most of the database queries are handled by try-except higher up.  The
basic database actions (create, drop, use, etc.) are handled here.  If
something goes wrong with those actions, then there's no hope, so I might
as well just bugout.

@author: bob
'''

import sys
import warnings
import MySQLdb
warnings.simplefilter("error", MySQLdb.Warning)


class Samdb(object):
    '''
    classdocs
    '''
    
    def __init__(self, dbname, hostname='localhost',  portnumber='3306', \
                username='bob', password=''):
        '''
        Connect to a database.  The exception will be caught higher up.
        '''
        self.db = MySQLdb.connect(host=hostname, port = portnumber, \
                user=username, passwd=password, db=dbname)

    # create the Samdb database
    def CreateDatabase(self, dbname):
        try:
            cursor = self.db.cursor()
        except MySQLdb.Error, e:
            print "Samdb.CreateDatabase: Error %d: %s" % \
                    (e.args[0], e.args[1])
            sys.exit (1)
        except MySQLdb.Warning, e:
            print("Samdb.CreateDatabase: Warning: ", e)
        try:
            cursor.execute('DROP DATABASE IF EXISTS ' + dbname + ';')
        except MySQLdb.Error, e:
            print "Samdb.CreateDatabase: Error %d: %s" % \
                    (e.args[0], e.args[1])
            sys.exit (1)
        except MySQLdb.Warning, e:
            print("Samdb.CreateDatabase: Warning: ", e)
        try:
            cursor.execute('CREATE DATABASE IF NOT EXISTS ' + \
                    dbname + ';')
        except MySQLdb.Error, e:
            print "Samdb.CreateDatabase: Error %d: %s" % \
                    (e.args[0], e.args[1])
            sys.exit (1)
        except MySQLdb.Warning, e:
            print("Samdb.CreateDatabase: Warning: ", e)
        try:
            cursor.execute('USE ' + dbname + ';')
        except MySQLdb.Error, e:
            print "Samdb.CreateDatabase: Error %d: %s" % \
                    (e.args[0], e.args[1])
            sys.exit (1)
        except MySQLdb.Warning, e:
            print("Samdb.CreateDatabase: Warning: ", e)
            
    # drop the Samdb database
    def DropDatabase(self, dbname):
        try:
            cursor = self.db.cursor()
            cursor.execute('DROP DATABASE ' + dbname + ';')
        except MySQLdb.Error, e:
            print "Samdb.DropDatabase: Error %d: %s" % (e.args[0], e.args[1])
            sys.exit (1)
            
    # Use a database
    def UseDatabase(self, dbname):
        try:
            cursor = self.db.cursor()
            cursor.execute('USE ' + dbname + ';')
        except MySQLdb.Error, e:
            print "Samdb.DropDatabase: Error %d: %s" % (e.args[0], e.args[1])
            sys.exit (1)
        except MySQLdb.Warning, e:
            print("Samdb.DropDatabase: Warning: ", e)
            
    # create a table
    def CreateTable(self, tableName, rows, primaryKey):
        try:
            cursor = self.db.cursor()
            cursor.execute("CREATE TABLE IF NOT EXISTS " + tableName +
                                rows + ";")
            self.db.commit()
        except MySQLdb.Error, e:
            print "Samdb.CreateTable: Error %d: %s" % (e.args[0], e.args[1])
            sys.exit (1)
        except MySQLdb.Warning, e:
            print("Samdb.CreateTable: Warning: ", e)
        
    def FetchRows(self, query):
        # Exceptions are caught higher up
        cursor = self.db.cursor()
        cursor.execute(query)
        rows = cursor.fetchall()
        self.db.commit()
        return rows

    def FetchRow(self, query):
        cursor = self.db.cursor()
        cursor.execute(query)
        row = cursor.fetchone()
        self.db.commit()
        return row
                      
    def ExecuteQuery(self, query):
        try:
            cursor = self.db.cursor()
            cursor.execute(query)
            self.db.commit()
        except MySQLdb.Error, e:
            print "Samdb.ExecuteQuery: Error %d: %s" % (e.args[0], e.args[1])
            sys.exit (1)
        except MySQLdb.Warning, e:
            print("Samdb.ExecuteQuery: Warning: ", e)
            
        '''   
        try:
            cursor.execute("ALTER TABLE " + tableName + \
                            " ADD PRIMARY KEY (" + primaryKey + ");")
        except MySQLdb.Error, e:
            print "Error %d: %s" % (e.args[0], e.args[1])
            sys.exit (1)
        except MySQLdb.Warning, e:
            print("Warning: ", e)
        '''
        
    def AddForeignKey(self, localTable, localField, foreignTable, foreignField):
        try:
            cursor = self.db.cursor()
            cursor.execute("ALTER TABLE " + localTable \
                            + " ADD CONSTRAINT FOREIGN KEY (" \
                            + localField + ") REFERENCES " \
                            + foreignTable + " (" + foreignField + ");")
            self.db.commit()
        except MySQLdb.Error, e:
            print "Samdb.AddForeignKey: Error %d: %s" % (e.args[0], e.args[1])
            sys.exit (1)
        except MySQLdb.Warning, e:
            print("Samdb.AddForeignKey: Warning: ", e)
      
    def InsertRow(self, tableName, fields, values):
        '''
        cursor = self.db.cursor()
        cursor.execute("INSERT INTO " + tableName + "(" + fields + ")" + \
                            " VALUES (" + values + " );")
        '''
        self.cursor = self.db.cursor()
        self.cursor.execute("INSERT INTO " + tableName + "(" + fields + ")" + \
                            " VALUES (" + values + " );")
        self.db.commit()
        
    def DeleteRow(self, tableName, fieldName, value):
        cursor = self.db.cursor()
        cursor.execute("DELETE FROM " + tableName + " WHERE " + \
                       fieldName  + " = " + value)
        self.db.commit()
    
# Run the program
if __name__ == '__main__':
    if len(sys.argv) < 2:
        print 'Usage: python dbservices.py dbname'
    else:
        try:
            db = Samdb(dbname='mysql')
            dbname = sys.argv[1]
            print('Now create ' + dbname + ';')
            samdb = db.CreateDatabase(dbname)
            print(dbname + ' created.')
        except MySQLdb.Error, e:
            print "Samdb.main: Error %d: %s" % (e.args[0], e.args[1])
            sys.exit (1)
        except MySQLdb.Warning, e:
            print("Samdb.main: Warning: ", e)
    


    
