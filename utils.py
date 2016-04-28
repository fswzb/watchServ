#!python
#-*-coding:utf-8 -*-
'''
'''

import chardet
import logging

def strToUTF8(strInput):
    if not strInput:
        return ''
    try:
        encode = chardet.detect(strInput)
        encoding = encode['encoding']
        if encode['confidence'] > 0.8 and encoding.lower() != 'utf-8' \
           and encoding.lower() != 'ascii':
            return strInput.decode(encoding).encode('utf-8')
    except Exception, e:
        logging.debug(str(e))
        return strInput
    return strInput
