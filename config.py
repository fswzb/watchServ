#!python
#-*-coding:utf-8 -*-
'''
    如果有更新，最迟10s会自动重新加载此文件
'''

# 发送邮件的配置，分别是：邮件服务器域名，端口，登录邮箱账号，密码
mailServer = 'foxmail.com'
mailPort = 25
mailUser = 'workforit@foxmail.com'
mailPasswd = 'atajcfktwoaybcdc'
mailDebug = 1
mailCopyTo = 'hujintao77@126.com'

# 调试等级
# CRITICAL = 50
# FATAL = CRITICAL
# ERROR = 40
# WARNING = 30
# WARN = WARNING
# INFO = 20
# DEBUG = 10
# NOTSET = 0
logLevel = 10
# 日志文件路径
logFile = 'daemon.log'
# 日志输出模式：0 表示输出到标准输出；1表示到日志文件
LOGMODE_STDOUT = 0
LOGMODE_FILE = 1
logMode = LOGMODE_FILE
