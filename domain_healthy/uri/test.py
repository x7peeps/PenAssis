#!/win64/python2.7
# -*- coding:UTF-8 -*-
import urllib,urllib2
from bs4 import BeautifulSoup
import time
import sys
import traceback    #需要导入traceback模块，此时获取的信息最全
import requests
import re
import pdb
from urllib2 import Request, urlopen, URLError, HTTPError
import socket
# 解决https报错：<urlopen error [SSL: CERTIFICATE_VERIFY_FAILED] certificate verify failed (_ssl.c:661)>，全局证书关闭
import ssl
ssl._create_default_https_context = ssl._create_unverified_context
# import requests.packages.urllib3.util.ssl_
# requests.packages.urllib3.util.ssl_.DEFAULT_CIPHERS = 'ALL'
# ssl_version=ssl.PROTOCOL_TLSv1
# from urllib3.contrib import pyopenssl
# pyopenssl.inject_into_urllib3()
import socket
import os
from threading import Thread

#init
# 初始化utf-8编码
reload(sys)
sys.setdefaultencoding('utf-8')
# 创建输出文件
data=time.strftime('urlcheck '+'%Y-%m-%d',time.localtime(time.time()))
file_object = open(data+'.txt','w')
file_object.close()



def output(texts):
    file_object2 = open(data+'.txt', 'a+')
    file_object2.write(texts+'\n')
    file_object2.close()

def filter_target(url):
	try:
	    url=url.split("//")[1]
	    #print "remove //: "+url
	except:
	    pass
	try:
	    url=url.split(":")[0]
	    #print "remove :: "+url
	except:
	    pass
	try:
	    url=url.split("/")[0]
	    #print "remove /: "+url
	except:
	    pass
	try:
	    proto, rest = urllib.splittype(url)
	    host, rest = urllib.splithost(rest)
	    #print "1:"+host
	    host, port = urllib.splitport(host)
	    #print "2:"+host
	    return host
	except:
	    #print url,type(url)
	    return url


def main():
    #
    # 文件读取
    #
    try:
        urllist=open('target.txt','r')
        url_target=urllist.readlines()
        url_target=[n.rstrip("\n") for n in url_target] # fix bug: ValueError: Invalid header value 'https://xxx.com\n'，优化：由于从target中读取的列表都带换行符，这里去掉列表中的"\n"
    except:
        print "[!]读取under_detection_targets.txt失败，请确保当前目录存在under_detection_targets.txt且含有内容。"
    for n in url_target:  # n 目标文件中取出的不包含http/https的域名
        #（优化：去除文件中http、https、去除/后面的内容只保留域名）
        n=filter_target(n)
        output(str(n))
        print "Target:"+n


if __name__ == '__main__':
    # ----------------------------------------
    # add: 中断，在主程序运行过程中可随时键盘中断
    #
    class CountDown(Thread):
        def __init__(self):
            super(CountDown, self).__init__()
        def run(self):
            print('slave start')
            main()
            print('slave end')
    print('[!]KeyboardInterrupt started listen.')
    td = CountDown()
    td.setDaemon(True)
    td.start()
    try:
        while td.isAlive():
            pass
    except KeyboardInterrupt:
        print('stopped by keyboard')
    print('[!]KeyboardInterrupt quited listen')
    #-------------------------------------
