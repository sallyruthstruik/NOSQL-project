#!/usr/bin/python
#-*- coding: cp1251 -*-
from classes.FileSystem import *



if False:
    x1 = File("/home/stas/workspace")
    x2 = File("/home/stas/workspace", True)
    print x1.__dict__
    print x2.__dict__
    print x1, x2
if False:
    file = FolderInFS(ROOT_SNAPSHOT_FOLDER)
    print "Getting count files..."
    file.childCount()
    print "Getted!\n"
    start = time.time()
    file.Run()
    print str(time.time() - start)
    print Get('count_files_cur')

if False:
    collection_files.drop()
    collection_versions.drop()

Version().compareVersion()
#print "Привет!"
#Folder(ROOT_SNAPSHOT_FOLDER).Run()
