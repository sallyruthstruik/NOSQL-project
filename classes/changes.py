#-*- coding: cp1251 -*-
from classes.FileSystem import *
import MySQLdb as sql
from classes.helpers import Timer

#database = sql.connection("127.0.0.1", "root", "1379468250", "Files")
#cursor = database.cursor()

def getchanges(gen1, gen2):
    """���������� ��������� ����� ������� � ��������� gen1(������/��������). 
    
    gen1 � gen2 - ���������, ������������ absolute_path"""
    
    head1, head2 = (gen1.next(), gen2.next())

    def __eq__(x1, x2):
        return x1 == x2
    def __lt__(x1, x2):
        return x1 < x2
    def __gt__(x1, x2):
        return x1 > x2

    def skip(func = __eq__):
        h1 = head1
        h2 = head2
        while func(h1, h2):
            if func == __eq__:
                h1, h2 = (gen1.next(), gen2.next())
            elif func == __lt__:
                print h1, "������"
                h1 = gen1.next()
            elif func == __gt__:
                print h2, "��������"
                h2 = gen2.next()
            else:
                raise ValueError("bad function")
        return [h1, h2]
    
    
    while True:
        head1, head2 = skip()
        head1, head2 = skip(__lt__)
        head1, head2 = skip(__gt__)

def FSinsert(path = ROOT_SNAPSHOT_FOLDER):
    for x in os.listdir(path):
        cur_path = os.path.join(path, x)
        collection_test.insert({"path": cur_path})
        if getType(cur_path) == "folder":
            try:
                FSinsert(cur_path)
            except:
                pass
                
def FSgenerator(path = ROOT_SNAPSHOT_FOLDER):
    for x in os.listdir(path):
        cur_path = os.path.join(path, x)
        yield cur_path
        if getType(cur_path) == "folder":
            try:
                for x in FSgenerator(cur_path):
                    yield x
            except:
                print "Error in", path

with open("test.txt", "w"):
    pass

def getFilesHashesShell(f):
    def _inside(path = ROOT_SNAPSHOT_FOLDER):
        collection_temp.drop()
        collection_temp.ensure_index("path")
        f(path)
    return _inside

@getFilesHashesShell
def getFilesHashes(path = ROOT_SNAPSHOT_FOLDER):
    """����� ���� ����-��� � ���� ������"""
    for x in FSgenerator(path):
        try:
            file = File(x)
            collection_temp.insert({"path":file.absolute_path, "hash": file.hash})
        except:
            pass
        
def getHashedFilesGenerator():
    """���������� ���� ���� - ��� � �������, �������� ����������������"""
    if collection_temp.count() == 0:
        getFilesHashes()
    generator = collection_temp.find().sort("path", -1)
    hashsumm = 0
    for x in generator:
        hash = x["hash"]
        if hash:
            hashsumm=(hashsumm + hash)%HASH_INT_LENGTH
            yield x
        else:
            hash = hashsumm
            hashsumm = 0
            x["hash"] = hash
            yield x
    collection_temp.drop()



        

    
    
    
    
    
