#!/usr/bin/python
#-*- coding: cp1251 -*-
import pymongo as pm
from classes.config import *
from random import randrange

try:
    connection = pm.Connection()
    database = pm.database.Database(connection, DATABASE_NAME)
except:
    print "Запустите сервер MongoDB"

def ToUnicode(string):
    x = string.decode("cp1251")
    return x.encode("utf-8")


class MyCollection(pm.collection.Collection):
    def __init__(self, *args, **kwargs):
        pm.collection.Collection.__init__(self, *args, **kwargs)
    
    def getPathCursor(self):
        for x in self.find(fields = ["path"]).sort("path_len"):
            yield x["path"]
            
    def insert(self, data, *a, **k):
        if type(data) == dict:
            out = {}
            for key in data.keys():
                if type(data[key]) == str:
                    out[key] = ToUnicode(data[key])
                else:
                    out[key] = data[key]
        return pm.collection.Collection.insert(self, out, safe = True, *a, **k)
            
        

try:
    collection_files = MyCollection(database, COLLECTION_NAME_FILES)
    collection_versions = MyCollection(database, COLLECTION_NAME_VERSIONS)
    collection_differents = MyCollection(database, COLLECTION_NAME_DIFFERENTS)
    collection_temp = MyCollection(database, "temp")
    collection_test = MyCollection(database, "test")
except:
    pass