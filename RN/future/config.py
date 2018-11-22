﻿# coding=utf-8
from CTSlib import Logger

# 设置日志路径
Logger.setLogPath('./log')

# 设置日志级别
Logger.setLogLevel(Logger.logLevelDebug)

# 打开控制台输出
Logger.setLogOutputFlag(True)


# 服务器信息
serverHost = '127.0.0.1'
serverPort = 9880

# 期货资金账号,密码
# acctId = '000000001967'
acctId = '000000180101'
pwd = '666666'

# 柜员，密码
# optId = '00076'
# optPw = '666666'

optId = '930126'
optPw = '666666'

# 交易市场
exchId = 'F'

# 证券代码
stkId = 'IF1704'
