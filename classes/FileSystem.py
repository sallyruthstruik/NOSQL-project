#!/usr/bin/python
#-*- coding: cp1251 -*-
import os
import datetime
import time
from classes.Connection import *
from classes.globals import *

def getType(s):
    
    if os.path.islink(s):
        return "link"
    elif os.path.ismount(s):
        return "mount"
    elif os.path.isdir(s):
        return "folder"
    elif os.path.isfile(s):
        return "file"
    else:
        return "unexpected"
    
def getPathLen(path):
    return None
    i=0
    while True:
        x = os.path.split(path)
        i+=1
        if x[0] == '':
            break
    return i

def timeFromSeconds(t):
    return datetime.datetime(*time.localtime(t)[:6])
                        
import hashlib as hash
      
class File:
    def __init__(self, full_path):
        if os.path.exists(full_path):
            if len(full_path)>1 and full_path[-1] == '/':
                full_path = full_path[:-1]
            self.absolute_path = full_path
            
            if os.path.split(full_path)[1] == '':
                self.name = 'root'
            else:
                self.name = os.path.split(full_path)[1]
            self.type = getType(full_path)
            self.size = os.path.getsize(full_path)
            self.modification_time = timeFromSeconds(os.path.getmtime(full_path))
            self.last_access_time = timeFromSeconds(os.path.getatime(full_path))
        else:
            raise ValueError("path is bad")
        self.path_len = getPathLen(self.absolute_path)
        self.hash = self.getHash()
        
    def getHash(self):
        """Возвращает хэш от атрибутов файла"""
        if self.type == "file":
            x = hash.md5(str(self.modification_time))
            return int(x.hexdigest(), 16)
        else:
            return None      
            
        
    
    def insertIntoDatabase(self):
        pass


        

    