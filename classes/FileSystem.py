#!/usr/bin/python
#-*- coding: utf-8 -*-
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
    return len(path.split("/"))

def timeFromSeconds(t):
    return t

class File:
    color = "white"
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
            self.modification_time = os.path.getmtime(full_path)
            self.last_access_time = os.path.getatime(full_path)
        else:
            raise ValueError("path is bad")
    
    def insertIntoDatabase(self):
        collection_files.insert({"name": self.name,
                                 "path": self.absolute_path,
                                 "path_len": getPathLen(self.absolute_path),
                                 "type": self.type,
                                 "size": self.size,
                                 "mtime": self.modification_time,
                                 "latime": self.last_access_time})
    
    def __str__(self):
        return self.absolute_path +" "+ self.name+ " "


#generator = collection_files.getPathCursor() 
fd = open("test", 'w')
class Folder(File):
    def __init__(self, path):
        if not os.path.isdir(path):
            raise ValueError("not folder")
        File.__init__(self, path)
    
    
    def Run(self):
        if Get("count_files_cur")%100 == 0 or True:
            print "Now "+str(Get("count_files_cur")) + " from "+str(Get("count_files"))
        files =[]
        folders = []
        for item in os.listdir(self.absolute_path):
            new_path = self.absolute_path + '/' + item
            if getType(new_path) == 'folder':
                try:
                    folders.append(Folder(new_path))
                except ValueError:
                    pass
            else:
                try:
                    files.append(File(new_path))
                except ValueError:
                    pass
            Inc("count_files_cur")
        
#        next_object = generator.next()
#        
#        if (getPathLen(self.absolute_path)+1) != getPathLen(next_object):
#            raise ValueError("Error in generator: length isn`t the same")
#        
#
#        while str(next_object).find(self.absolute_path) != -1 and ((getPathLen(self.absolute_path)+1)==getPathLen(next_object)):
#            print>>fd, "\nIm in " + self.absolute_path + "\nCheck " + next_object+"\n"
#            for item in files+folders:
#                print>>fd, "\tCheck in folder"+item.absolute_path
#                label = False
#                if str(item.absolute_path) == str(next_object):
#                    item.color = 'black'
#                    label = True
#                    break
#            if not label:
#                print>>fd, next_object + " deleted"
#                
#            next_object = generator.next()
#        
#        for item in files+folders:
#            if item.color == "white":
#                print>>fd, str(item) + " added"
            


        for item in files+folders:
            item.insertIntoDatabase()

        for item in folders:
            try:
                item.Run()
            except:
                pass
            
    def childCount(self):
        for item in os.listdir(self.absolute_path):
            new_path = self.absolute_path + '/' + item
            if getType(new_path) == 'folder':
                try:
                    Folder(new_path).childCount()
                except:
                    pass
                
            Inc("count_files")
        self.child_count = Get("count_files")
    
    
    
    
    
    
    