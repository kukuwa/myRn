# uncompyle6 version 3.2.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.5 |Anaconda, Inc.| (default, Mar 29 2018, 13:32:41) [MSC v.1900 64 bit (AMD64)]
# Embedded file name: CTSlib\MultiProcessHandle.py
# Compiled at: 2018-05-31 17:21:58
# Size of source mod 2**32: 637 bytes
"""
Created on 2018年4月25日

@author: Administrator
"""
from multiprocessing.pool import ThreadPool

class OrderNewHandle:
    """
    多线程报单
    """

    def __init__(self, multiProcessCnt):
        self.multiProcessCnt = multiProcessCnt
        self.initReadProcess()

    def order(self, orderNew, orderInfo):
        return self.pool.apply(orderNew, (orderInfo, False))

    def initReadProcess(self):
        self.pool = ThreadPool(processes=self.multiProcessCnt)

    def destroy(self):
        self.pool.close()
        self.pool.join()
# okay decompiling MultiProcessHandle.pyc
