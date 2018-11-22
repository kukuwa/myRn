# uncompyle6 version 3.2.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.5 |Anaconda, Inc.| (default, Mar 29 2018, 13:32:41) [MSC v.1900 64 bit (AMD64)]
# Embedded file name: CTSlib\ExtendAPI.py
# Compiled at: 2018-07-23 14:57:14
# Size of source mod 2**32: 16826 bytes
"""
Python API 服务
"""
from CTSlib.ApiStruct import *
from CTSlib.ApiUtils import *

class ExtendServer(object):

    def __init__(self, ctsServer):
        self.ctsServer = ctsServer
        self.ctsServer.addFunCallback(MsgTypeList.MSG_TYPE_EXTEND_UNDUE_REPURCHASE, self.onQueryUndueRepurchase)
        self.ctsServer.addFunCallback(MsgTypeList.MSG_TYPE_EXTEND_STK_TRADINGLOG, self.onQueryStkTradingLogHis)
        self.ctsServer.addFunCallback(MsgTypeList.MSG_TYPE_EXTEND_FUT_TRADINGLOG, self.onQueryFutTradingLogHis)

    def queryUndueRepurchase(self, queryCond, maxRowNum=100, pageNum=1):
        """
        查询未到期回购
        
        :parameters:  * queryCond : 查询条件
                          * acctId : 资金账号
                          * stkId : 证券代码(可选)
                      * maxRowNum : 最大查询记录数量(可选，默认为100)
                      * pageNum : 查询页数(可选，默认为1)
        """
        msgHead = MsgHead(MsgTypeList.MSG_TYPE_EXTEND_UNDUE_REPURCHASE, self.ctsServer.sessionId)
        msgRequest = ParaQueryUndueRepurchase(queryCond, maxRowNum, pageNum)
        msgData = MsgData(msgHead, msgRequest)
        reqDataValue = self.ctsServer.syncExchangeData(msgData)
        return reqDataValue.data

    def onQueryUndueRepurchase(self, jsonData, msgRespond, msgHead):
        """
        查询未到期回购回调方法
        """
        if msgHead.requestId in self.ctsServer.reqMap:
            msgData = []
            if 'undueRepurchaseList' in jsonData:
                msgDataList = jsonData['undueRepurchaseList']
                for msgDataDictTmp in msgDataList:
                    msgDataDict = MsgQueryUndueRepurchase()
                    msgDataDict.__dict__ = msgDataDictTmp
                    msgData.append(msgDataDict)

            self.ctsServer.handleSyncRequest2(msgHead.requestId, msgRespond, msgData)

    def queryStkTradingLogHis(self, queryCond, maxRowNum=100, pageNum=1):
        """
        查询现货历史交易日志
        
        :parameters:  * queryCond : 查询条件
                          * queryOptId : 查询柜员代码(可选)
                          * beginDate : 起始日期(必送)
                          * endDate : 截止日期(必送)
                          * acctId : 资金帐号(必送)
                          * grantExchList : 交易所代码(可选，多个使用^隔开)
                          * stkId : 证券代码(可选)
                          * regId : 股东代码(可选)
                          * custId : 客户帐号(可选)
                          * briefId : 摘要代码(可选)
                          * currencyId : 货币代码(可选)
                          * bankId : 银行代码(可选)
                          * branchId : 客户开户营业部代码、所属营业部代码、营业部标识、营业部(可选)
                          * custType : 客户类别(可选)
                          * brokerId : 经纪人代码(可选)
                          * creditFundFlag : 信用资金帐户标志,账户属性(可选)
                      * maxRowNum : 最大查询数量(可选)
                      * pageNum : 查询页码(可选)
        """
        msgHead = MsgHead(MsgTypeList.MSG_TYPE_EXTEND_STK_TRADINGLOG, self.ctsServer.sessionId)
        msgRequest = ParaQueryStkTradingLogHis(queryCond, maxRowNum, pageNum)
        msgData = MsgData(msgHead, msgRequest)
        reqDataValue = self.ctsServer.syncExchangeData(msgData)
        return reqDataValue.data

    def onQueryStkTradingLogHis(self, jsonData, msgRespond, msgHead):
        """
        查询现货历史交易日志回调方法
        """
        if msgHead.requestId in self.ctsServer.reqMap:
            msgData = []
            if 'tradingInfoList' in jsonData:
                msgDataList = jsonData['tradingInfoList']
                for msgDataDictTmp in msgDataList:
                    msgDataDict = MsgQueryStkTradingLogHis()
                    msgDataDict.__dict__ = msgDataDictTmp
                    msgData.append(msgDataDict)

            self.ctsServer.handleSyncRequest2(msgHead.requestId, msgRespond, msgData)

    def queryFutTradingLogHis(self, queryCond, maxRowNum=100, pageNum=1):
        """
        查询期货历史交易日志
        
        :parameters:  * queryCond : 查询条件
                          * beginDate : 开始日期（必送）
                          * endDate : 截止日期（必送）
                          * f_productId : 品种代码
                          * exchId : 市场代码
                          * branchId : 营业部代码
                          * deskId : 席位代码
                          * acctId : 资金帐号
                          * regId : 交易编码
                          * futureId : 合约代码
                          * basketId : 投资组合代码(多选)【根据app处理逻辑进行注释】
                          * briefId : 操作摘要
                          * internalOffSetFlag : 内部开平标识
                          * internalCoveredFlag : 内部备兑标识
                          * brokerId : 经纪人代码(可选)
                          * creditFundFlag : 信用资金帐户标志,账户属性(可选)
                      * maxRowNum : 最大查询数量(可选)
                      * pageNum : 查询页码(可选)
        
        """
        msgHead = MsgHead(MsgTypeList.MSG_TYPE_EXTEND_FUT_TRADINGLOG, self.ctsServer.sessionId)
        msgRequest = ParaQueryStkTradingLogHis(queryCond, maxRowNum, pageNum)
        msgData = MsgData(msgHead, msgRequest)
        reqDataValue = self.ctsServer.syncExchangeData(msgData)
        return reqDataValue.data

    def onQueryFutTradingLogHis(self, jsonData, msgRespond, msgHead):
        """
        查询期货历史交易日志回调方法
        """
        if msgHead.requestId in self.ctsServer.reqMap:
            msgData = []
            if 'tradingInfoList' in jsonData:
                msgDataList = jsonData['tradingInfoList']
                for msgDataDictTmp in msgDataList:
                    msgDataDict = MsgQueryFutTradingLogHis()
                    msgDataDict.__dict__ = msgDataDictTmp
                    msgData.append(msgDataDict)

            self.ctsServer.handleSyncRequest2(msgHead.requestId, msgRespond, msgData)


class ParaQueryFutTradingLogHis(object):
    """
    期货历史交易日志查询参数
    
    :fieldmembers:  * queryCond : 查询条件
                        * beginDate : 开始日期（必送）
                        * endDate : 截止日期（必送）
                        * f_productId : 品种代码
                        * exchId: 市场代码
                        * acctId: 资金帐号
                        * regId : 交易编码
                        * futureId: 合约代码
                        * briefId : 操作摘要
                        * creditFundFlag: 信用资金帐户标志,账户属性(可选)
                    * maxRowNum : 最大查询数量(可选，默认为100)
                    * pageNum : 查询页码(可选，默认为1)
    
    """
    pass


class MsgQueryFutTradingLogHis(object):
    """
    tradingInfoList               期货交易信息列表
    
    :fieldmembers:  * serialNum : 流水号
                    * briefId : 摘要代码
                    * exteriorDesc : 摘要描述
                    * currencyId : 货币代码
                    * reckoningTime : 清算时间
                    * occurTime : 发生时间
                    * partId : 会员编号
                    * bankId : 银行代码
                    * contractNum : 合同序号
                    * branchId : 营业部代码
                    * custId : 客户代码
                    * custName : 客户姓名
                    * custType : 客户类别
                    * exchId : 交易市场
                    * acctId : 资金帐号
                    * acctName : 帐户名称
                    * regId : 交易编码
                    * offerRegId : 报盘股东代码
                    * F_productId : 产品代码
                    * stkId : 合约代码
                    * stkName : 合约名称
                    * deskId : 席位代码
                    * bsFlag : 买卖方向
                    * bsFlagDesc : 买卖方向描述
                    * settlementPrice : 今结算价格
                    * preSettlementPrice : 昨结算价格
                    * knockCode : 成交编号
                    * knockQty : 成交数量
                    * kncokPrice : 成交价格
                    * knockAmt : 成交金额
                    * knockTime : 成交时间
                    * reckoningAmt : 清算金额
                    * postAmt : 后资金额
                    * .postQty : 后持有数量
                    * exchCommision : 交易所手续费
                    * custCommision : 客户手续费
                    * custMarginAmt : 客户保证金占用
                    * exchMarginAmt : 交易所保证金占用
                    * closePNL : 平仓盈亏
                    * realTimePNL : 实时盈亏
                    * F_hedgeFlag : 投保标志
                    * F_hedgeFlagDesc : 投保标志描述
                    * F_offsetFlagDesc : 开平标志描述
                    * internalOffSetFlag : 内部开平标识
                    * internalOffSetFlagDesc : 内部开平标识描述
                    * str2 : 备兑标识（外）
                    * str3 : 备兑标识（内）
                    * costCenterId : 成本中心代码
                    * salesId : 销售员代码
                    * accountingFlag : 后台记帐标志
                    * getAccountDate : 记帐日期
                    * getAccountNum : 记帐流水号
                    * selfFlag : 自营标志
                    * custodyMode : 托管方式
                    * settleDate : 清算日期
                    * settleOptId : 清算柜员代码
                    * optMode : 委托方式
                    * memo : 备注
                    * openPrice : 开仓价格
                    * openDate : 开仓日期
                    * openKnockCode : 开仓成交编号
                    * floatPNL : 浮动盈亏
                    * everyPositionPNL : 逐笔持仓盈亏
                    * basketId : 投资组合代码
                    * interContnum : 内部流水号
                    * F_MatchCondition : 有效期类型
                    * handlingfee : 经手费
                    * reckoningfee : 结算费
                    * da1 : 盈亏（不含手续费）
    """
    pass


class ParaQueryStkTradingLogHis(object):
    """
    现货历史交易日志查询参数
    
    :fieldmembers:  * queryCond : 查询条件
                        * beginDate :起始日期(必送)
                        * endDate :截止日期(必送)
                        * acctId:资金帐号(必送)
                        * regId :股东代码(可选)
                        * stkId :证券代码(可选)
                        * briefId :摘要代码(可选)
                        * currencyId:货币代码(可选)
                        * creditFundFlag:信用资金帐户标志,账户属性(可选)
                    * maxRowNum : 最大查询数量(可选，默认为100)
                    * pageNum : 查询页码(可选，默认为1)
    """
    queryCond = ''
    maxRowNum = ''
    pageNum = ''

    def __init__(self, queryCond, maxRowNum, pageNum):
        self.queryCond = queryCond
        self.maxRowNum = maxRowNum
        self.pageNum = pageNum


class MsgQueryStkTradingLogHis(object):
    """
    tradingInfoList               现货交易信息列表
    
    :fieldmembers:  * serialNum : 流水号
                    * briefId : 摘要代码
                    * occurTime : 发生时间
                    * reckoningTime : 清算时间
                    * acctId : 资金帐号
                    * acctName : 帐户姓名
                    * regId : 股东帐户
                    * optmode : 委托方式
                    * reckoningAmt : 资金发生数
                    * postAmt : 资金余额
                    * currencyId : 货币
                    * exchId : 交易所
                    * contractNum : 合同序号
                    * stkId : 证券代码
                    * stkName : 证券名称
                    * knockPrice : 成交价格
                    * knockAmt : 成交金额
                    * fullknockamt : 全价成交金额
                    * knockQty : 成交数量(单位为委托单位)
                    * knockQtyF : 成交数量(支持小数位，场外开放基金会有小数)
                    * postQty : 股份余额
                    * undoFlagDesc : 冲正标志
                    * exteriorDesc : 摘要说明
                    * stampTax : 印花税
                    * commision : 手续费
                    * tradeTransFee : 过户费
                    * exchTransFee : 一级过户费
                    * reckoningFee : 清算费
                    * transruleFee : 交易规费
                    * perorderFee : 委托单费
                    * withdrawFee : 撤单单费
                    * knockFee : 成交单费
                    * exteriorAcctId : 外部帐号
                    * tradeCurrencyId : 交易币种(港股通业务用)
                    * exchRate : 结算汇率(港股通业务用)
                    * tradeReckoningAmt : 交易币种资金发生数(港股通业务用)
                    * settleKnockAmt : 结算币种成交金额(港股通业务用)
                    * settleFullKnockAmt : 结算币种全价成交金额(港股通业务用)
    """
    pass


class MsgQueryUndueRepurchase(object):
    """
    undueRepurchaseList           未到期回购列表
    
    :fieldmembers:  * acctId :资金账号
                    * exchId : 市场
                    * stkId : 证券代码
                    * regId : 股东代码
                    * rollbackDate : 购回日期
                    * rollbackAmt : 购回金额（平仓时使用）
                    * orderTime :回购委托时间
                    * knockQty : 成交数量
                    * knockPrice : 成交金额
                    * contractNum : 合同号
                    * deskId : 席位
                    * custId : 客户编号
                    * financeOrderFlag : 回购方向(0-买入融资,1-卖出融券)
                    * stkType : 证券类别
                    * deposit : 履约金
                    * bondId : 债券代码
                    * creditFundFlag : 信用资金帐户标志
                    * totalRollBackAmt : 累计已经购回金额
                    * totalKnockQty : 总成交数量
                    * needSettleQty : 未交收数量
                    * needSettleAmt : 在途资金
                    * exteriorAcctId : 外部帐号
                    * repurchaseDay : 交易期限(回购天数)
                    * targetDeskId : 对方席位代码
                    * registerNo : 登记结算编号
                    * knockCode : 成交编号
                    * knockAmt : 成交金额
                    * branchId : 所属营业部代码
                    * regName : 股东姓名
                    * stkName : 证券名称
                    * financeInterest : 借款利息
    
    """
    pass


class ParaQueryUndueRepurchase(object):
    """
    未到期回购查询参数
    
    :fieldmembers:  * queryCond : 查询条件
                        * acctId : 资金账号
                        * stkId : 证券代码(可选)
                    * maxRowNum : 最大查询记录数量(可选，默认为100)
                    * pageNum : 查询页数(可选，默认为1)
    """
    queryCond = ''
    maxRowNum = ''
    pageNum = ''

    def __init__(self, queryCond, maxRowNum, pageNum):
        self.queryCond = queryCond
        self.maxRowNum = maxRowNum
        self.pageNum = pageNum


class QueryCond(object):
    """
    queryCond查询公共类
    """
    pass
# okay decompiling ExtendAPI.pyc
