# uncompyle6 version 3.2.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.5 |Anaconda, Inc.| (default, Mar 29 2018, 13:32:41) [MSC v.1900 64 bit (AMD64)]
# Embedded file name: CTSlib\InstAPI.py
# Compiled at: 2018-06-27 11:43:50
# Size of source mod 2**32: 21609 bytes
"""
Created on 2017年12月6日

Python API 服务
提供指令交易功能
"""
from CTSlib.ApiStruct import *
from CTSlib.ApiUtils import *

class InstServer:
    """
    指令交易服务类
    """

    def __init__(self, ctsServer):
        self.ctsServer = ctsServer
        self.ctsServer.addFunCallback(MsgTypeList.MSG_TYPE_CREATE_INST, self.onInstCreate)
        self.ctsServer.addFunCallback(MsgTypeList.MSG_TYPE_QRY_INSTLIST, self.onQueryInstList)
        self.ctsServer.addFunCallback(MsgTypeList.MSG_TYPE_QRY_INSTINFO, self.onQueryInstInfo)
        self.ctsServer.addFunCallback(MsgTypeList.MSG_TYPE_QRY_INST_DETAILORDER, self.onQueryInstDetailOrder)
        self.ctsServer.addFunCallback(MsgTypeList.MSG_TYPE_QRY_INST_SUMORDER, self.onQueryInstSumOrder)
        self.ctsServer.addFunCallback(MsgTypeList.MSG_TYPE_QRY_INST_DETAILKNOCK, self.onQueryInstDetailKnock)
        self.ctsServer.addFunCallback(MsgTypeList.MSG_TYPE_HANDLE_INST, self.onInstHandle)

    def instCreate(self, instInfo, instLists):
        """
        指令创建
        
        :parameters: * instInfo : 指令信息
                     * instLists : 指令明细
        
        """
        msgHead = MsgHead(MsgTypeList.MSG_TYPE_CREATE_INST, self.ctsServer.sessionId)
        msgRequest = {}
        msgRequest['instInfo'] = instInfo
        msgRequest['instList'] = instLists
        msgData = MsgData(msgHead, msgRequest)
        reqDataValue = self.ctsServer.syncExchangeData(msgData)
        return reqDataValue.data

    def onInstCreate(self, jsonData, msgRespond, msgHead):
        """
        指令创建回调方法
        """
        msgData = ''
        if msgRespond.successFlg == 0:
            if 'errorList' not in jsonData:
                Logger.debug('requestId:%s,创建指令成功！' % msgHead.requestId)
            Logger.debug('requestId:%s,创建指令失败！' % msgHead.requestId)
            msgData = []
            if 'errorList' in jsonData:
                msgDataList = jsonData['errorList']
                for msgDataDictTmp in msgDataList:
                    msgDataDict = MsgInstCreate()
                    msgDataDict.__dict__ = msgDataDictTmp
                    msgData.append(msgDataDict)

        if msgHead.requestId in self.ctsServer.reqMap:
            self.ctsServer.handleSyncRequest2(msgHead.requestId, msgRespond, msgData)

    def instHandle(self, instInfo):
        """
        指令暂停中止恢复操作
        
        instInfo    指令信息
        """
        msgHead = MsgHead(MsgTypeList.MSG_TYPE_HANDLE_INST, self.ctsServer.sessionId)
        msgRequest = {}
        msgRequest['instInfo'] = instInfo
        msgData = MsgData(msgHead, msgRequest)
        reqDataValue = self.ctsServer.syncExchangeData(msgData)
        return reqDataValue.data

    def onInstHandle(self, jsonData, msgRespond, msgHead):
        """
        指令暂停中止恢复操作回调方法
        """
        msgData = ''
        if msgRespond.successFlg == 0:
            Logger.debug('requestId:%s,指令操作成功！' % msgHead.requestId)
            msgData = True
        else:
            Logger.debug('requestId:%s,指令操作失败！' % msgHead.requestId)
            msgData = False
        if msgHead.requestId in self.ctsServer.reqMap:
            self.ctsServer.handleSyncRequest2(msgHead.requestId, msgRespond, msgData)

    def queryInstList(self, paraQueryInstList):
        """
        指令列表查询
        """
        msgHead = MsgHead(MsgTypeList.MSG_TYPE_QRY_INSTLIST, self.ctsServer.sessionId)
        msgRequest = {}
        msgRequest['instInfo'] = paraQueryInstList
        msgData = MsgData(msgHead, msgRequest)
        reqDataValue = self.ctsServer.syncExchangeData(msgData)
        return reqDataValue.data

    def onQueryInstList(self, jsonData, msgRespond, msgHead):
        """
        指令列表查询回调方法
        """
        if msgHead.requestId in self.ctsServer.reqMap:
            msgData = []
            if 'instList' in jsonData:
                msgDataList = jsonData['instList']
                for msgDataDictTmp in msgDataList:
                    msgDataDict = MsgQueryInstList()
                    msgDataDict.__dict__ = msgDataDictTmp
                    msgData.append(msgDataDict)

            self.ctsServer.handleSyncRequest2(msgHead.requestId, msgRespond, msgData)

    def queryInstInfo(self, paraQueryInstInfo):
        """
        指令明细查询
        """
        msgHead = MsgHead(MsgTypeList.MSG_TYPE_QRY_INSTINFO, self.ctsServer.sessionId)
        msgRequest = {}
        msgRequest['instInfo'] = paraQueryInstInfo
        msgData = MsgData(msgHead, msgRequest)
        reqDataValue = self.ctsServer.syncExchangeData(msgData)
        return reqDataValue.data

    def onQueryInstInfo(self, jsonData, msgRespond, msgHead):
        """
        指令明细查询回调方法
        """
        if msgHead.requestId in self.ctsServer.reqMap:
            msgData = MsgQueryInstInfo()
            msgDataList = []
            if 'instList' in jsonData:
                msgDataListTmp = jsonData['instList']
                for msgDataDictTmp in msgDataListTmp:
                    msgQueryInstInfo_InstList = MsgQueryInstInfo_InstList()
                    msgQueryInstInfo_InstList.__dict__ = msgDataDictTmp
                    msgDataList.append(msgQueryInstInfo_InstList)

                msgData.instList = msgDataList
            if 'instInfo' in jsonData:
                msgQueryInstInfo_InstInfo = MsgQueryInstInfo_InstInfo()
                msgQueryInstInfo_InstInfo.__dict__ = jsonData['instInfo']
                msgData.instInfo = msgQueryInstInfo_InstInfo
            self.ctsServer.handleSyncRequest2(msgHead.requestId, msgRespond, msgData)

    def queryInstDetailOrder(self, paraQueryInstDetailOrder):
        """
        指令报单明细
        """
        msgHead = MsgHead(MsgTypeList.MSG_TYPE_QRY_INST_DETAILORDER, self.ctsServer.sessionId)
        msgRequest = {}
        msgRequest['instInfo'] = paraQueryInstDetailOrder
        msgData = MsgData(msgHead, msgRequest)
        reqDataValue = self.ctsServer.syncExchangeData(msgData)
        return reqDataValue.data

    def onQueryInstDetailOrder(self, jsonData, msgRespond, msgHead):
        """
        指令报单明细查询回调方法
        """
        if msgHead.requestId in self.ctsServer.reqMap:
            msgData = []
            if 'orderList' in jsonData:
                msgDataList = jsonData['orderList']
                for msgDataDictTmp in msgDataList:
                    msgDataDict = MsgQueryInstDetailOrder()
                    msgDataDict.__dict__ = msgDataDictTmp
                    msgData.append(msgDataDict)

            self.ctsServer.handleSyncRequest2(msgHead.requestId, msgRespond, msgData)

    def queryInstSumOrder(self, paraQueryInstSumOrder):
        """
        指令报单汇总查询
        """
        msgHead = MsgHead(MsgTypeList.MSG_TYPE_QRY_INST_SUMORDER, self.ctsServer.sessionId)
        msgRequest = {}
        msgRequest['instInfo'] = paraQueryInstSumOrder
        msgData = MsgData(msgHead, msgRequest)
        reqDataValue = self.ctsServer.syncExchangeData(msgData)
        return reqDataValue.data

    def onQueryInstSumOrder(self, jsonData, msgRespond, msgHead):
        """
        指令报单汇总查询回调方法
        """
        if msgHead.requestId in self.ctsServer.reqMap:
            msgData = []
            if 'orderList' in jsonData:
                msgDataList = jsonData['orderList']
                for msgDataDictTmp in msgDataList:
                    msgDataDict = MsgQueryInstSumOrder()
                    msgDataDict.__dict__ = msgDataDictTmp
                    msgData.append(msgDataDict)

            self.ctsServer.handleSyncRequest2(msgHead.requestId, msgRespond, msgData)

    def queryInstDetailKnock(self, paraQueryInstDetailKnock):
        """
        指令成交查询
        """
        msgHead = MsgHead(MsgTypeList.MSG_TYPE_QRY_INST_DETAILKNOCK, self.ctsServer.sessionId)
        msgRequest = {}
        msgRequest['instInfo'] = paraQueryInstDetailKnock
        msgData = MsgData(msgHead, msgRequest)
        reqDataValue = self.ctsServer.syncExchangeData(msgData)
        return reqDataValue.data

    def onQueryInstDetailKnock(self, jsonData, msgRespond, msgHead):
        """
        指令成交查询回调方法
        """
        if msgHead.requestId in self.ctsServer.reqMap:
            msgData = []
            if 'knockList' in jsonData:
                msgDataList = jsonData['knockList']
                for msgDataDictTmp in msgDataList:
                    msgDataDict = MsgQueryInstDetailKnock()
                    msgDataDict.__dict__ = msgDataDictTmp
                    msgData.append(msgDataDict)

            self.ctsServer.handleSyncRequest2(msgHead.requestId, msgRespond, msgData)


class ParaCreateInstInfo:
    """
    instInfo        指令公共信息
    
    :fieldmembers: * instructId : 指令ID
                   * instructName : 指令名称
                   * acctId : 资金账号
                   * securityType : 证券类型（CS-现货，FUT-期货）
                   * orderType : 买卖方向
                   * beginDate : 指令起始日期（yyyy-mm-dd）
                   * endDate : 指令结束日期（yyyy-mm-dd）
                   * offerStartTime : 指令起始时间（hh:mm:ss）
                   * offerStopTime : 指令结束时间（hh:mm:ss）
                   * memo : 指令的备注
                   * checkFlag : 是否交易检查（0-不检查，1-检查）
    
    """
    pass


class ParaCreateInstList:
    """
    instList        指令列表
    
    :fieldmembers: * exchId : 市场
                   * stkId : 证券代码
                   * regId : 股东代码
                   * f_offSetFlag : 开平标志（OPEN-开仓，CLOSE-平仓）
                   * f_hedgeFlag : 投保标记（SPEC-投机，HEDGE-套保，ARB-套利）
                   * priceMode : 价格策略（0--固定 1--限价 2--CD 3--市场价格）
                   * orderPrice : 委托价格
                   * orderQty : 委托数量
                   * traderId : 交易员
                   * numRate : 量比比例
                   * memo : 指令明细的备注
                   * stopPrice : 止损价格
    
    """
    pass


class MsgInstCreate:
    """
    errorList        错误返回列表
    
    :fieldmembers: * successFlg : 成功标志
                   * tradeFlag : 允许交易标志
                   * errorCode : 错误代码
                   * failInfo : 中文失败信息
                   * englishFailInfo : 英文失败信息
                   * optFlag : 操作标志
                   * exceptionType : 异常类型
                   * instructId : 指令ID
                   * stkId : 证券代码
                   * traderId : 交易员代码
                   * orderType : 买卖方向
                   * exchId : 交易市场
                   * regId : 股东代码
                   * acctId : 资金帐号
                   * custId : 客户帐号
                   * orderQty : 委托数量
                   * orderPrice : 委托价格
                   * optId : 柜员代码
                   * restrictMode : 限制类型
                   * stkName : 证券名称
    
    """
    pass


class ParaQueryInstList:
    """
    instInfo        指令列表查询参数
    
    :fieldmembers: * acctId : 资金帐号(必送)
                   * securityType : 证券类型（CS-现货，FUT-期货）
                   * instructStatus : 指令状态(可选)
    
    """
    pass


class MsgQueryInstList:
    """
    instList                      指令列表
    
    :fieldmembers: * instructId : 指令ID
                   * instructName : 指令名称
                   * acctId : 资金帐号
                   * orderType : 委托类型、回购方向、买卖方向
                   * beginDate : 指令起始日期
                   * endDate : 指令结束日期
                   * offerStartTime : 指令起始时间
                   * offerStopTime : 指令结束时间
                   * instructStatus : 指令状态
                       * InstructStatus_NotDeal : 0; //未处理
                       * InstructStatus_Execute : 1; //执行
                       * InstructStatus_WithDraw : 2; //终止
                       * InstructStatus_Invalid : 3; //失效,日终
                       * InstructStatus_Pause : 4; //暂停
                       * InstructStatus_Finish : 5; //完成
                       * InstructStatus_SubExecute : 6; //部分执行
                       * InstructStatus_Uncheck : 8; //需要复核，但尚未复核
                       * InstructStatus_NoPass : 9; //复核不通过
                   * instructDate : 指令下达时间
                   * optId : 操作柜员
                   * otherAmt : 换股指令买入额外增减资金
                   * riskMemo : 风险提醒备注信息
    
    """
    pass


class ParaQueryInstInfo:
    """
    instInfo        指令明细查询参数
    
    :fieldmembers: * instructId : 指令ID(可选必送)
                   * securityType : 证券类型（CS-股票，FUT-期货）
    
    """
    pass


class MsgQueryInstInfo:
    """
    指令查询返回
    
    :fieldmembers:  * instInfo : 指令公共信息
                    * instList : 指令列表
    """
    instInfo = ''
    instList = ''


class MsgQueryInstInfo_InstInfo:
    """
    instInfo         指令公共信息
    
    :fieldmembers: * instructId : 指令ID
                   * instructName : 指令名称
                   * acctId : 资金帐号
                   * orderType : 委托类型、回购方向、买卖方向
                   * beginDate : 有效开始日期
                   * endDate : 有效结束日期
                   * offerStartTime : 开始申报时间
                   * offerStopTime : 停止申报时间
                   * instructStatus : 指令状态
                   * instructDate : 指令下达时间
                   * optId : 操作柜员
                   * riskMemo : 风险提醒备注信息
    
    """
    pass


class MsgQueryInstInfo_InstList:
    """
    instList        指令列表
    
    :fieldmembers: * exchId : 市场
                   * instructId : 指令ID
                   * stkId : 证券代码
                   * stkName : 证券名称
                   * f_offSetFlag : 开平标志（OPEN-开仓，CLOSE-平仓）
                   * f_hedgeFlag : 投保标记（SPEC-投机，HEDGE-套保，ARB-套利）
                   * priceMode : 价格策略 (0--固定，1--限价，2--CD，3--市场价格)
                   * orderPrice : 委托价格
                   * orderQty : 委托数量
                   * executeQty : 执行数量
                   * regId : 股东代码
                   * buyAmt : 约用资金
                   * traderId : 交易员
                   * exchTotalKnockQty : 指令创建时市场成交量
                   * exchTotalKnockAmt : 指令创建时市场成交金额
                   * numRate : 量比
                   * memo : 备注
                   * stopPrice : 止损价格
                   * orderAmt : 指令金额
                   * instructType : 指令类别（0-数量指令，1-金额指令）
                   * executeStatus : 执行状态
                       * 0 : 执行
                       * 1 : 终止
                       * 2 : 锁定
                       * 3 : 暂停
                       * 4 : 完成
                   * rate : 比率（换股指令）
                   * fixOrderFlag : 订单标记
                   * referencePrice : 参考价格
                   * arrivedLastPx : 接受订单时的市场价格
    
    """
    pass


class ParaQueryInstDetailOrder:
    """
    instInfo        指令报单明细查询参数
    
    :fieldmembers: * instructId : 指令ID(必送)
                   * securityType : 证券类型（CS-股票，FUT-期货）
                   * stkId : 证券代码
                   * queryType : 查询类型
                       * 0 : 未完成询类型
                       * 2 : 全部不含撤单
    
    """
    pass


class MsgQueryInstDetailOrder:
    """
    orderList        指令报单明细查询返回
    
    :fieldmembers: * instructId : 指令ID
                   * acctId : 资金帐号
                   * exchId : 市场
                   * orderType : 买卖反向
                   * f_offSetFlag : 开平标志（OPEN-开仓，CLOSE-平仓）
                   * f_hedgeFlag : 投保标记（SPEC-投机，HEDGE-套保，ARB-套利）
                   * stkId : 证券代码
                   * stkName : 证券名称
                   * batchNum : 批号
                   * contractNum : 合同号
                   * orderQty : 指令数量
                   * knockQty : 已成交数量
                   * orderTime : 委托时间
                   * withdrawQty : 撤单数量
                   * fillStauts : 指令成交状态
                       * 期货 : 0-全部成交，1-部分成交，2-未成交
                       * 现货 : 0-完全成交,1-部分成交,2-未成交,3-撤单，4-部分撤单
                   * knockPrice : 成交价格
                   * knockAmt : 成交金额
    
    """
    pass


class ParaQueryInstSumOrder:
    """
    instInfo        指令报单汇总查询参数
    
    :fieldmembers: * instructId : 指令ID(必送)
                   * stkId : 证券代码(可选)
    
    """
    pass


class MsgQueryInstSumOrder:
    """
    orderList        指令报单汇总查询返回
    
    :fieldmembers: * instructId : 指令ID
                   * acctId : 资金帐号
                   * exchId : 市场
                   * stkId : 证券代码
                   * regId : 股东代码
                   * orderType : 买卖反向
                   * f_offSetFlag : 开平标志（OPEN-开仓，CLOSE-平仓）
                   * orderQty : 委托数量
                   * knockQty : 成交数量
                   * orderAmt : 委托金额
                   * knockAmt : 成交金额
                   * knockAvgPx : 成交均价
    
    """
    pass


class ParaQueryInstDetailKnock:
    """
    instInfo        指令成交明细查询参数
    
    :fieldmembers: * instructId : 指令ID(必送)
                   * securityType : 证券类型（CS-股票，FUT-期货）
                   * stkId : 证券代码(可选)
    
    """
    pass


class MsgQueryInstDetailKnock:
    """
    knockList        指令成交明细查询返回
    
    :fieldmembers: * instructId : 指令代码
                   * acctId : 资金帐号
                   * orderType : 买卖方向
                   * f_offSetFlag : 开平标志（OPEN-开仓，CLOSE-平仓）
                   * f_hedgeFlag : 投保标记（SPEC-投机，HEDGE-套保，ARB-套利）
                   * stkId : 证券代码
                   * stkName : 证券名称
                   * batchNum : 批号
                   * contractNum : 合同号
                   * orderQty : 指令数量
                   * knockQty : 成交数量
                   * exchId : 市场
                   * regId : 股东代码
                   * status : 执行状态
                       * 0 : 完全成交
                       * 1 : 部分成交
                   * knockTime : 成交时间
                   * knockPrice : 成交价格
                   * knockAmt : 成交金额
    
    """
    pass


class ParaInstHandle:
    """
    指令暂停中止恢复参数
    
    :fieldmembers:  * acctId : 资金账号(必送)
                    * instructId : 指令ID(必送)
                    * stkId : 证券代码(可选)
                    * closeFlag : 操作类型(必送)
                        * 0-暂停
                        * 1-中止
                        * 2-恢复
    
    """
    pass
# okay decompiling InstAPI.pyc
