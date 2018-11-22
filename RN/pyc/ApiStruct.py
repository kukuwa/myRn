# uncompyle6 version 3.2.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.5 |Anaconda, Inc.| (default, Mar 29 2018, 13:32:41) [MSC v.1900 64 bit (AMD64)]
# Embedded file name: CTSlib\ApiStruct.py
# Compiled at: 2018-07-16 16:58:55
# Size of source mod 2**32: 38775 bytes
"""
Python API 接口
提供行情、交易接口结构

"""
from CTSlib.SysUtils import *
sequenceManager = SequenceManager()

class MsgHead(object):
    """
    通讯数据包头类
    """
    msgType = 0
    sessionId = ''
    requestId = 0

    def __init__(self, msgType, sessionId='-1', requestId=0):
        self.msgType = msgType
        self.sessionId = sessionId
        self.requestId = sequenceManager.getNextId()


class MsgRespond(object):
    """
    通讯数据响应类
    
    :fieldmembers: * successFlg : 成功标记(0-成功，1-失败)
                   * errorCode : 错误代码
                   * errorMsg : 错误信息
                   * lastFlag : 数据包是否最后一个
    
    """
    successFlg = 0
    errorCode = ''
    errorMsg = ''
    lastFlag = True

    def __init__(self, successFlg=0, errorCode='', errorMsg='', lastFlag=True):
        self.successFlg = successFlg
        self.errorCode = errorCode
        self.errorMsg = errorMsg
        self.lastFlag = lastFlag


class MsgData(object):
    head = None
    request = None
    respond = None
    data = None

    def __init__(self, msgHead=None, request=None):
        self.head = msgHead
        self.request = request


class MsgConnectInfo(object):
    """
    服务器连接信息
    
    :fieldmembers:  * sysDate : 系统时间
                    * sysVersion : 系统版本号
                    * customer : 客户名称
                    * serverName : 服务器名称
                    * expireDate : 过期日期
    
    """
    pass


class MsgDisConnectInfo(object):
    """
    服务器断开信息
    
    :fieldmembers:  * sysDate : 系统时间
    
    """
    pass


class ParaStkInfo(object):
    """
    行情查询
    
    :fieldmembers: * exchId : 交易市场
                   * stkId : 证券代码
    """
    exchId = ''
    stkId = ''

    def __init__(self, exchId, stkId):
        self.exchId = exchId
        self.stkId = stkId


class MsgQueryFutureInfo(object):
    """
    futureInfo                  期货合约基本信息
    
    :fieldmembers:  * exchId : 市场
                    * f_productId : 品种
                    * stkId : 合约代码
                    * stkName : 合约名称
                    * stkStatus : 合约状态
                    * basicExchId : 标的证券所在市场
                    * basicStkId : 标的证券代码
                    * contractTimes : 合约乘数
                    * deliveryType : 交割方式
                    * deliveryYear : 交割年份
                    * deliveryMonth : 交割月份
                    * listDate : 上市日
                    * firstTrdDate : 首交易日
                    * lastTrdDate : 最后交易日
                    * matureDate : 到期日
                    * lastSettleDate : 最后结算日
                    * deliveryDate : 交割日
                    * stkOrderStatus : 合约交易状态
                    * stkOrderStatusDesc : 合约交易状态描述
                    * orderPriceUnit : 价格档位
                    * maxLimitOrderQty : 限价委托上限数量(每笔最大限量)
                    * maxMarketOrderQty : 市价委托上限数量(每笔最大限量)
                    * minLimitOrderQty : 限价委托下限数量(每单最小数量单位)
                    * minMarketOrderQty : 市价委托下限数量(每单最小数量单位)
                    * maxOrderPrice : 委托价格上限、上限价(涨停价格)
                    * minOrderPrice : 委托价格下限、下限价(跌停价格)
                    * upPercent : 涨幅比例
                    * downPercent : 跌幅比例
                    * preSettlementPrice : 昨日结算价
                    * preClosePrice : 昨收盘
                    * preOpenPosition : 市场昨持仓量
                    * openPrice : 开盘价
                    * highestPrice : 最高价
                    * lowestPrice : 最低价
                    * exchTotalKnockQty : 当天交易所总成交数量
                    * exchTotalKnockAmt : 当天交易所总成交金额
                    * openPosition : 市场持仓量
                    * closePrice : 收盘价
                    * settlementPrice : 结算价(全价)
                    * preDelta : 昨虚实度
                    * delta : 今虚实度
                    * basicStkType : 标的证券类型
                    * basicPreClosePrice : 标的证券昨收盘
                    * strikeStyle : 行权方式
                    * exerciseDate : 行权-行权日
                    * currMargin : 当前保证金总额
                    * stkType : 证券类型
                    * optionStkId : 权证代码
                    * newPrice : 最新价
                    * strikePrice : 行权价格
                    * optionType : 权证类型
                    * optExecType : 期权执行方式(0欧式，1 美式)
                    * marginRate1 : 保证金比率1
                    * marginRate2 : 保证金比率2
                    * optionMonth : 合约到期月份类型
                    * adjustedFlag : 是否调整标志(Y-是,N-否)
                    * preContractTimes : 上一交易日合约乘数
                    * expireType : 过期类型
                    * lastUpdateDate : 最后修改日期
    
    """
    pass


class MsgStkInfo(object):
    """
    stkInfo                      证券信息
    
    :fieldmembers:  * exchId : 交易市场
                    * stkId : 证券代码
                    * stkName : 证券名称
                    * newPrice : 最新价格
                    * openPrice : 开盘价格
                    * closePrice : 昨收盘价
                    * buyPrice : 买盘价格
                    * sellPrice : 卖盘价格
                    * buyAmt : 买盘数量
                    * sellAmt : 卖盘数量
                    * closeFlag : 停牌标记
                    * highPrice : 今日最高
                    * lowPrice : 今日最低
                    * maxOrderPrice : 价格上限
                    * minOrderPrice : 价格下限
                    * knockQty : 成交数量
                    * knockAmt : 成交金额
                    * preClosePrice : 昨收盘价格
                    * preSettlementPrice : 昨日结算价
                    * F_productId : 产品内部编码
                    * basicExchId : 标的证券所在市场
                    * basicStkId : 标的证券代码
                    * F_BasisPrice : 挂牌基准价
                    * settleGrp : 结算组
                    * settleID : 结算编号
                    * stkOrderStatus : 合约交易状态
                    * preOpenPosition : 市场昨持仓量
                    * highestPrice : 最高价
                    * lowestPrice : 最低价
                    * exchTotalKnockQty : 当天交易所总成交数量
                    * exchTotalKnockAmt : 当天交易所总成交金额
                    * openPosition : 市场持仓量
                    * settlementPrice : 结算价
                    * preDelta : 昨虚实度
                    * delta : 今虚实度
                    * lastModifyTime : 最后修改时间
                    * mseconds : 最后修改毫秒
                    * contractTimes : 合约乘数
                    * deliveryDate : 交割日
                    * endDays : 计息截止天
                    * estimate : 约用资金
                    * beginPrice : 开始价格
                    * endPrice : 结束价格
                    * stkType : 证券类别
                    * lastTrdDate : 最后交易日
                    * orderPriceUnit : 价格单位
                    * qtyPerHand : 每手数量
                    * strikePrice : 行权价格
                    * optionType : 期权类型(P-看涨期权，C-看跌期权)
                    * optExecType : 期权执行方式(0-欧式，1-美式)
                    * optionStkId : 期权证券代码
                    * stkStatus : 合约状态
                    * stkStatusDesc : 合约状态描述
                    * deliveryType : 交割方式
                    * deliveryYear : 交割年份
                    * deliveryMonth : 交割月
                    * listDate : 上市日
                    * firstTrdDate : 首交易日
                    * matureDate : 到期日
                    * lastSettleDate : 最后结算日
                    * stkOrderStatusDesc : 合约交易状态描述
                    * maxLimitOrderQty : 限价委托上限数量
                    * maxMarketOrderQty : 市价委托上限数量
                    * upPercent : 涨幅比例
                    * downPercent : 跌幅比例
                    * tradeUnit : 交易单位
                    * basicStkType : 标的证券类型(EBS-ETF，ASH-A股,IDX-指数)
                    * basicPreClosePrice : 标的证券昨收盘
                    * strikeStyle : 行权方式欧式美式(欧式-E,美式-A)
                    * exerciseDate : 行权日(T+1)
                    * currMargin : 个股期权持空仓单位保证金
                    * referencePrice : 参考价格
    
    """
    pass


class ParaAccount(object):
    """
    账户登录参数
    """
    acctId = ''
    password = ''

    def __init__(self, acctId, password):
        self.acctId = acctId
        self.password = password


class MsgAccount(object):
    """
    acctInfo                     账户信息
    
    :fieldmembers:  * acctId : 资金帐号
                    * acctName : 帐户姓名
                    * currencyId : 币种代码
                    * currentAmt : 资金余额
                    * usableAmt : 可用金额
                    * creditFundFlag : 帐户类型（0-现货帐户 9-期货帐户）
                    * sysDate : 系统时间
                    * regList : 股东信息列表
                        * exchId : 交易市场
                        * regId : 股东代码
                        * regName : 股东姓名
    
    """
    pass


class ParaOptLogin(object):
    """
    柜员登录参数
    """
    optId = ''
    password = ''

    def __init__(self, optId, password):
        self.optId = optId
        self.password = password


class ParaOrderNew(object):
    """
    orderInfo                    报单信息
    
    :fieldmembers: * acctId : 资金帐号(必送)
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
                   * f_offSetFlag : 开平标记（OPEN-开仓，CLOSE-平仓）(期货期权必送)
                   * bsFlag : 委托类型（B-多头，S-空头）(期货期权必送)
                   * f_orderPriceType : 价格类型（ANY-任意价，LIMIT-限价）(期货期权必送)
                   * f_hedgeFlag : 投保标记 (可选)
                   * coveredFlag : 备兑标签(可选)(0-非备兑,1-备兑)
                   * businessMark : 交易业务类型(可选)(OTO-期权订单，OTU-证券冻结与解冻，OTE-行权)
    
    """
    orderInfo = ''

    def __init__(self, orderInfo):
        self.orderInfo = orderInfo


class OrderNewInfo(object):
    """
    orderInfo                    报单信息
    
    :fieldmembers:  * acctId : 资金帐号(必送)
                    * currencyId : 资金代码(期货期权必送)
                    * exchId : 交易市场(必送)
                    * stkId : 证券代码(必送)
                    * orderType : 委托类型(现货必送)
                        * B : 普通买入
                        * S : 普通卖出
                        * YB : 对手最优价买(市价委托,exchId=1)
                        * YS : 对手最优价卖(市价委托,exchId=1)
                        * XB : 本方最优价买(市价委托,exchId=1)
                        * XS : 本方最优价卖(市价委托,exchId=1)
                        * 2B : 即时成交买(市价委托,exchId=1)
                        * 2S : 即时成交卖(市价委托,exchId=1)
                        * VB : 最优五档买(市价委托,exchId=0,1)
                        * VS : 最优五档卖(市价委托,exchId=0,1)
                        * WB : 全额成交买(市价委托,exchId=0,1)
                        * WS : 全额成交卖(市价委托,exchId=0,1)
                    * orderPrice : 委托价格(必送)
                    * orderQty : 委托数量(必送)
                    * contractNum : 合同序号(可选)
                    * regId : 股东代码(可选,默认报单市场的第一个股东)
                    * batchNum : 委托批号(可选)
                    * clientId : 客户端编号(可选)
                    * f_offSetFlag : 开平标记（OPEN-开仓，CLOSE-平仓）(期货期权必送)
                    * bsFlag : 委托类型（B-多头，S-空头）(期货期权必送)
                    * f_orderPriceType : 价格类型（ANY-任意价，LIMIT-限价）(期货期权必送)
                    * f_hedgeFlag : 投保标记 (可选)
                    * coveredFlag : 备兑标签(可选)(0-非备兑,1-备兑)
                    * businessMark : 交易业务类型(可选)(OTO-期权订单，OTU-证券冻结与解冻，OTE-行权)
    
    """
    orderInfo = ''
    acctId = ''
    currencyId = ''
    exchId = ''
    stkId = ''
    orderType = ''
    orderPrice = ''
    orderQty = ''
    contractNum = ''
    regId = ''
    batchNum = ''
    clientId = ''
    f_offSetFlag = ''
    bsFlag = ''
    f_orderPriceType = ''
    f_hedgeFlag = ''
    coveredFlag = ''
    businessMark = ''


class OrderCancelInfo(object):
    """
    撤单信息
    
    :fieldmembers:  * acctId : 资金帐号(必送)
                    * exchId : 交易市场(必送)
                    * contractNum : 合同序号(必送)
    
    """
    acctId = ''
    exchId = ''
    contractNum = ''


class MsgOrderNew(object):
    """
    报单信息
    
    :fieldmembers:  * contractNum : 合同号
                    * orderAmt : 委托金额
                    * usableAmt : 可用金额
    
    """
    pass


class ParaOrderCancel(object):
    """
    orderCancelInfo             撤单功能
    
    :fieldmembers:  * acctId : 资金帐号(必送)
                    * exchId : 交易市场(必送)
                    * contractNum : 合同序号(必送)
    
    """
    orderCancelInfo = ''

    def __init__(self, orderCancelInfo):
        self.orderCancelInfo = orderCancelInfo


class MsgOrderCancel(object):
    """
    撤单信息
    
    撤单成功 Fieldmembers:
        * contractNum : 合同序号
        * completeNum : 成功笔数
        * orderTime : 委托时间
    
    撤单失败 Fieldmembers:
        * acctId : 资金帐号(必送)
        * exchId : 交易市场(必送)
        * contractNum : 合同序号
    
    """
    pass


class ParaAccontQuery(object):
    """
    资金账号查询
    
    :fieldmembers:  * acctId : 资金帐号(必送)
                    * currencyId : 币种(必送)
    
    """
    acctId = ''
    currencyId = ''

    def __init__(self, acctId, currencyId):
        self.acctId = acctId
        self.currencyId = currencyId


class ParaQueryFutAcctInfo(object):
    """
    资金账号查询
    
    :fieldmembers:  * acctId : 资金帐号(必送)
                    * currencyId : 币种(必送)
    
    """
    acctId = ''
    currencyId = ''

    def __init__(self, acctId, currencyId):
        self.acctId = acctId
        self.currencyId = currencyId


class MsgAccontQuery(object):
    """
    acctInfo                     账户信息
    
    :fieldmembers:  * acctId : 资金帐号
                    * currencyId : 币种
                    * currencyName : 货币名称
                    * custId : 客户帐号
                    * custName : 客户姓名
                    * currentAmt : 余额
                    * usableAmt : 可用数
                    * stkValue : 证券市值
                    * tradeFrozenAmt : 交易冻结
                    * exceptFrozenAmt : 异常冻结
                    * currentStkValue : 参考市值
                    * creditFundFlag : 信用资金标志
                    * acctAtRiskLevel : 帐户风险承受等级
    
    """
    pass


class MsgQueryFutAcctInfo(object):
    """
    acctInfo                      账户信息
    
    :fieldmembers:  * acctId : 资金帐户
                    * currencyId : 币种代码
                    * acctName : 帐户姓名
                    * custType : 客户类别
                    * custId : 客户代码
                    * currentAmt : 当前余额
                    * usableAmt : 可用余额（实时计算）
                    * realtimeAmt : 权益（实时计算）
                    * closePNL : 平仓盈亏
                    * realtimePNL : 实时盈亏（实时计算）
                    * ydMarginUsedAmt : 昨日保证金占用
                    * marginUsedAmt : 当日保证金占用（实时计算）
                    * tradeFrozenAmt : 交易冻结金额
                    * cashMovementAmt : 当日出入金
                    * commision : 手续费用
    """
    pass


class ParaSubQuote(object):
    """
    行情订阅
    
    :fieldmembers: * quotaList :
                        * exchId : 市场
                        * stkId : 证券代码
                   * subType : 订阅类型(必送，默认为0) 0-订阅 1-退订
    """
    subType = ''
    quotaList = []

    def __init__(self, quotaList, subType):
        self.subType = subType
        self.quotaList = quotaList


class SubQuotaContent(object):
    """
    行情订阅
    
    :fieldmembers:  * exchId : 市场
                    * stkId : 证券代码
    """
    exchId = ''
    stkId = ''

    def __init__(self, exchId, stkId):
        self.exchId = exchId
        self.stkId = stkId


class MsgSubQuoteReturn(object):
    """
    quotaInfo                    行情信息
    
    :fieldmembers:  * exchId : 市场
                    * stkId : 证券代码
                    * newPrice : 最新价
                    * highPrice : 今日最高价
                    * lowPrice : 今日最低价
                    * closePrice : 昨收盘
                    * buy : 买盘价
                    * buyAmt : 买盘量
                    * sell : 卖盘价
                    * sellAmt : 卖盘量
                    * referencePrice : 参考价格
                    * openPosition : 持仓量
                    * exchTotalKnockQty : 成交量
                    * exchTotalKnockAmt : 成交金额
                    * lastModifyTime : 行情时间
    
    """
    pass


class ParaSubscriptTrade(object):
    """
    成交订阅
    
    :fieldmembers: * acctId : 资金账号(必送)
                   * pwd : 交易密码(必送)
                   * subType : 订阅类型(必送，默认为0) 0-订阅 1-退订
    """
    acctId = ''
    password = ''
    subType = ''

    def __init__(self, acctId, pwd, subType):
        self.acctId = acctId
        self.password = pwd
        self.subType = subType


class MsgSubscriptTradeReturn(object):
    """
    subKnockInfo                    账户信息
    
    :fieldmembers:  * acctId : 资金帐号
                    * exchId : 市场
                    * stkId : 证券代码
                    * orderQty : 委托数量
                    * orderPrice : 委托价格
                    * contractNum : 合同号
                    * orderType : 买卖方向
                    * returnType : 回报类型
                    * tradingResultType : 成交类型
                    * knockQty : 成交数量
                    * knockPrice : 成交价格
                    * knockAmt : 成交金额
                    * fullKnockAmt : 全价成交金额
                    * reckoningAmt : 清算金额
                    * accuredInterestAmt : 应计利息金额
                    * accuredInteres : 应计利息
                    * knockTime : 交易所成交时间
                    * knockCode : 交易所成交编号
                    * serialNum : 根网内部成交编号
                    * exchErrorCode : 交易所错误编码
                    * memo : 交易所错误编码描述
                    * regId : 市场股东代码
                    * stkType : 证券类别
                    * tradeType : 交易类型
                    * f_offSetFlag : 开平标记
                    * closePNL : 平仓盈亏
                    * openUsedMarginAmt : 今开占用保证金
                    * offsetMarginAmt : 平仓释放保证金
                    * bsFlag : 买卖标志
                    * batchNum : 委托批号
                    * ownerType : 订单所有类型
                    * orderTime : 委托时间
                    * f_hedgeFlag : 投保标记
    """
    pass


class QueryOrderCond(object):
    """
    queryCond                    查询条件
    
    :fieldmembers:  * acctId : 资金帐号(必送)
                    * exchId : 市场代码(可选)
                    * batchNum : 批号(可选)
                    * contractNum : 合同号(可选)
                    * stkId : 证券代码(可选)
                    * withdrawFlag : 撤单标志(可选, N-报单, Y-撤单)
                    * isCancellable : 是否可撤单标志(可选)
                    * beginTime : 起始时间(可选, hh:mm:ss)
                    * endTime : 结束时间(可选, hh:mm:ss)
    """
    acctId = ''
    exchId = ''
    batchNum = ''
    contractNum = ''
    stkId = ''
    withdrawFlag = ''
    isCancellable = ''
    beginTime = ''
    endTime = ''


class ParaQueryOrderInfo(object):
    """
    queryCond                      报单查询条件
    
    :fieldmembers:  * queryCond : 查询条件
                    * maxRowNum : 最大查询记录数量(可选，默认为100)
                    * pageNum : 查询页数(可选，默认为1)
                    * queryType : 同步异步数据返回标记
    """
    queryCond = ''
    maxRowNum = ''
    pageNum = ''
    queryType = ''

    def __init__(self, queryCond, maxRowNum, pageNum, queryType):
        self.queryCond = queryCond
        self.maxRowNum = maxRowNum
        self.pageNum = pageNum
        self.queryType = queryType


class MsgQueryOrderInfo(object):
    """
    orderInfo                    报单信息
    
    :fieldmembers:  * exchId : 市场代码
                    * contractNum : 合同序号
                    * acctId : 资金帐号
                    * regId : 股东代码
                    * regName : 股东姓名
                    * orderType : 委托类型
                    * stkId : 证券代码
                    * stkName : 证券名称
                    * orderPrice : 委托价格
                    * orderQty : 委托数量
                    * knockQty : 成交数量
                    * withdrawQty : 撤单数量
                    * orderTime : 委托时间
                    * offerTime : 申报时间
                    * orderPuttingQty : 申报数量
                    * validFlag : 合法标志
                        * -1 : 待回报
                        * 0 : 合法
                        * 1 : 非法
                        * 2 : 未开户
                    * validFlagDesc : 合法标志描述
                    * sendFlag : 报送标志
                    * sendFlagDesc : 报送标志描述
                    * withdrawFlag : 撤单标志
                    * withdrawFlagDesc : 撤单标志描述
                    * withdrawOrderFlag : 已下撤单委托标志
                    * memo : 备注
                    * batchNum : 委托批号
                    * stkType : 证券类别
                    * tradeType : 交易类型
                    * orderAmt : 委托金额
                    * statusId : 委托状态
                    * exchErrorCode : 交易所的委托确认码
                    * orderStatus : 交易状态
                    * isCancellable : 可撤单标志
                    * occurTime : 发生时间
                    * operationMAC : 委托主机MAC地址
                    * basketId : 篮子代码
                    * f_orderStatus : 报单状态
                    * orderId : 交易的订单编号
                    * serialNum : 流水号，作为交易所的requestId使用
                    * actionFlag : 报单的操作类型(NEW-报单, DELETE-撤单)
                    * f_hedgeFlag : 投保标记
                    * f_offSetFlag : 开平标志
                    * bsFlag : 合约方向(B-多头，S-空头)
                    * f_orderPriceType : 报单价格条件
                    * futureOrderPrice : 委托价格(精确到小数点后4位)
                    * f_MatchCondition : 有效期类型
                    * GTDDate : GTS日期
                    * filledQtyCondition : 成交量类型
                    * minimalVolume : 最小成交量
                    * queuedCondition : 触发条件
                    * stopPrice : 止损价格
                    * autoSuspend : 自动挂起标志
                    * f_forceCloseReason : 强平原因
                    * exchErrorMsg : 错误信息
                    * openUsedMarginAmt : 今开占用保证金
                    * closePNL : 平仓损益
                    * offsetMarginAmt : 平仓释放保证金
                    * openFrozMargin : 开仓冻结保证金
                    * coveredFlag : 备兑标签(0-非备兑,1-备兑)
    """
    pass


class MsgQueryPositionInfo(object):
    """
    positionInfo                 持仓信息
    
    :fieldmembers:  * exchId : 交易市场
                    * exchAbbr : 市场简称
                    * stkId : 证券代码
                    * stkName : 证券名称
                    * orderUnit : 交易单位
                    * orderUnitDesc : 委托单位描述
                    * exceptFrozenQty : 异常冻结数量
                    * sellFrozenQty : 卖出冻结数量
                    * buyFrozenQty : 买入冻结数量
                    * newPrice : 最新价
                    * regId : 股东代码
                    * previousQty : 昨日余额
                    * previousCost : 昨日买入成本金额
                    * previousIncome : 昨日收益
                    * acctId : 资金帐号
                    * currentStkValue : 当前证券市值
                    * currentQtyForAsset : 计算资产用的股份余额
                    * realtimeCost : 实时成本
                    * realtimeIncome : 实时收入
                    * usableQty : 可用数量(单位为委托单位)
                    * unsaleableQty : 非流通余额非流通股份（股票）
                    * rightsQty : 权益数量
                    * frozenQty : 冻结权益数量
                    * stkValue : 证券市值
                    * currentQty : 实时股份余额（考虑实时买卖）
                    * expectedbuyamt : 回报买入金额
                    * expectedsellamt : 回报卖出金额
                    * maxSellStkQty : 回报卖出数量
                    * qtyPerHand : 委托单位
                    * bsFlag : 合约方向(B-多头，S-空头)
                    * f_hedgeFlag : 投保标记
                    * currentPositionQty : 当前持仓数量
                    * realTimePositionQty : 实时持仓数（实时计算）
                    * ydPositionUsableQty : 昨日持仓可平仓数
                    * todayPositionUsableQty : 今日持仓可平仓数
                    * todayPositionCost : 今开持仓均价
                    * preSettlementPrice : 昨日结算价
                    * closePNL : 平仓盈亏
                    * realtimePNL : 实时盈亏（实时计算）
                    * openFrozPositionQty : 开仓冻结数量
                    * todayOffsFrozPositionQty : 平今冻结
                    * ydOffsFrozPositionQty : 平昨冻结数
                    * marginFrozenAmt : 保证金冻结金额
                    * marginUsedAmt : 当日保证金占用（实时计算）
                    * todayContractAmt : 今日合约金额
                    * ydContractAmt : 昨日持仓合约金额
                    * coveredFlag : 备兑标签(可选)(0-备兑,1-非备兑)
                    * securityType : 证券类型（CS-现货，FUT-期货）
    """
    pass


class QueryFutureCond(object):
    """
    queryCond                   期货合约查询条件
    
    :fieldmembers:  * exchId : 市场(可选)
                    * f_productId : 品种(可选)
    """
    exchId = ''
    f_productId = ''


class ParaQueryFutureInfo(object):
    """
    期货合约查询参数
    
    :fieldmembers:  * queryCond : 查询条件
                        * exchId : 市场(可选)
                        * f_productId : 品种(可选)
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


class QueryKnockCond(object):
    """
    queryCond                    查询条件
    
    :fieldmembers:  * acctId : 资金帐号(必送)
                    * contractNum : 合同号(可选)
                    * stkId : 证券代码(可选)
                    * beginTime : 起始时间(可选, hh:mm:ss)
                    * endTime : 结束时间(可选, hh:mm:ss)
    """
    acctId = ''
    contractNum = ''
    stkId = ''
    beginTime = ''
    endTime = ''


class QueryPositionCond(object):
    """
    queryCond                    查询条件
    
    :fieldmembers:  * acctId : 资金帐号(必送)
                    * exchId : 市场代码(可选)
                    * stkId : 证券代码(可选)
                    * regId : 股东代码(可选)
                    * bsFlag : 合约方向(期货，期权可选)(B-多头，S-空头)
                    * f_hedgeFlag : 投保标记(期货，期权可选)(HEDGE-套保，SPEC-投机)
                    * coveredFlag : 备兑标签(期货，期权可选)(0-备兑,1-非备兑)
    """
    acctId = ''
    exchId = ''
    stkId = ''
    regId = ''
    bsFlag = ''
    f_hedgeFlag = ''
    coveredFlag = ''


class ParaQueryKnockInfo(object):
    """
    成交查询参数
    
    :fieldmembers:  * maxRowNum : 最大查询记录数量(可选，默认为100)
                    * pageNum : 查询页数(可选，默认为1)
    """
    queryCond = ''
    maxRowNum = ''
    pageNum = ''
    queryType = ''

    def __init__(self, queryCond, maxRowNum, pageNum, queryType):
        self.queryCond = queryCond
        self.maxRowNum = maxRowNum
        self.pageNum = pageNum
        self.queryType = queryType


class ParaQueryPositionInfo(object):
    """
    持仓查询参数
    
    :fieldmembers:  * maxRowNum : 最大查询记录数量(可选，默认为100)
                    * pageNum : 查询页数(可选，默认为1)
    """
    queryCond = ''
    maxRowNum = ''
    pageNum = ''
    queryType = ''

    def __init__(self, queryCond, maxRowNum, pageNum, queryType):
        self.queryCond = queryCond
        self.maxRowNum = maxRowNum
        self.pageNum = pageNum
        self.queryType = queryType


class MsgQueryKnockInfo(object):
    """
    knockInfo                    成交信息
    
    :fieldmembers:  * acctId : 资金帐号
                    * exchId : 市场
                    * stkName : 证券名称
                    * occurTime : 发生时间
                    * stkId : 证券代码
                    * totalWithdrawQty : 总撤单数量
                    * orderQty : 委托数量
                    * regName : 股东名称
                    * postQty : 本次可用股份
                    * orderPrice : 委托价格
                    * contractNum : 合同号
                    * orderType : 买卖方向
                    * knockQty : 成交数量
                    * knockPrice : 成交价格
                    * knockAmt : 成交金额
                    * fullKnockAmt : 全价成交金额
                    * reckoningAmt : 清算金额
                    * accuredInterestAmt : 应计利息金额
                    * accuredInterest : 应计利息
                    * knockTime : 交易所成交时间
                    * knockCode : 交易所成交编号
                    * serialNum : 根网内部成交编号
                    * exchErrorCode : 交易所错误编码
                    * memo : 交易所错误编码描述
                    * stkType : 证券类别
                    * tradeType : 交易类型
                    * deskId : 席位代码
                    * optId : 操作柜员
                    * optMode : 委托方式
                    * branchId : 营业部
                    * custType : 客户类别
                    * brokerId : 经纪人
                    * custId : 客户代码
                    * tradingResultTypeDesc : 成交类别说明
                    * briefId : 摘要代码
                    * internalBizMark : 业务交易类型
                    * internalOrderType : 内部委托类型
                    * productGrp : 产品集编码
                    * knockNum : 产品集成交序号
                    * operationMAC : 委托主机MAC地址
                    * basketId : 篮子代码
                    * orderId : 交易的订单编号
                    * f_hedgeFlag : 投保标记
                    * f_offSetFlag : 开平标志
                    * bsFlag : 合约方向(B-多头，S-空头)
                    * futureOrderPrice : 报单价格
                    * execType : 执行状态
                    * cumQty : 累计成交数量
                    * leavesQty : 剩余数量
                    * orderSerial : 按时间排队的序号
                    * knockPrice : 成交价格
                    * openUsedMarginAmt : 今开占用保证金
                    * closePNL : 平仓盈亏
                    * offsetMarginAmt : 平仓释放保证金
                    * exchErrorMsg : 错误信息
                    * commision : 手续费
                    * coveredFlag : 备兑标签(0-非备兑,1-备兑)
    """
    pass


class MsgQueryUndueRepurchase(object):
    """
    undueRepurchaseList           未到期回购列表
    
    :fieldmembers:  * acctId :资金账号
                    * exchId : 市场
                    * stkId : 证券代码
                    * regId : 股东代码
                    * rollbackDate: 购回日期
                    * rollbackAmt: 购回金额（平仓时使用）
                    * orderTime:回购委托时间
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
    查询未到期回购条件
    
    :fieldmembers:  * queryCond : 查询条件
                        * acctId :资金账号
                        * stkId:证券代码(可选)
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
# okay decompiling ApiStruct.pyc
