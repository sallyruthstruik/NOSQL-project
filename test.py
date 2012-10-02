#-*-coding: cp1251 -*-

from classes.Connection import *


def toCp1251(string):
    string = str(string)
    x = string.decode("utf-8")
    print x
    return x.encode("cp1251")

if False:
    for x in collection_versions.find():
        for y in x.keys():
            print x[y]
