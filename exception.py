#!python
#-*-coding:utf-8 -*-
'''
    自定义异常类，插件在抛出异常时，以抛出的字符串为邮件标题和内容
'''

class WatchError(Exception):
    def __init__(self, subject, content):
        self.subject = subject
        self.content = content
    def __str__(self):
        return "subject: %s\ncontent:%s\n" % (self.subject, self.content)
