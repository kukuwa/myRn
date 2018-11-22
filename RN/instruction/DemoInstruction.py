# coding=utf8
from config import *
from CTSlib.ApiUtils import *
from CTSlib.InstAPI import *
from CTSlib.SysUtils import printObject
try:
    
    # 设置日志级别
    Logger.setLogOutputFlag(True)
    Logger.setLogLevel(Logger.logLevelDebug)
    
    # 连接服务器
    tradeServer = CtsServer()
    connInfo = tradeServer.connect(serverHost, serverPort)
    printObject(connInfo, '系统连接：')
    
    # 柜员登录
    optLoign = tradeServer.optLogin(optId, optPw)
    printObject(optLoign, '柜员登录：')
    
    # 账户登录
    acctInfo = tradeServer.accountLogin(acctId, pwd)
    printObject(acctInfo, '账户登录：')
    
    # 账户登录
    acctInfo = tradeServer.accountLogin(acctId_F, pwd_F)
    printObject(acctInfo, '账户登录：')
    
    # 创建指令服务
    instServer = InstServer(tradeServer)
    
    instructId = '00000N'
    
    # 创建指令
    instInfo = ParaCreateInstInfo()
    instInfo.instructId = instructId
    instInfo.instructName = '000000'
    instInfo.acctId = acctId_F
    instInfo.orderType = 'B'
    instInfo.securityType = 'CS'
    instInfo.beginDate = '2018-03-02'
    instInfo.endDate = '2018-03-02'
    instInfo.offerStartTime = '10:00:00'
    instInfo.offerStopTime = '22:00:00'
    instInfo.memo = ''
    instInfo.checkFlag = 1
                      
    instList1 = ParaCreateInstList()
    instList1.exchId = '0'
    instList1.stkId = '600030'
    instList1.regId = 'Sh77210000'
    instList1.priceMode = 3
    instList1.orderPrice = 0
    instList1.orderQty = 1000000
    instList1.f_hedgeFlag = 'SPEC'
    instList1.traderId = optId
    instList1.numRate = 0.00
    instList1.memo = ''
    instList1.stopPrice = 0.00
                        
#     instList2 = ParaCreateInstList()
#     instList2.exchId = 'D'
#     instList2.stkId = 'c1803'
#     instList2.regId = 'D1969000'
#     instList2.priceMode = 3
#     instList2.orderPrice = 0
#     instList2.orderQty = 3000
#     instList2.f_hedgeFlag = 'SPEC'
#     instList2.f_offSetFlag = 'OPEN'
#     instList2.traderId = optId
#     instList2.numRate = 0.00
#     instList2.stopPrice = 0.00
#            
#     instList3 = ParaCreateInstList()
#     instList3.exchId = '0'
#     instList3.stkId = '600010'
#     instList3.regId = 'Sh77210000'
#     instList3.priceMode = 3
#     instList3.orderPrice = 0
#     instList3.orderQty = 10000
#     instList3.traderId = optId
#     instList3.numRate = 0.00
#     instList3.memo = ''
#     instList3.stopPrice = 0.00
#     instServer.instCreate(instInfo, [instList1,instList2,instList3])
    msgCreateInstInfo =  instServer.instCreate(instInfo, [instList1])
    if(msgCreateInstInfo):
        printObject(msgCreateInstInfo, "errorList:")
             
    # 指令暂停中止恢复
    paraInstHandle = ParaInstHandle()
    paraInstHandle.acctId = acctId
    paraInstHandle.instructId = instructId
    paraInstHandle.stkId = '600030'
    paraInstHandle.closeFlag = '0'
    successFlag = instServer.instHandle(paraInstHandle)
              
    # 指令列表查询
    paraQueryInstList = ParaQueryInstList()
    paraQueryInstList.acctId = acctId_F
    paraQueryInstList.securityType = 'FUT'
    instList = instServer.queryInstList(paraQueryInstList)
    printObject(instList,'指令列表查询:')
                  
    # 指令明细查询
    paraQueryInstInfo = ParaQueryInstInfo()
    paraQueryInstInfo.instructId = instructId
    paraQueryInstInfo.securityType = 'FUT'
    instInfo = instServer.queryInstInfo(paraQueryInstInfo)
    printMutiObject(instInfo, '指令明细查询:')
              
    # 指令报单明细查询
    paraQueryInstDetailOrder = ParaQueryInstDetailOrder()
    paraQueryInstDetailOrder.instructId = instructId
    paraQueryInstDetailOrder.queryType = 2
    paraQueryInstDetailOrder.securityType = 'CS'
    orderList = instServer.queryInstDetailOrder(paraQueryInstDetailOrder)
    printObject(orderList, '指令报单明细查询:')
       
    # 指令报单汇总查询
    paraQueryInstSumOrder = ParaQueryInstSumOrder()
    paraQueryInstSumOrder.instructId = instructId
    orderList = instServer.queryInstSumOrder(paraQueryInstSumOrder)
    printObject(orderList, '指令报单汇总查询:')
      
    # 指令成交明细查询
    paraQueryInstKnock = ParaQueryInstDetailKnock()
    paraQueryInstKnock.instructId = instructId
    paraQueryInstKnock.securityType = 'FUT'
    knockList = instServer.queryInstDetailKnock(paraQueryInstKnock)
    printObject(knockList, '指令成交明细查询:')
     
except Exception as ex:
    print(traceback.format_exc())
    Logger.error('Exception... %s' % ex)
