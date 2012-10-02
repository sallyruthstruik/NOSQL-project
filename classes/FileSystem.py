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

class File:
    def __init__(self):
        self.__dict__ = {    #Все поля файла по умолчанию
            "_id": None,
            "absolute_path":None,
            "name": None,
            'type': None,
            'size': None,
            "modification_time": None,
            "last_access_time": None,
            "path_len": None,
            "versions":[]
                }
        
    bad_items = (   #Поля, которые НЕ НАДО вносить в базу
            "_id",
            "version"
                 )
    non_checked_items = (   #Поля, которые не надо сравнивать
            "versions",    
                         )
    changing_items = (      #Поля, которые могут меняться в процессе жизни файла
            "size",
            "modification_time",
                      )

    def __eq__(self, file):
        """Сравнивает левый файл с правым и выдает поля правого, которые не равны левому"""
        returning = {}
        for x in file.__dict__.keys():
            if x not in self.non_checked_items:
                if x not in self.__dict__.keys():
                    returning[x] = file.__dict__[x]
                elif self.__dict__[x] != file.__dict__[x]:
                    returning[x] = file.__dict__[x]
        return returning
                
    def __str__(self):
        return self.absolute_path +" "+ self.name+ " "

class FileInDatabase(File):
    def __init__(self, full_path):
        files = list(collection_files.find({"absolute_path": ToUnicode(full_path)}))
        if len(files) == 0:
            raise ValueError("File with path "+full_path+" not in db")
        if len(files)>1:
            raise ValueError("Error in database: two row with one ObjectID")
        if len(files) == 1:
            self._id = files[0]["_id"]
            for x in files[0].keys():
                self.__dict__[x] = files[0][x]


class FileInFS(File):
    def __init__(self, full_path, version_id):
        File.__init__(self)
        self.version = version_id
        self.versions.append(self.version)
        if True:
            self._id = None
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
        
    
    def insertIntoDatabase(self):
        try:
            database_file = FileInDatabase(self.absolute_path)
        except ValueError:
            toInsert = {}
            toChange = {}
            for x in self.__dict__.keys():
                if x in self.bad_items:
                    continue
                else:
                    toInsert[x] = self.__dict__[x]
            collection_files.insert(toInsert, safe = True)
        else:
            differents = (database_file == self)
            for x in self.bad_items:
                del differents[x]
            print differents
            #diff_id = collection_differents.insert(differents, safe = True)
            if differents!={}:
                collection_files.update(
                                {"absolute_path": database_file.absolute_path},
                                {"$push":
                                    {"versions": self.version},
                                 "$push":
                                    {"changes":
                                        {"version": self.version,
                                         "changes": differents}
                                    }
                                 })
            else:
                collection_files.update(
                                {"absolute_path": database_file.absolute_path},
                                {"$push":
                                    {"versions":self.version}
                                 })




#generator = collection_files.getPathCursor() 
fd = open("test", 'w')





class FolderInFS(FileInFS):
    def __init__(self, path, version_id):
        if not os.path.isdir(path):
            raise ValueError("not folder")
        FileInFS.__init__(self, path, version_id)
    
    
    def Run(self):
        if Get("count_files_cur")%PRINTING_INTERVAL == 0 or True:
            print "Now "+str(Get("count_files_cur")) + " from "+str(Get("count_files"))
        files =[]
        folders = []
        for item in os.listdir(self.absolute_path):
            new_path = os.path.join(self.absolute_path,item)
            if getType(new_path) == 'folder':
                try:
                    folders.append(FolderInFS(new_path, self.version))
                except ValueError:
                    pass
            else:
                try:
                    files.append(FileInFS(new_path, self.version))
                except ValueError:
                    pass
            Inc("count_files_cur")

        for item in files+folders:
            item.insertIntoDatabase()

        for item in folders:
            try:
                item.Run()
            except:
                pass
            
    def childCount(self):
        for item in os.listdir(self.absolute_path):
            new_path = os.path.join(self.absolute_path, item)
            if getType(new_path) == 'folder':
                try:
                    FolderInFS(new_path).childCount()
                except:
                    pass
                
            Inc("count_files")
        self.child_count = Get("count_files")
    
class Version:
    def __init__(self):
        
        self.name = raw_input("Enter the name of FV")
        self.date = datetime.datetime.now()
        self._id = collection_versions.insert(self.__dict__)
        
    def compareVersion(self, folder = ROOT_SNAPSHOT_FOLDER):
        FolderInFS(folder, self._id).Run()
        

    