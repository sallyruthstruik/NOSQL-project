#-*- coding: cp1251 -*-
from classes.FileSystem import *
import MySQLdb as sql
from classes.helpers import Timer

#database = sql.connection("127.0.0.1", "root", "1379468250", "Files")
#cursor = database.cursor()

def getchanges(gen1, gen2):
    """Возвращает изменения между файлами в итераторе gen1(удален/добавлен). 
    
    gen1 и gen2 - итераторы, возвращающие absolute_path"""
    
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
                print h1, "удален"
                h1 = gen1.next()
            elif func == __gt__:
                print h2, "добавлен"
                h2 = gen2.next()
            else:
                raise ValueError("bad function")
        return [h1, h2]
    
    
    while True:
        head1, head2 = skip()
        head1, head2 = skip(__lt__)
        head1, head2 = skip(__gt__)

def FSinsert(path = ROOT_SNAPSHOT_FOLDER):
    """Для каждого файла пишет его в базу"""
    for x in os.listdir(path):
        cur_path = os.path.join(path, x)
        collection_test.insert({"path": cur_path})
        if getType(cur_path) == "folder":
            try:
                FSinsert(cur_path)
            except:
                pass
                
def FSgenerator(path = ROOT_SNAPSHOT_FOLDER):
    """Генератор файлов из файловой системы"""
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
    """Пишет пары путь-хэш в базу данных"""
    for x in FSgenerator(path):
        try:
            collection_temp.insert({"path":x, "hash": File(x).getHash()})
        except:
            pass
        
def getHashedFilesGenerator():
    """Возвращает словарь путь, хэш в порядке, обратном отсортированному"""
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

class TestFile(File):
    def __init__(self, path, hash):
        File.__init__(self, path)
        self.hash = hash
        self.path_len = len(self.absolute_path.split("\\"))
        
    def insertIntoDatabase(self):
        self._id = collection_test.insert(self.__dict__)

    
      
getFilesHashes()
for x in getHashedFilesGenerator():
    TestFile(x["path"], x["hash"]).insertIntoDatabase()
    
    
        


    



        

    
    
    
    
    
