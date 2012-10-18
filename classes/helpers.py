#!/usr/bin/python
#-*- coding: utf-8 -*-
import time
import threading as th
import random as ran


def Ecran(string):
    string = string.replace("'", r"\'").replace('"', r'\"').replace("\n", '')
    return string

def Timer(f):
    #Декоратор, первой переменной возвращает ответ функции, второй - время ее работы
    def _inside(*a, **kw):
        start = time.time()
        x = f(*a, **kw)
        t = str(time.time()-start)
        print "Working "+t
        return [x, t]
    return _inside

def Threading(f):
    def inside(*args, **kwargs):
        thread = th.Thread(target = f, args = args, kwargs = kwargs)
        thread.start()
        return thread
    return inside

def getRandomElement(arr, delete = False):
    index = ran.randrange(0, len(arr), 1)
    value = arr[index]
    if delete:
        arr.remove(value)
    return value

def tester(f, args, printing):
    """Тестер функций. Записывает в файл время ее работы и полученные данные. Принимает на вход функцию, и массив из 
        [[args1,kwargs1], ...] для нее.
        Функция printing отвечает за то, как вносить полученные тестовые значения в файл. Printing получает значения
        [f(args, kwargs), time] и возвращает строку, которая будет записана"""
    if True:
        i=0
        with open("tests", "w"):
            pass
        for x in args:
            i+=1
            print "Test "+str(i) +" from "+str(len(args))
            resp = Timer(f)(*x[0], **x[1])
            with open("tests", 'a') as fd:
                print >> fd, printing(resp)
    
