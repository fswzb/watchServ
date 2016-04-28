#!python
#-*- coding:utf-8 -*-
'''
    daemon进程，读取 cmds 下的命令并为每一个配置项新建一个线程；
    在按照指定时间需要执行测试命令时，线程新建进程并判断执行状况
    如果出现返回值不是0或者有输出，就发送邮件到指定邮箱
    否则休眠指定时间，等待下次执行；
    注意不能捕捉 SIG_CHILD 信号
'''

import os,sys,signal
import config
import cmds
from subprocess import Popen,PIPE
import threading
import time
import logging
import sendMail
import random

# 初始化日志模块
def initLogging():
    global logging
    if config.logMode == config.LOGMODE_FILE:
        logging.basicConfig(level=config.logLevel,
                        format='%(asctime)s %(levelname)s %(filename)s %(funcName)s \
%(lineno)d [%(thread)d]:%(message)s',
                        datefmt = '%Y-%m-%d %H:%M:%S',
                        filename=config.logFile,
                        filemode='ab+')
    else:
        logging.basicConfig(level=config.logLevel,
                        format='%(asctime)s %(levelname)s %(filename)s %(funcName)s \
%(lineno)d [%(thread)d]:%(message)s',
                        datefmt = '%Y-%m-%d %H:%M:%S')



# 修复命令执行时间不能超过 execTime
def runFixCmd(fixCmd, execTime):
    execTime = int(execTime)
    if execTime <= 0 or not fixCmd.strip():
        return '', ''
    process = Popen(fixCmd, bufsize = 4096, shell = True, stdout = PIPE, stderr = PIPE)
    maxExecTime = execTime - 1
    for i in range(execTime):
        if i >= maxExecTime:
            process.kill()
            return 'fixCmd runned %d seconds and still not completed, kill it' % maxExecTime, ''
        ret = process.poll()
        if ret is not None:
            output = process.stdout.read()
            errout = process.stderr.read()
            return output, errout
        time.sleep(1)


# 执行线程；定期运行 cmd，如果失败运行 fixCmd
def watchCmd(toEmail, timeInterval, cmd, dealOutput, fixCmd, maxErrTime = 5):
    # 缺少配置项则直接返回
    timeInterval = timeInterval if timeInterval > 0 else random.randint(10,60)
    if not toEmail or not cmd:
        logging.error('cmd configuration error: %s' % cmd)
        return 1
    logging.debug('timeInterval: %d, cmd: %s' % (timeInterval, cmd))
    errTime = 0
    while 1:
        # 出错次数太多则停止1个小时不监视
        if errTime >= maxErrTime:
            logging.warning('stop watch for 3600 seconds: %s' % cmd)
            time.sleep(3600)
            break
        process = Popen(cmd, bufsize = 4096, shell = True, stdout = PIPE, stderr = PIPE)
        waitTime = 0
        ret = 0
        while 1:
            if waitTime >= timeInterval:
                subject = 'execute too long'
                content = 'cmd[%s] execute longer than %d seconds' % (cmd, timeInterval)
                logging.warning('cmd[%s] execute longer than %d seconds' % (cmd, timeInterval))
                if fixCmd.strip():
                    fixOutput, fixErrout = runFixCmd(fixCmd, timeInterval)
                    content = '%s\r\nrun fixCmd: %s\r\nstdout:%s\r\nstderr:%s' % (content, fixCmd, fixOutput, fixErrout)
                sendMail.sendMail(toEmail, subject, content)
                # 杀掉进程
                process.kill()
                errTime += 1
                break
            ret = process.poll()
            if ret is None:
                time.sleep(1)
                waitTime += 1
            else:
                break
        if waitTime >= timeInterval:
            continue
        if dealOutput != 0:
            output = process.stdout.read()
            output = output.strip()
        else:
            output = ''
        errout = process.stderr.read()
        errout = errout.strip()
        # 返回值非0或者有输出则发送邮件
        if ret != 0 or output or errout:
            subject = 'test cmd has output'
            content = 'cmd: %s\r\nreturn: %d\r\noutput:\r\n%s\r\nerrout:\r\n%s' % (cmd, ret, output, errout)
            if fixCmd.strip():
                fixOutput, fixErrout = runFixCmd(fixCmd, timeInterval)
                content = '%s\r\nrun fixCmd: %s\r\nstdout:%s\r\nstderr:%s' % (content, fixCmd, fixOutput, fixErrout)
            sendMail.sendMail(toEmail, subject, content)
            errTime += 1
        logging.debug('sleep %d seconds' % timeInterval)
        time.sleep(timeInterval)
        

# 重启自身进程
def restart_program():  
    """Restarts the current program. 
    Note: this function does not return. Any cleanup action (like 
    saving data) must be done before calling this function."""  
    python = sys.executable
    os.execl(python, python, * sys.argv)


def main():
    initLogging()
    for cmd in cmds.cmds:
        th = threading.Thread(target=watchCmd, args = cmd)
        #th.setDaemon(True)
        th.start()
    cmdConfStat = os.stat('cmds.py')
    cmdStartTime = int(cmdConfStat.st_mtime)
    confConfStat = os.stat('config.py')
    confStartTime = int(confConfStat.st_mtime)
    # 每隔10s检查配置文件是否有更新，有的话自动重启进程
    while threading.active_count() > 1:
        cmdConfStat = os.stat('cmds.py')
        cmdModifyTime = int(cmdConfStat.st_mtime)
        confConfStat = os.stat('config.py')
        confModifyTime = int(confConfStat.st_mtime)
        if cmdModifyTime > cmdStartTime or confModifyTime > confStartTime:
            logging.info('restart %s\n' % sys.argv[0])
            restart_program()
        time.sleep(10)


if __name__ == '__main__':
    main()
