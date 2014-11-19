'''
Created on Aug 24, 2010

@author: bob
'''

class ChooserLists(object):
    '''
    classdocs
    '''

    def __init__(self):
        return
        
    def BuildChooserNumberList(self, player, samdb):
        print("AAAAAAA Entering BuildChooserNumberList with player = ", player)
        if player == 'donor':
            query = "SELECT donor_number FROM Donors ORDER BY donor_number;"
        elif player == 'item':
            query = 'SELECT item_number FROM Items ORDER by item_number;'
        elif player == 'buyer':
            query = 'SELECT buyer_number FROM Buyers ORDER by buyer_number;'
        elif player == 'purchase':
            query = "SELECT item_Number FROM Items \
                        WHERE item_purchasedby IS NOT NULL \
                        AND item_salesprice IS NOT NULL \
                        ORDER BY item_number;"
        else:
            print "Chooser.BuildChooserNumberList received bad player name"
            return
        rows = samdb.FetchRows(query)
        listToReturn = []
        for row in rows:
            listToReturn.append(row[0])
        return listToReturn
    
    def BuildChooserNumberAndInfoList(self, player, samdb):
        if player == 'donor':
            query = "SELECT donor_number, donor_name FROM Donors \
                        ORDER BY donor_name;"
        elif player == 'item':
            query = "SELECT item_number, item_description FROM Items \
                        ORDER BY item_description;"      
        elif player == 'buyer':
            query = "SELECT buyer_number, buyer_last FROM Buyers \
                        ORDER BY buyer_last;" 
        elif player == 'purchase':
            query = "SELECT item_Number, item_description FROM Items \
                        WHERE item_purchasedby IS NOT NULL \
                        AND item_salesprice IS NOT NULL \
                        ORDER BY item_description;"  
        else:
            print "Choosers.BuildChooserNumberList received bad player name"
            return
        rows = samdb.FetchRows(query)
        listToReturn = []
        for row in rows:
            listToReturn.append(row[0] + ' ' + row[1])
        return listToReturn
        