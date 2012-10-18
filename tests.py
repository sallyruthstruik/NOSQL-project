from classes.helpers import *
from MySQLdb import *
import pymongo as pm
from random import randrange

with open("test", "w"):
    pass

TRANSACTION_INSERT_COUNT = 10000

class MongoDB:
    def __init__(self):
        self.conn = pm.connection.Connection()
        self.db = pm.database.Database(self.conn, "test")
        self.coll = pm.collection.Collection(self.db, "time_test")
        
    def insertIntoDatabase(self, val):
        self.coll.insert({"value": val})
    
    def clear(self):
        self.coll.drop()
        

class MySQL:
    def __init__(self):
        self.db = Connection("127.0.0.1", "root", "1379468250", "Files")
        self.cursor = self.db.cursor()
        self.count = 0
    
    def insertIntoDatabase(self, val, TRANSACTION_INSERT_COUNT = TRANSACTION_INSERT_COUNT):
        self.count+=1
        self.cursor.execute("INSERT INTO fortest VALUES(NULL, '%s');"%
                            (val))
        if self.count%TRANSACTION_INSERT_COUNT == 0:
            self.db.commit()
            
    def clear(self):
        self.cursor.execute("DELETE FROM fortest;")

db = MySQL()
def testDatabaseInsert(n):
    count = 0
    max_d=n
    data = [hex(randrange(10**100, 10**101)) for x in range(10**max_d)]
    start = time.time()
    for x in data:
        db.insertIntoDatabase(x)
        count+=1
        if count%1000 == 0:
            print "inserted", count
            with open("test", "a") as fd:
                print >> fd, str(count)+";", int(time.time()-start)
        
for i in range(1,9):
    start = time.time()
    db.cursor.execute("SELECT * from fortest_select_%s WHERE path = ''")