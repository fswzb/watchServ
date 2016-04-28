#!python
#-*- coding: utf-8 -*-
'''
    发送邮件
'''

import smtplib
#from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.header import Header
from config import mailServer,mailPort,mailUser,mailPasswd,mailDebug,mailCopyTo
import logging
from utils import strToUTF8

def sendMail(toEmail, sub, content):
    sub = strToUTF8(sub)
    content = strToUTF8(content)
    msg = MIMEText(content, _subtype='plain', _charset='utf-8')
    msg['Subject'] = Header(sub, 'utf-8')
    msg['From'] = mailUser
    msg['To'] = toEmail
    msg['Bcc'] = mailCopyTo
    msg = msg.as_string()
    server = smtplib.SMTP(mailServer, mailPort)
    
    server.set_debuglevel(mailDebug)
    server.starttls()
    server.login(mailUser, mailPasswd)
    logging.debug('*' * 20)
    logging.debug('\nfrom: %s, to: %s, msg: %s' % (mailUser, toEmail, msg))
    logging.debug('*' * 20)
    server.sendmail(mailUser, toEmail, msg)
    server.close()

if __name__ == '__main__':
    import sys
    if len(sys.argv) < 4:
        print('Usage: %s toMailAddress title content' % sys.argv[0])
        sys.exit(0)
    sendMail(sys.argv[1], sys.argv[2], sys.argv[3])
