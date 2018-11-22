# uncompyle6 version 3.2.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.5 |Anaconda, Inc.| (default, Mar 29 2018, 13:32:41) [MSC v.1900 64 bit (AMD64)]
# Embedded file name: CTSlib\Logger.py
# Compiled at: 2018-06-27 14:38:03
# Size of source mod 2**32: 4038 bytes
"""
提供 API 日志服务功能
日志默认输出到程序运行当前目录下的 log 目录，系统自动创建目录结构
日志分为四个级别进行记录，分别是 info, error, warn, debug

"""
__author__ = 'GuiPei <guipei@croot.com>'
__status__ = 'production'
__version__ = '1.01'
__date__ = '2017-03-10'
import sys, os, datetime, logging, types, traceback
from CTSlib.SysUtils import *
from logging.handlers import RotatingFileHandler
logLevelInfo = logging.INFO
logLevelError = logging.ERROR
logLevelDebug = logging.DEBUG
logLevelWarn = logging.WARN
logDate = datetime.datetime.now().strftime('%Y%m%d')
logPath = ''
logInfo = logging.Logger(logging.INFO)
logDebug = logging.Logger(logging.DEBUG)
logError = logging.Logger(logging.ERROR)
logWarn = logging.Logger(logging.WARN)
FORMAT = '%(asctime)-15s %(levelname)s -- %(message)s'
defaultFormat = logging.Formatter(FORMAT)
logStream = logging.StreamHandler(stream=sys.stdout)
logStream.setFormatter(defaultFormat)

def setLogPath(path):
    """
    设置日志路径
    """
    logPath = path
    if not os.path.exists(logPath):
        os.makedirs(logPath)
    fileHandlerInfo = logging.handlers.RotatingFileHandler('%s/log_%s_info.log' % (logPath, logDate), mode='a', maxBytes=52428800, backupCount=100, encoding=encode, delay=0)
    fileHandlerInfo.setFormatter(defaultFormat)
    logInfo.addHandler(fileHandlerInfo)
    fileHandlerDebug = logging.handlers.RotatingFileHandler('%s/log_%s_debug.log' % (logPath, logDate), mode='a', maxBytes=52428800, backupCount=100, encoding=encode, delay=0)
    fileHandlerDebug.setFormatter(defaultFormat)
    logDebug.addHandler(fileHandlerDebug)
    fileHandlerError = logging.handlers.RotatingFileHandler('%s/log_%s_error.log' % (logPath, logDate), mode='a', maxBytes=52428800, backupCount=100, encoding=encode, delay=0)
    fileHandlerError.setFormatter(defaultFormat)
    logError.addHandler(fileHandlerError)
    fileHandlerWarn = logging.handlers.RotatingFileHandler('%s/log_%s_warn.log' % (logPath, logDate), mode='a', maxBytes=52428800, backupCount=100, encoding=encode, delay=0)
    fileHandlerWarn.setFormatter(defaultFormat)
    logWarn.addHandler(fileHandlerWarn)


def setLogLevel(level):
    """
    设置日志记录级别
    
    :parameters: * level : Numeric value
                    * CRITICAL : 50
                    * ERROR : 40
                    * WARNING : 30
                    * INFO : 20
                    * DEBUG : 10
                    * NOTSET : 0
    
    """
    logInfo.setLevel(level)
    logDebug.setLevel(level)
    logError.setLevel(level)
    logWarn.setLevel(level)


def setLogOutputFlag(flag):
    """
    设置打开或者关闭控制台输出日志功能
    """
    if flag == True:
        logInfo.addHandler(logStream)
        logDebug.addHandler(logStream)
        logError.addHandler(logStream)
        logWarn.addHandler(logStream)
    else:
        logInfo.removeHandler(logStream)
        logDebug.removeHandler(logStream)
        logError.removeHandler(logStream)
        logWarn.removeHandler(logStream)


def error(msg):
    """
    记录错误级别日志
    """
    msg = strEncodeConvert(msg)
    logError.error(msg)


def warn(msg):
    """
    记录警告级别日志
    """
    msg = strEncodeConvert(msg)
    logWarn.warn(msg)


def info(msg):
    """
    记录信息级别日志
    """
    msg = strEncodeConvert(msg)
    logInfo.info(msg)


def debug(msg):
    """
    记录调试级别日志
    """
    msg = strEncodeConvert(msg)
    logDebug.debug(msg)
# okay decompiling Logger.pyc
