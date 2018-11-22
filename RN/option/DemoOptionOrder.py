#coding=utf-8
from CTSlib.ApiStruct import *
from CTSlib.ApiUtils import *
from CTSlib.ExtendAPI import *
from config import *
import time

try:
    
    # 设置日志级别
    Logger.setLogOutputFlag(True)
    Logger.setLogLevel(Logger.logLevelDebug)
    
    # 测试连接服务器
    tradeServer = CtsServer()
    connInfo = tradeServer.connect(serverHost, serverPort)
    printObject(connInfo, '系统连接：')
    
    # 柜员登录
    optLoign = tradeServer.optLogin(optId, optPw)
    printObject(optLoign, '柜员登录：')
    
    # 账户登录
    acctInfo = tradeServer.accountLogin(acctId, pwd)
    printObject(acctInfo, '账户登录：')
    
    # 查询行情
    stkInfo = tradeServer.queryStkInfo(exchId, stkId)

    # 报单(同步)
    orderInfo = OrderNewInfo()
    orderInfo.acctId = acctId
    orderInfo.currencyId = acctInfo.currencyId
    orderInfo.exchId = exchId
    orderInfo.stkId = stkId
    orderInfo.orderType = 'B'
    orderInfo.orderQty = 2
    orderInfo.orderPrice = stkInfo.newPrice
    orderInfo.f_offSetFlag = 'OPEN'
    orderInfo.bsFlag = 'B'
    orderInfo.businessMark = 'OTO'
    orderInfo.f_orderPriceType = 'ANY'
    newOrderResponse = tradeServer.orderNew(orderInfo)
    printObject(newOrderResponse, '期权报单结果：')
    orderNewContractNum_sync = newOrderResponse.contractNum

    # 报单(异步)
    orderInfo = OrderNewInfo()
    orderInfo.acctId = acctId
    orderInfo.currencyId = acctInfo.currencyId
    orderInfo.exchId = exchId
    orderInfo.stkId = stkId
    orderInfo.orderType = 'B'
    orderInfo.orderQty = 2
    orderInfo.orderPrice = stkInfo.newPrice
    orderInfo.f_offSetFlag = 'OPEN'
    orderInfo.bsFlag = 'B'
    orderInfo.businessMark = 'OTO'
    orderInfo.f_orderPriceType = 'ANY'
    global orderNewContractNum_noSync
    orderNewContractNum_noSync = ''
    def onOrderNew(returnData, msgRespond, msgHead):
        if(msgRespond.successFlg != 0):
            printString('期权报单结果：')
            printString('%s,%s' , (msgRespond.errorCode, msgRespond.errorMsg))
        else:
            global orderNewContractNum_noSync
            orderNewContractNum_noSync = returnData.contractNum
            printObject(returnData, '期权报单结果：')
            printObject(msgHead)
    tradeServer.onOrderNew = onOrderNew
    msgHead = tradeServer.orderNew(orderInfo, False) #异步请求方法返回包头
    printObject(msgHead, '期权报单发送：')

    # 撤单(同步)
    orderCancelInfo = OrderCancelInfo()
    orderCancelInfo.acctId = acctId
    orderCancelInfo.exchId = exchId
    orderCancelInfo.contractNum = orderNewContractNum_sync
    cancellOrderResponse = tradeServer.orderCancel(orderCancelInfo)
    printObject(cancellOrderResponse, '期权撤单结果：')

    # 撤单(异步)
    time.sleep(1)
    orderCancelInfo = OrderCancelInfo()
    orderCancelInfo.acctId = acctId
    orderCancelInfo.exchId = exchId
    orderCancelInfo.contractNum = orderNewContractNum_noSync
    def onOrderCancel(returnData, msgRespond, msgHead):
        if(msgRespond.successFlg != 0):
            printString('期权撤单结果：')
            printString('%s,%s' , (msgRespond.errorCode, msgRespond.errorMsg))
        else:
            printObject(returnData, '期权撤单结果：')
            printObject(msgHead)
    tradeServer.onOrderCancel = onOrderCancel
    msgHead = tradeServer.orderCancel(orderCancelInfo, False) #异步请求方法返回包头
    printObject(msgHead, '期权撤单发送：')

    # 期权报单查询(同步)
    queryCond = QueryOrderCond()
    queryCond.acctId = acctId
    orderList = tradeServer.queryOrderList(queryCond, maxRowNum = 100, pageNum = 1,syncFlag = True)
    printObject(orderList,'期权报单查询：')
     
    # 期权报单查询(异步)
    queryCond = QueryOrderCond()
    queryCond.acctId = acctId
    def onQueryOrderList(returnData, msgRespond, msgHead):
        if(msgRespond.successFlg != 0):
            printString('期权报单查询：')
            printString('%s,%s' , (msgRespond.errorCode, msgRespond.errorMsg))
        else:
            printObject(returnData, '期权报单查询：')
            if (msgRespond.lastFlag):
                printString('查询数据全部返回')
    tradeServer.onQueryOrderList = onQueryOrderList
    msgHead = tradeServer.queryOrderList(queryCond, maxRowNum = 100, pageNum = 1,syncFlag = False)
    printObject(msgHead,'期权报单查询发送:')

    # 查询期权历史交易日志
    extendServer = ExtendServer(tradeServer)
    queryCond = QueryCond()
    queryFutTradingLogHis = extendServer.queryFutTradingLogHis(queryCond, maxRowNum=100, pageNum=1)
    printObject(queryFutTradingLogHis, '查询期货历史交易日志')

    # 期权成交查询(同步)
    queryCond = QueryKnockCond()
    queryCond.acctId = acctId
    knockList = tradeServer.queryKnockList(queryCond, maxRowNum = 100, pageNum = 1, syncFlag = True)
    printObject(knockList,'期权成交查询：')

    # 期权成交查询(异步)
    queryCond = QueryKnockCond()
    queryCond.acctId = acctId
    def onQueryKnockList(returnData, msgRespond, msgHead):
        if(msgRespond.successFlg != 0):
            printString('期权成交查询：')
            printString('%s,%s' , (msgRespond.errorCode, msgRespond.errorMsg))
        else:
            printObject(returnData, '期权成交查询：')
            if (msgRespond.lastFlag):
                printString('查询数据全部返回')
    tradeServer.onQueryKnockList = onQueryKnockList
    msgHead = tradeServer.queryKnockList(queryCond, maxRowNum = 100, pageNum = 1, syncFlag = False)
    printObject(msgHead,'期权成交查询发送：')
    
except Exception as ex:
    Logger.error('Exception... %s' % ex)
