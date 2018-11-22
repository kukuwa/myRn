# uncompyle6 version 3.2.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.5 |Anaconda, Inc.| (default, Mar 29 2018, 13:32:41) [MSC v.1900 64 bit (AMD64)]
# Embedded file name: CTSlib\SysUtils.py
# Compiled at: 2018-05-31 13:18:11
# Size of source mod 2**32: 2563 bytes
"""
    提供系统工具类   

"""
from _ast import Str
__author__ = 'GuiPei <guipei@croot.com>'
__status__ = 'production'
__version__ = '1.01'
__date__ = '2017-03-10'
import threading, types
encode = 'utf-8'

class Borg(object):
    _state = {}

    def __new__(cls, *args, **kw):
        ob = super(Borg, cls).__new__(cls, *args, **kw)
        ob.__dict__ = cls._state
        return ob


lock = threading.Lock()

class SequenceManager(Borg):
    num = 10000000

    def getNextId(self):
        if lock.acquire():
            self.num = self.num + 1
            lock.release()
            return self.num


def checkValid(obj):
    """
    判断变量是否为空
    """
    if obj != None:
        if obj != '':
            return True
        return False


def strEncodeConvert(msg):
    t = type(msg)
    if t == bytes:
        msg = msg.decode(encode)
    return msg


def printObject(theObject, msg=None):
    """
    打印输出对象
    """
    if not checkValid(theObject):
        return
    if msg != None:
        printString(msg)
    if type(theObject) == str:
        printString(theObject)
    else:
        if type(theObject) == list:
            for item in theObject:
                printObject(item)
                print('\n')

        else:
            for key, value in vars(theObject).items():
                printString('   .%s=%s ', (key, value))


def printMutiObject(theObject, msg=None):
    """
    打印输出对象
    """
    if not checkValid(theObject):
        return
    if msg != None:
        printString(msg)
    for key, value in vars(theObject).items():
        printString(' .%s= ', key)
        if type(value) == list:
            for item in value:
                printObject(item)
                printObject('\n')

        else:
            printObject(value)
            printObject('\n')


def printString(key, value=None):
    """
    字符串打印，将字符进行编码后打印。
    """
    if not checkValid(value):
        print(strEncodeConvert(key))
    else:
        print(strEncodeConvert(key) % strEncodeConvert(value))
# okay decompiling SysUtils.pyc
