#!/usr/bin/python
#-*- coding: utf-8 -*-
from classes.FileSystem import *

if True:
    file = Folder(ROOT_SNAPSHOT_FOLDER)
    print "Getting count files..."
    file.childCount()
    print "Getted!\n"
    start = time.time()
    file.Run()
    print str(time.time() - start)
    print Get('count_files_cur')

#print "Привет!"
#Folder(ROOT_SNAPSHOT_FOLDER).Run()
