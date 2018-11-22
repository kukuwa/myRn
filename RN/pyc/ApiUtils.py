# uncompyle6 version 3.2.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.5 |Anaconda, Inc.| (default, Mar 29 2018, 13:32:41) [MSC v.1900 64 bit (AMD64)]
# Embedded file name: CTSlib\ApiUtils.py
# Compiled at: 2018-07-17 16:51:55
# Size of source mod 2**32: 40902 bytes
"""
Python API 服务
提供行情、交易功能
"""
import json
from socket import error as socketError
from socket import *
from CTSlib.ApiStruct import *
from CTSlib import Logger
from CTSlib.Encryptor import encrypt
import CTSlib, os, sys, traceback
_pythonMajorVersion = sys.version_info[0]
_pythonMinorVersion = sys.version_info[1]
if _pythonMajorVersion == 3:
    if _pythonMinorVersion == 6:
        from idlelib.iomenu import encoding

class MsgTypeList(object):
    """
    定义请求功能消息
    
    * 10000 : 系统连接服务
    * 10001 : 系统连接关闭
    * 10011 : 账户登录
    * 10021 : 柜员登录
    * 11001 : 证券信息查询
    * 11003 : 期货合约基本信息查询
    * 15001 : 报单功能
    * 15002 : 撤单功能
    * 16001 : 账户查询
    * 11002 : 行情数据订阅
    * 17001 : 行情订阅
    * 10012 : 账户订阅服务
    * 17002 : 成交订阅
    * 16006 : 持仓查询
    * 16011 : 报单查询
    * 16012 : 成交查询
    * 16002 : 期货期权资金账户查询
    * 21001 : 创建指令
    * 21002 : 查询指令列表
    * 21003 : 查询指令明细
    * 21004 : 指令暂停中止恢复
    * 21011 : 查询指令报单明细
    * 21012 : 查询指令报单汇总
    * 21016 : 查询指令成交明细
    * 23001 : 算法策略下单
    * 23002 : 算法策略撤单
    * 23003 : 算法强制撤单
    * 23006 : 算法策略查询
    * 23011 : 算法报单明细查询
    * 23012 : 算法报单汇总查询
    * 23016 : 算法成交明细查询
    * 18001 : 查询现货历史交易日志
    * 18002 : 查询期货历史交易日志
    * 18003 : 查询未到期回购
    """
    MSG_TYPE_SYS_CONNECT = 10000
    MSG_TYPE_SYS_DISCONNECT = 10001
    MSG_TYPE_ACCT_LOGIN = 10011
    MSG_TYPE_OPT_LOGIN = 10021
    MSG_TYPE_QRY_STKINFO = 11001
    MSG_TYPE_QRY_FUTURE = 11003
    MSG_TYPE_ORDER_NEW = 15001
    MSG_TYPE_ORDER_CANCEL = 15002
    MSG_TYPE_QRY_ACCOUNT = 16001
    MSG_TYPE_FUTURE_ACCOUNT = 16002
    MSG_TYPE_SUB_QUOTE_RESP = 11002
    MSG_TYPE_SUB_QUOTE_RETURN = 17001
    MSG_TYPE_SUB_TRADE_RESP = 10012
    MSG_TYPE_SUB_TRADE_RETURN = 17002
    MSG_TYPE_QRY_POSITION = 16006
    MSG_TYPE_QRY_ORDER = 16011
    MSG_TYPE_QRY_KNOCK = 16012
    MSG_TYPE_CREATE_INST = 21001
    MSG_TYPE_QRY_INSTLIST = 21002
    MSG_TYPE_QRY_INSTINFO = 21003
    MSG_TYPE_HANDLE_INST = 21004
    MSG_TYPE_QRY_INST_DETAILORDER = 21011
    MSG_TYPE_QRY_INST_SUMORDER = 21012
    MSG_TYPE_QRY_INST_DETAILKNOCK = 21016
    MSG_TYPE_ALGO_ORDER = 23001
    MSG_TYPE_ALGO_WITHDRAW = 23002
    MSG_TYPE_ALGO_FORCEWITHDRAW = 23003
    MSG_TYPE_ALGO_QRY_STRATEGY = 23006
    MSG_TYPE_ALGO_QRY_DETAILORDER = 23011
    MSG_TYPE_ALGO_QRY_SUMORDER = 23012
    MSG_TYPE_ALGO_QRY_DETAILKNOCK = 23016
    MSG_TYPE_EXTEND_STK_TRADINGLOG = 18001
    MSG_TYPE_EXTEND_FUT_TRADINGLOG = 18002
    MSG_TYPE_EXTEND_UNDUE_REPURCHASE = 18003


class ErrTypeList(object):
    """
    连接异常清单
    
    * A000001 : 连接服务器异常
    * A000002 : 服务器未连接
    * A000003 : 服务器已连接
    
    """
    EX_CONNECT_ERROR = ('A000001', '连接服务器异常')
    EX_CONNECT_NONE = ('A000002', '服务器未连接')
    EX_CONNECT_REPEAT = ('A000003', '服务器已连接')


class ApiException(Exception):
    """
    接口异常类  
    
    """
    errorCode = 0
    errorMsg = ''

    def __init__(self, errorCode=0, errorMsg=''):
        self.errorCode = errorCode
        self.errorMsg = errorMsg

    def __str__(self, *args, **kwargs):
        return 'ApiException: errorCode=%s, errorMsg=%s' % (self.errorCode, self.errorMsg)


class CtsServer(object):
    """
    服务通讯类
    
    """
    BUFSIZE = 4096
    host = '127.0.0.1'
    port = 9880
    reqMap = {}
    callbackFuncMap = {}
    sessionId = '-1'
    passkey = ''
    connectionState = False
    t = None

    def checkError(self, dataValue):
        if dataValue.respond.successFlg != 0:
            ex = ApiException(dataValue.respond.errorCode, dataValue.respond.errorMsg)
            raise ex

    def addFunCallback(self, functionId, callbackFunction):
        """
        添加回调方法
        """
        self.callbackFuncMap[functionId] = callbackFunction

    def connect(self, host, port):
        """
        连接服务器
        
        :parameters: * host : IP地址
                     * port : 端口
        
        """
        try:
            self.host = host
            self.port = port
            if self.connectionState == True:
                ex = ApiException(*ErrTypeList.EX_CONNECT_REPEAT)
                raise ex
            addr = (host, port)
            Logger.debug('客户端版本号:%s' % CTSlib.__version__)
            Logger.debug('connect server:%s' % host)
            self.tcpCliSock = socket(AF_INET, SOCK_STREAM)
            self.tcpCliSock.setsockopt(IPPROTO_TCP, TCP_NODELAY, 1)
            self.tcpCliSock.settimeout(30)
            try:
                self.tcpCliSock.connect(addr)
            except:
                ex = ApiException(*ErrTypeList.EX_CONNECT_ERROR)
                raise ex

            self.tcpCliSock.settimeout(None)
            Logger.debug('before DispatchThread...')
            self.t = DispatchThread(self)
            Logger.debug('after DispatchThread...')
            self.t.start()
            self.connectionState = True
            msgHead = MsgHead(MsgTypeList.MSG_TYPE_SYS_CONNECT, self.sessionId)
            msgRequest = ParaTerminalInfo()
            msgData = MsgData(msgHead, msgRequest)
            reqDataValue = self.syncExchangeData(msgData, 30)
            reqData = reqDataValue.data
            self.passkey = str(reqData.passkey)
            del reqData.passkey
            Logger.info('连接成功')
            return reqData
        except ApiException as ex:
            raise ex
        except AttributeError as ex:
            Logger.error('连接超时... %s' % ex)
            self.disConnect()
            raise ex
        except Exception as ex:
            Logger.error('Connect error... %s' % ex)
            self.disConnect()
            raise ex

    def disConnect(self):
        """
        断开服务器连接
        调用此方法，关闭 socket连接，设置连接状态为 False，记录Info级别日志，结束子线程
        """
        if self.connectionState:
            msgHead = MsgHead(MsgTypeList.MSG_TYPE_SYS_DISCONNECT, self.sessionId)
            msgRequest = ParaTerminalInfo()
            msgData = MsgData(msgHead, msgRequest)
            reqDataValue = self.syncExchangeData(msgData)
            printObject(reqDataValue.data, '系统断开：')
            self.tcpCliSock.close()
            self.connectionState = False
        self.t.stop()

    def queryStkInfo(self, exchId, stkId, syncFlag=True):
        """
        行情查询
        
        :parameters: * exchId : 交易市场
                     * stkId : 证券代码
                     * syncFlag : 同步异步标志(默认为True)  True-同步 False-异步
        
        """
        msgHead = MsgHead(MsgTypeList.MSG_TYPE_QRY_STKINFO, self.sessionId)
        msgRequest = ParaStkInfo(exchId, stkId)
        msgData = MsgData(msgHead, msgRequest)
        if syncFlag == True:
            reqDataValue = self.syncExchangeData(msgData)
            return reqDataValue.data
        self.sendData(msgData)

    def accountLogin(self, acctId, password):
        """
        账户登录
        
        :parameters: * acctId : 账户代码
                     * password : 账户密码
        
        """
        msgHead = MsgHead(MsgTypeList.MSG_TYPE_ACCT_LOGIN, self.sessionId)
        password = encrypt2(password, self.passkey, self.connectionState)
        msgRequest = ParaAccount(acctId, password)
        msgData = MsgData(msgHead, msgRequest)
        reqDataValue = self.syncExchangeData(msgData)
        return reqDataValue.data

    def optLogin(self, optId, password):
        """
        柜员登录
        
        :parameters: * optId : 柜员代码
                     * password : 柜员密码
        """
        msgHead = MsgHead(MsgTypeList.MSG_TYPE_OPT_LOGIN, self.sessionId)
        password = encrypt2(password, self.passkey, self.connectionState)
        msgRequest = ParaOptLogin(optId, password)
        msgData = MsgData(msgHead, msgRequest)
        reqDataValue = self.syncExchangeData(msgData)
        return reqDataValue.data

    def orderNew(self, orderInfo, syncFlag=True):
        """
        报单功能
        
        :parameters: * orderInfo : 报单信息
                         * acctId : 资金帐号(必送)
                         * currencyId : 资金代码(期货期权必送)
                         * exchId : 交易市场(必送)
                         * stkId : 证券代码(必送)
                         * orderType : 委托类型(现货必送)
                         * orderPrice : 委托价格(必送)
                         * orderQty : 委托数量(必送)
                         * contractNum : 合同序号(可选)
                         * regId : 股东代码(可选,默认报单市场的第一个股东)
                         * batchNum : 委托批号(可选)
                         * clientId : 客户端编号(可选)
                         * f_offSetFlag : 开平标记（OPEN-开仓，CLOSE-平仓,FCLOSE-强平,CLOSETD-平今,CLOSEYD-平昨）(期货期权必送)
                         * bsFlag : 委托类型（B-多头，S-空头）(期货期权必送)
                         * f_orderPriceType : 价格类型（ANY-任意价，LIMIT-限价）(期货期权必送)
                         * f_hedgeFlag : 投保标记 (可选)
                         * coveredFlag : 备兑标签(可选)(0-非备兑,1-备兑)
                         * businessMark : 交易业务类型(可选)(OTO-期权订单，OTU-证券冻结与解冻，OTE-行权)
                     * syncFlag : 同步异步标志(默认为True) True-同步 False-异步
        """
        msgHead = MsgHead(MsgTypeList.MSG_TYPE_ORDER_NEW, self.sessionId)
        msgRequest = ParaOrderNew(orderInfo)
        msgData = MsgData(msgHead, msgRequest)
        if syncFlag == True:
            reqDataValue = self.syncExchangeData(msgData)
            return reqDataValue.data
        else:
            self.sendData(msgData)
            return msgHead

    @classmethod
    def orderNew2(cls, orderInfo):
        """
        异步报单功能，生成报单数据包
        orderInfo                    报单信息
        """
        msgHead = MsgHead(MsgTypeList.MSG_TYPE_ORDER_NEW)
        msgRequest = ParaOrderNew(orderInfo)
        msgData = MsgData(msgHead, msgRequest)
        return msgData

    def sendData2(self, data):
        """
        发送报单数据包
        """
        data.head.sessionId = self.sessionId
        self.sendData(data)

    def orderCancel(self, orderCancelInfo, syncFlag=True):
        """
        撤单功能
        
        :parameters: * orderCancelInfo : 撤单信息
                        * acctId : 资金帐号(必送)
                        * exchId : 交易市场(必送)
                        * contractNum : 合同序号(必送)
                     * syncFlag : 同步异步标志(默认为True) True-同步 False-异步
        
        """
        msgHead = MsgHead(MsgTypeList.MSG_TYPE_ORDER_CANCEL, self.sessionId)
        msgRequest = ParaOrderCancel(orderCancelInfo)
        msgData = MsgData(msgHead, msgRequest)
        if syncFlag == True:
            reqDataValue = self.syncExchangeData(msgData)
            return reqDataValue.data
        else:
            self.sendData(msgData)
            return msgHead

    def queryAccountInfo(self, acctId, currencyId='00', syncFlag=True):
        """
        资金账号查询
        
        :parameters: * acctId : 资金帐号(必送)
                     * currencyId : 币种代码(必送，默认为"00")
                     * syncFlag : 同步异步标志(默认为True)  True-同步 False-异步
        
        """
        msgHead = MsgHead(MsgTypeList.MSG_TYPE_QRY_ACCOUNT, self.sessionId)
        msgRequest = ParaAccontQuery(acctId, currencyId)
        msgData = MsgData(msgHead, msgRequest)
        if syncFlag == True:
            reqDataValue = self.syncExchangeData(msgData)
            return reqDataValue.data
        self.sendData(msgData)

    def subscriptQuota(self, stkList, subType=0):
        """
        行情订阅
        
        :parameters: * stkList : quotaList[]
                            * exchId : 市场
                            * stkId : 证券代码
                     * subType : 订阅类型(必送，默认为0) 0-订阅 1-退订
        """
        msgHead = MsgHead(MsgTypeList.MSG_TYPE_SUB_QUOTE_RESP, self.sessionId)
        msgRequest = ParaSubQuote(stkList, subType)
        msgData = MsgData(msgHead, msgRequest)
        self.sendData(msgData)

    def subscriptTrade(self, acctId, pwd, subType=0):
        """
        成交订阅
        
        :parameters: * acctId : 资金账号(必送)
                     * pwd : 交易密码(必送)
                     * subType : 订阅类型(必送，默认为0) 0-订阅 1-退订
        """
        msgHead = MsgHead(MsgTypeList.MSG_TYPE_SUB_TRADE_RESP, self.sessionId)
        pwd = encrypt2(pwd, self.passkey, self.connectionState)
        msgRequest = ParaSubscriptTrade(acctId, pwd, subType)
        msgData = MsgData(msgHead, msgRequest)
        self.sendData(msgData)

    def queryOrderList(self, queryCond, maxRowNum=100, pageNum=1, syncFlag=False):
        """
        报单查询
        
        :parameters: * queryCond : 查询条件
                         * acctId : 资金帐号(必送)
                         * exchId : 市场代码(可选)
                         * batchNum : 批号(可选)
                         * contractNum : 合同号(可选)
                         * stkId : 证券代码(可选)
                         * withdrawFlag : 撤单标志(可选, N-报单, Y-撤单)
                         * isCancellable : 是否可撤单标志(可选)
                         * beginTime : 起始时间(可选, hh:mm:ss)
                         * endTime : 结束时间(可选, hh:mm:ss)
                     * maxRowNum : 最大查询记录数量(可选，默认为100)
                     * pageNum : 查询页数(可选，默认为1)
                     * syncFlag : 同步异步标志(默认为True) True-同步 False-异步
        
        """
        queryType = 0
        if syncFlag == True:
            queryType = 1
        msgHead = MsgHead(MsgTypeList.MSG_TYPE_QRY_ORDER, self.sessionId)
        msgRequest = ParaQueryOrderInfo(queryCond, maxRowNum, pageNum, queryType)
        msgData = MsgData(msgHead, msgRequest)
        if syncFlag == True:
            reqDataValue = self.syncExchangeData(msgData)
            return reqDataValue.data
        else:
            self.sendData(msgData)
            return msgHead

    def queryFutureInfo(self, queryCond, maxRowNum=100, pageNum=1):
        """
        期货合约基本信息查询
        
        :parameters: * queryCond : 查询条件
                      * exchId : 市场(可选)
                      * f_productId : 品种(可选)
                  * maxRowNum : 最大查询记录数量(可选，默认为100)
                  * pageNum : 查询页数(可选，默认为1)
        
        """
        msgHead = MsgHead(MsgTypeList.MSG_TYPE_QRY_FUTURE, self.sessionId)
        msgRequest = ParaQueryFutureInfo(queryCond, maxRowNum, pageNum)
        msgData = MsgData(msgHead, msgRequest)
        reqDataValue = self.syncExchangeData(msgData)
        return reqDataValue.data

    def queryFutAcctInfo(self, acctId, currencyId='00'):
        """
        期货期权资金账户查询
        
        :parameters: * acctId : 资金帐号(必送)
                     * currencyId : 币种代码(必送，默认为"00")
        """
        msgHead = MsgHead(MsgTypeList.MSG_TYPE_FUTURE_ACCOUNT, self.sessionId)
        msgRequest = ParaQueryFutAcctInfo(acctId, currencyId)
        msgData = MsgData(msgHead, msgRequest)
        reqDataValue = self.syncExchangeData(msgData)
        return reqDataValue.data

    def queryKnockList(self, queryCond, maxRowNum=100, pageNum=1, syncFlag=False):
        """
        成交查询
        
        :parameters: * queryCond : 查询条件
                        * acctId : 资金帐号(必送)
                        * contractNum : 合同号(可选)
                        * stkId : 证券代码(可选)
                        * beginTime : 起始时间(可选, hh:mm:ss)
                        * endTime : 结束时间(可选, hh:mm:ss)
                     * maxRowNum : 最大查询记录数量(可选，默认为100)
                     * pageNum : 查询页数(可选，默认为1)
                     * syncFlag : 同步异步标志(默认为True) True-同步 False-异步
        
        """
        queryType = 0
        if syncFlag == True:
            queryType = 1
        msgHead = MsgHead(MsgTypeList.MSG_TYPE_QRY_KNOCK, self.sessionId)
        msgRequest = ParaQueryKnockInfo(queryCond, maxRowNum, pageNum, queryType)
        msgData = MsgData(msgHead, msgRequest)
        if syncFlag == True:
            reqDataValue = self.syncExchangeData(msgData)
            return reqDataValue.data
        else:
            self.sendData(msgData)
            return msgHead

    def queryPositionList(self, queryCond, maxRowNum=100, pageNum=1, syncFlag=False):
        """
        持仓查询
        
        :parameters: * queryCond : 查询条件
                        * acctId : 资金帐号(必送)
                        * exchId : 市场代码(可选)
                        * stkId : 证券代码(可选)
                        * regId : 股东代码(可选)
                        * bsFlag : 合约方向(期货，期权可选)(B-多头，S-空头)
                        * f_hedgeFlag : 投保标记(期货，期权可选)(HEDGE-套保，SPEC-投机)
                        * coveredFlag : 备兑标签(期货，期权可选)(0-备兑,1-非备兑)
                     * maxRowNum : 最大查询记录数量(可选，默认为100)
                     * pageNum : 查询页数(可选，默认为1)
                     * syncFlag : 同步异步标志(默认为True) True-同步 False-异步
        
        """
        queryType = 0
        if syncFlag == True:
            queryType = 1
        msgHead = MsgHead(MsgTypeList.MSG_TYPE_QRY_POSITION, self.sessionId)
        msgRequest = ParaQueryPositionInfo(queryCond, maxRowNum, pageNum, queryType)
        msgData = MsgData(msgHead, msgRequest)
        if syncFlag == True:
            reqDataValue = self.syncExchangeData(msgData)
            return reqDataValue.data
        else:
            self.sendData(msgData)
            return msgHead

    def sendData(self, data):
        self.exchangeData(data)

    def exchangeData(self, data):
        if not self.connectionState:
            ex = ApiException(*ErrTypeList.EX_CONNECT_NONE)
            raise ex
        s1 = json.dumps(data, default=lambda obj: obj.__dict__)
        lock = threading.Lock()
        if lock.acquire():
            self.tcpCliSock.send((s1 + '\n').encode())
            Logger.debug('send data:%s' % s1)
            lock.release()

    def syncExchangeData(self, msgData, timeout=30):
        requestId = msgData.head.requestId
        lock = threading.Condition()
        reqDataValue = RequestDataValue(requestId, lock)
        self.reqMap[requestId] = reqDataValue
        self.exchangeData(msgData)
        lock.acquire()
        lock.wait(timeout)
        self.checkError(reqDataValue)
        return reqDataValue

    def handleSyncRequest2(self, reqId, msgRespond, msgData):
        reqMap = self.reqMap
        reqDataValue = reqMap[reqId]
        reqDataValue.respond = msgRespond
        reqDataValue.data = msgData
        lock = reqDataValue.lock
        lock.acquire()
        lock.notify()
        lock.release()
        del reqMap[reqId]

    def handleSyncRequest(self, reqId, response):
        reqMap = self.reqMap
        reqDataValue = reqMap[reqId]
        reqDataValue.returnValue = response
        lock = reqDataValue.lock
        lock.acquire()
        lock.notify()
        lock.release()
        del reqMap[reqId]

    def onSubscriptQuota(self, data, msgRespond):
        """
        行情订阅成功/失败回调方法
        
        :param str data:
        :param CTSlib.ApiStruct.MsgRespond msgRespond:
        """
        Logger.debug('onSubscriptQuota:')
        printObject(data)

    def onQuoteEvent(self, data, msgRespond):
        """
        行情订阅数据推送回调方法
        
        :param CTSlib.ApiStruct.MsgSubQuoteReturn data:
        :param CTSlib.ApiStruct.MsgRespond msgRespond:
        
        """
        Logger.debug('onQuoteEvent:')
        printObject(data)

    def onQueryStkInfo(self, stkInfoData, msgRespond):
        """
        行情异步查询数据回调方法
        
        :param CTSlib.ApiStruct.MsgStkInfo stkInfoData:
        :param CTSlib.ApiStruct.MsgRespond msgRespond:
        
        """
        printObject(stkInfoData)

    def onQueryAccountInfo(self, accountInfoData, msgRespond):
        """
        资金账号异步查询回调方法
        
        :param CTSlib.ApiStruct.MsgAccontQuery accountInfoData:
        :param CTSlib.ApiStruct.MsgRespond msgRespond:
        
        """
        printObject(accountInfoData)

    def onOrderNew(self, orderData, msgRespond, msgHead):
        """
        异步报单回调方法
        
        :param CTSlib.ApiStruct.MsgOrderNew orderData:
        :param CTSlib.ApiStruct.MsgRespond msgRespond:
        :param CTSlib.ApiStruct.MsgHead msgHead:
        
        """
        printObject(orderData)
        printObject(msgHead)

    def onOrderCancel(self, cancelOrderData, msgRespond, msgHead):
        """
        异步撤单回调方法
        
        :param CTSlib.ApiStruct.MsgOrderCancel cancelOrderData:
        :param CTSlib.ApiStruct.MsgRespond msgRespond:
        :param CTSlib.ApiStruct.MsgHead msgHead:
        
        """
        printObject(cancelOrderData)
        printObject(msgHead)

    def onQueryOrderList(self, orderInfoData, msgRespond, msgHead):
        """
        报单查询回调方法
        
        :param CTSlib.ApiStruct.MsgQueryOrderInfo orderInfoData:
        :param CTSlib.ApiStruct.MsgRespond msgRespond:
        :param CTSlib.ApiStruct.MsgHead msgHead:
        
        """
        printObject(orderInfoData)
        printObject(msgHead)

    def onQueryKnockList(self, knockInfoData, msgRespond, msgHead):
        """
        成交查询回调方法
        
        :param CTSlib.ApiStruct.MsgQueryKnockInfo knockInfoData:
        :param CTSlib.ApiStruct.MsgRespond msgRespond:
        :param CTSlib.ApiStruct.MsgHead msgHead:
        
        """
        printObject(knockInfoData)
        printObject(msgHead)

    def onQueryPositionList(self, positionInfoData, msgRespond, msgHead):
        """
        持仓查询回调方法
        
        :param CTSlib.ApiStruct.MsgQueryPositionInfo positionInfoData:
        :param CTSlib.ApiStruct.MsgRespond msgRespond:
        :param CTSlib.ApiStruct.MsgHead msgHead:
        
        """
        printObject(positionInfoData)
        printObject(msgHead)

    def onSubscriptTrade(self, subscriptTradeData, msgRespond):
        """
        成交订阅成功/失败回调方法
        
        :param str subscriptTradeData:
        :param CTSlib.ApiStruct.MsgRespond msgRespond:
        
        """
        printObject(subscriptTradeData)

    def onTradeEvent(self, subscriptTradeData, msgRespond):
        """
        成交订阅推送数据回调方法
        
        :param CTSlib.ApiStruct.MsgSubscriptTradeReturn subscriptTradeData:
        :param CTSlib.ApiStruct.MsgRespond msgRespond:
        
        """
        printObject(subscriptTradeData)

    def onSocketError(self, status):
        """
        服务器连接异常回调方法
        
        :parameter: * status : -1-异常状态
        
        """
        print('服务器连接异常')


class RequestDataValue(object):
    reqId = 0
    lock = None
    returnValue = None

    def __init__(self, reqId, lock):
        self.reqId = reqId
        self.lock = lock


def getReqId(json_str):
    reqId = json_str['requestId']
    return reqId


class DispatchThread(threading.Thread):
    """
    数据接收线程
    
    """

    def __init__(self, ctsServer):
        threading.Thread.__init__(self)
        self.ctsServer = ctsServer
        self.thread_stop = False

    def run(self):
        """
        运行线程
        """
        threadname = threading.currentThread().getName()
        Logger.debug('Thread [%s] is running... ' % threadname)
        fileobject = None
        if _pythonMajorVersion < 3:
            fileobject = self.ctsServer.tcpCliSock.makefile()
        else:
            fileobject = self.ctsServer.tcpCliSock.makefile(encoding='UTF-8')
        reqMap = self.ctsServer.reqMap
        while not self.thread_stop:
            try:
                data = fileobject.readline()
                Logger.debug('receiveData, %s ' % data)
                if not data:
                    break
                jsonData = json.loads(data)
                jsonHead = jsonData['head']
                jsonRespond = jsonData['respond']
                jsonData = jsonData['data']
                msgRespond = MsgRespond()
                msgRespond.__dict__ = jsonRespond
                msgType = jsonHead['msgType']
                reqId = jsonHead['requestId']
                msgHead = MsgHead(msgType)
                msgHead.__dict__ = jsonHead
                if MsgTypeList.MSG_TYPE_SYS_CONNECT == msgType:
                    pass
                if reqId in reqMap:
                    msgData = MsgConnectInfo()
                    msgData.__dict__ = jsonData
                    self.ctsServer.sessionId = jsonHead['sessionId']
                    self.ctsServer.handleSyncRequest2(reqId, msgRespond, msgData)
                else:
                    if MsgTypeList.MSG_TYPE_SYS_DISCONNECT == msgType:
                        if reqId in reqMap:
                            msgData = MsgDisConnectInfo()
                            msgData.__dict__ = jsonData
                            self.ctsServer.sessionId = jsonHead['sessionId']
                            self.ctsServer.handleSyncRequest2(reqId, msgRespond, msgData)
                            break
                    else:
                        if MsgTypeList.MSG_TYPE_QRY_STKINFO == msgType:
                            msgData = MsgStkInfo()
                            if 'stkInfo' in jsonData:
                                msgData.__dict__ = jsonData['stkInfo']
                            if reqId in reqMap:
                                self.ctsServer.handleSyncRequest2(reqId, msgRespond, msgData)
                            else:
                                self.ctsServer.onQueryStkInfo(msgData, msgRespond)
                        else:
                            if MsgTypeList.MSG_TYPE_QRY_FUTURE == msgType:
                                msgData = []
                                if 'futureList' in jsonData:
                                    msgFutrueList = jsonData['futureList']
                                    for msgFutureDictTmp in msgFutrueList:
                                        msgFutureDict = MsgQueryFutureInfo()
                                        msgFutureDict.__dict__ = msgFutureDictTmp
                                        msgData.append(msgFutureDict)

                                if reqId in reqMap:
                                    self.ctsServer.handleSyncRequest2(reqId, msgRespond, msgData)
                if MsgTypeList.MSG_TYPE_ACCT_LOGIN == msgType:
                    if reqId in reqMap:
                        msgData = MsgAccount()
                        if 'acctInfo' in jsonData:
                            msgData.__dict__ = jsonData['acctInfo']
                        self.ctsServer.handleSyncRequest2(reqId, msgRespond, msgData)
                    else:
                        if MsgTypeList.MSG_TYPE_OPT_LOGIN == msgType:
                            pass
                if reqId in reqMap:
                    if msgRespond.successFlg == 0:
                        msgData = '柜员登录成功!'
                    else:
                        if msgRespond.successFlg == 1:
                            msgData = '柜员登录失败!'
                    self.ctsServer.handleSyncRequest2(reqId, msgRespond, msgData)
                else:
                    if MsgTypeList.MSG_TYPE_SUB_TRADE_RESP == msgType:
                        if msgRespond.successFlg == 0:
                            msgData = '订阅成功!'
                        else:
                            if msgRespond.successFlg == 1:
                                msgData = '订阅失败!'
                        self.ctsServer.onSubscriptTrade(msgData, msgRespond)
                    else:
                        if MsgTypeList.MSG_TYPE_SUB_TRADE_RETURN == msgType:
                            msgData = MsgSubscriptTradeReturn()
                            if 'subKnockInfo' in jsonData:
                                msgData.__dict__ = jsonData['subKnockInfo']
                            self.ctsServer.onTradeEvent(msgData, msgRespond)
                        else:
                            if MsgTypeList.MSG_TYPE_SUB_QUOTE_RESP == msgType:
                                if msgRespond.successFlg == 0:
                                    msgData = '订阅成功!'
                                else:
                                    if msgRespond.successFlg == 1:
                                        msgData = '订阅失败!'
                                self.ctsServer.onSubscriptQuota(msgData, msgRespond)
                            else:
                                if MsgTypeList.MSG_TYPE_SUB_QUOTE_RETURN == msgType:
                                    msgData = MsgSubQuoteReturn()
                                    if 'quotaInfo' in jsonData:
                                        msgData.__dict__ = jsonData['quotaInfo']
                                        self.ctsServer.onQuoteEvent(msgData, msgRespond)
                                    else:
                                        if MsgTypeList.MSG_TYPE_ORDER_NEW == msgType:
                                            msgData = MsgOrderNew()
                                            if 'contractNum' in jsonData:
                                                msgData.__dict__ = jsonData
                                            if reqId in reqMap:
                                                self.ctsServer.handleSyncRequest2(reqId, msgRespond, msgData)
                                            else:
                                                self.ctsServer.onOrderNew(msgData, msgRespond, msgHead)
                                        else:
                                            if MsgTypeList.MSG_TYPE_ORDER_CANCEL == msgType:
                                                msgData = MsgOrderCancel()
                                                if 'contractNum' in jsonData:
                                                    msgData.__dict__ = jsonData
                                                if reqId in reqMap:
                                                    self.ctsServer.handleSyncRequest2(reqId, msgRespond, msgData)
                                                else:
                                                    self.ctsServer.onOrderCancel(msgData, msgRespond, msgHead)
                                            else:
                                                if MsgTypeList.MSG_TYPE_QRY_ACCOUNT == msgType:
                                                    msgData = MsgAccontQuery()
                                                    if 'acctInfo' in jsonData:
                                                        msgData.__dict__ = jsonData['acctInfo']
                                                    if reqId in reqMap:
                                                        self.ctsServer.handleSyncRequest2(reqId, msgRespond, msgData)
                                                    else:
                                                        self.ctsServer.onQueryAccountInfo(msgData, msgRespond)
                if MsgTypeList.MSG_TYPE_FUTURE_ACCOUNT == msgType:
                    msgData = MsgQueryFutAcctInfo()
                    if 'acctInfo' in jsonData:
                        msgData.__dict__ = jsonData['acctInfo']
                    if reqId in reqMap:
                        self.ctsServer.handleSyncRequest2(reqId, msgRespond, msgData)
                    else:
                        if MsgTypeList.MSG_TYPE_QRY_ORDER == msgType:
                            if reqId in reqMap:
                                msgData = []
                                if 'orderInfo' in jsonData:
                                    msgDataList = jsonData['orderInfo']
                                    for msgOrderDictTmp in msgDataList:
                                        msgDataDict = MsgQueryOrderInfo()
                                        msgDataDict.__dict__ = msgOrderDictTmp
                                        msgData.append(msgDataDict)

                                self.ctsServer.handleSyncRequest2(reqId, msgRespond, msgData)
                            else:
                                msgData = MsgQueryOrderInfo()
                                if 'orderInfo' in jsonData:
                                    msgData.__dict__ = jsonData['orderInfo']
                                self.ctsServer.onQueryOrderList(msgData, msgRespond, msgHead)
                        else:
                            if MsgTypeList.MSG_TYPE_QRY_KNOCK == msgType:
                                if reqId in reqMap:
                                    msgData = []
                                    if 'knockInfo' in jsonData:
                                        msgDataList = jsonData['knockInfo']
                                        for msgDataDictTmp in msgDataList:
                                            msgDataDict = MsgQueryKnockInfo()
                                            msgDataDict.__dict__ = msgDataDictTmp
                                            msgData.append(msgDataDict)

                                    self.ctsServer.handleSyncRequest2(reqId, msgRespond, msgData)
                                else:
                                    msgData = MsgQueryKnockInfo()
                                    if 'knockInfo' in jsonData:
                                        msgData.__dict__ = jsonData['knockInfo']
                                    self.ctsServer.onQueryKnockList(msgData, msgRespond, msgHead)
                            else:
                                if MsgTypeList.MSG_TYPE_QRY_POSITION == msgType:
                                    if reqId in reqMap:
                                        msgData = []
                                        if 'positionInfo' in jsonData:
                                            msgDataList = jsonData['positionInfo']
                                            for msgDataDictTmp in msgDataList:
                                                msgDataDict = MsgQueryPositionInfo()
                                                msgDataDict.__dict__ = msgDataDictTmp
                                                msgData.append(msgDataDict)

                                        self.ctsServer.handleSyncRequest2(reqId, msgRespond, msgData)
                                    else:
                                        msgData = MsgQueryPositionInfo()
                                        if 'positionInfo' in jsonData:
                                            msgData.__dict__ = jsonData['positionInfo']
                                        self.ctsServer.onQueryPositionList(msgData, msgRespond, msgHead)
                                else:
                                    if msgType in self.ctsServer.callbackFuncMap:
                                        self.ctsServer.callbackFuncMap[msgType](jsonData, msgRespond, msgHead)
                                    else:
                                        Logger.debug('msgType: %s' % msgType)
                                        Logger.debug('msgData: %s' % msgData)
            except socketError as ex:
                Logger.error('Socket error... %s' % ex)
                Logger.error('Socket error... %s' % (ApiException(*ErrTypeList.EX_CONNECT_ERROR)))
                self.ctsServer.connectionState = False
                self.ctsServer.onSocketError(-1)
                break
            except Exception as ex:
                print(traceback.format_exc())
                Logger.error('DispatchThread error... %s' % ex)

    def stop(self):
        """
        停止线程
        """
        self.thread_stop = True


def encrypt2(data, key, connectionState):
    """
    加密方法,DES加密
    首先判断系统是否已经连接，如未连接抛出异常
    """
    if not connectionState:
        ex = ApiException(*ErrTypeList.EX_CONNECT_NONE)
        raise ex
    return encrypt(data, key).decode()


class ParaTerminalInfo(object):
    """
    :fieldmembers: * APIType : API类型（固定送 PyAPI）
                   * APIVersion : 送入PyAPI Version
                   * TerminalInfo : 送入终端信息
    
    """
    APIType = ''
    APIVersion = ''
    TerminalInfo = ''

    def __init__(self):
        self.APIType = 'PyAPI'
        self.APIVersion = CTSlib.__version__
        self.TerminalInfo = getTerminalInfo()


def getTerminalInfo():
    """
    获取终端信息
    """
    if os.name == 'nt':
        command = os.path.abspath(CTSlib.__path__[0] + '\\TerminalInfo')
        output = os.popen('"' + command + '"')
        return output.read()
    else:
        os.environ['LD_LIBRARY_PATH'] = str(CTSlib.__path__[0])
        command = os.path.abspath(CTSlib.__path__[0] + '/TestJavaGetTerminalInfo.so')
        output = os.popen(command)
        return output.read()
# okay decompiling ApiUtils.pyc
