# -*- coding: utf-8 -*-
# @Time    : 2020/2/7 下午5:37
# @Author  : zhihuiyuan
# @Email   : yzh@commasmart.com
# @File    : my_dest.py
# @Software: PyCharm

class RevealAccess(object):
    """A data descriptor that sets and returns values
       normally and prints a message logging their access.
    """

    def __init__(self, initval=None, name='var'):
        self.val = initval
        self.name = name

    def __get__(self, obj, objtype):
        print('Retrieving', self.name)
        print("the type is {},and the obj is {}".format(objtype,obj))
        return self.val

    def __set__(self, obj, val):
        print('Updating', self.name)
        self.val = val

class MyClass(object):
     x = RevealAccess(10, 'var "x"')
     y = 5
     def __init__(self, testt):
         self.x = testt

m = MyClass('122')
m.x

