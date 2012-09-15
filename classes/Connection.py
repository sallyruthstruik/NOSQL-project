#!/usr/bin/python
#-*- coding: utf-8 -*-
import pymongo as pm
from classes.config import *

connection = pm.Connection()
database = pm.database.Database(connection, DATABASE_NAME)

class MyCollection(pm.collection.Collection):
    def __init__(self, *args, **kwargs):
        pm.collection.Collection.__init__(self, *args, **kwargs)
    
    def getPathCursor(self):
        for x in self.find(fields = ["path"]).sort("path_len"):
            yield x["path"]
        

        
collection_files = MyCollection(database, COLLECTION_NAME_FILES)