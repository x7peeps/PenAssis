#!/win64/python2.7
# -*- coding:UTF-8 -*-
# Author: Fighting Bear XT. 张续腾
#
# 准备引入谷歌代码规范：http://zh-google-styleguide.readthedocs.io/en/latest/google-python-styleguide/python_language_rules/
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
import ssl
ssl._create_default_https_context = ssl._create_unverified_context # 解决https报错：<urlopen error [SSL: CERTIFICATE_VERIFY_FAILED] certificate verify failed (_ssl.c:661)>，全局证书关闭
import socket
import os
from threading import Thread
from ssl import SSLError
from gevent import monkey
monkey.patch_socket()
# import argparse
import thread
from colorama import init,Fore
import getopt
from requests import ReadTimeout, ConnectTimeout, HTTPError, Timeout, ConnectionError


##
# 待优化，如果存在7001端口，还应该尝试连接7001端口探测weblogic

#init
# 初始化utf-8编码
reload(sys)
sys.setdefaultencoding('utf-8')
# 创建输出文件
data=time.strftime('urlcheck '+'%Y-%m-%d',time.localtime(time.time()))
file_object = open(data+'.txt','w')
file_object.close()
# 设置线程数
# 从文档targets.txt中读取各种格式的URL




# main主逻辑
def main():
    # 文件读取
    #print 'main test:'+inner_url
    try:
        urllist=open('targets.txt','r')
        url_target=urllist.readlines()
        url_target=[n.rstrip("\n") for n in url_target]
    except:
        print "[!]读取under_detection_targets.txt失败，请确保当前目录存在targets.txt且含有内容。"
    for n in url_target:  # n 目标文件中取出的不包含http/https的域名
        #（优化：去除文件中http、https、去除/后面的内容只保留域名）
        n=filter_target(n)
        output(str(n))
        print "Target:"+n
        # t=Thread(target=work)
        # t.start()
        # t.join()
        try:
            response_http,pagecode_http=gethttp("http://"+n)
        except:
            print Fore.RED+'Get http ERROR.'
            pass
        try:
            response_https,pagecode_https=gethttp("https://"+n)
        except:
            print Fore.RED+'Get https ERROR.'
            pass



#
# 对文件中批量内容过滤获取其中域名或ip部分
#
def filter_target(url):
    try:
        url=url.split("//")[1]
    except:
        pass
    try:
        url=url.split(":")[0]
    except:
        pass
    try:
        url=url.split("/")[0]
    except:
        pass
    try:
        proto, rest = urllib.splittype(url)
        host, rest = urllib.splithost(rest)
        host, port = urllib.splitport(host)
        return host
    except:
        return url




# 获取域名并探测
def gethttp(reurl_http):
    # 逻辑：尝试不加头部请求，如果不成功则加head头重新请求geturl_multiTry()。
    # reurl_http="http://"+reurl
    print Fore.BLUE+'[+]'+reurl_http+' ',
    output('[+]'+reurl_http)
    headers = {'User-agent' : 'Mozilla/5.0 (Windows NT 6.2; WOW64; rv:22.0) Gecko/20100101 Firefox/22.0'}
    req=urllib2.Request(reurl_http, headers = headers)
    #
    # 尝试获取页面，错误则获取错误页面同时调用getUrl_multiTry重试几次，错误则写入文件，正确则返回page
    #
    try:
        timeout = 20
        socket.setdefaulttimeout(timeout)
        # -------------------------
        #response=urllib2.urlopen(req,timeout=5) #bug thread error 1
        response=urllib2.urlopen(req,timeout=5)
        page=response.read()
        pagecode=str(response.getcode())
        # output---------
        print Fore.YELLOW+'Response:'+pagecode+' ',
        res_output="Response:"+pagecode
        output("[+]"+res_output)
        head=response.info()
        try:
            re_header =head['server']
            print Fore.GREEN+"Server: "+re_header
            server="Server: "+re_header
            output(server)
        except:
            print Fore.BLUE+"\n[-]Header didn't get server."
            output("[-]Header didn't get server.")
        return page,pagecode
    #    return page,"access" #（等待开发，page通过opener获取，还没有合适的测试站，遇到再说）
    #
    # response error exception reload.
    #
    #
    except HTTPError, e:
        #print 'The server couldn\'t fulfill the request.'
        exr='Error reason: '+str(e.code)
        print Fore.RED+exr+' '+e.reason
        output('[-]'+exr)
        return "can't connect.","httperror"
    except URLError, e:
        #print 'We failed to reach a server.'
        exr='Failed reason: '+str(e.reason)
        print Fore.RED+exr
        output('[-]'+exr)
        return "can't connect.","urlerror"
    # fix bug: socket.timeout: timed out
    except socket.timeout as e:
        #print type(e)    #catched
        print Fore.RED+"timeout error catched"
        return "can't connect.","urlerror"
    except (SSLError, socket.timeout) as error:
        err_s = str(error)
        if 'operation timed out' in err_s:
            print Fore.RED+("ssl operation timed out")
            raise
        raise NetworkError(err_s)
    print Fore.WHITE






def ite_ip(ip):
    for i in range(1, 256):
        final_ip = '{ip}.{i}'.format(ip=ip, i=i)
        print final_ip
        thread.start_new_thread(weblogic_ssrf_scan, (final_ip,))
        time.sleep(3)




# 结果保存到新的文档中
def output(texts):
    file_object2 = open(data+'.txt', 'a+')
    file_object2.write("[+]"+time.strftime("%Y%m%d %H:%M:%S ", time.localtime())+texts+'\n')
    file_object2.close()




# 主流程调用，并引入中断
if __name__ == '__main__':
    # # 计划：增加程序参数 -p,-proxy
    # parser = argparse.ArgumentParser(description='Weblogic SSRF vulnerable exploit')
    # # parser.add_argument('--proxy', dest='proxy', required=True, help='Use proxy.')
    # parser.add_argument('--inner', dest='inner', required=True, help='Inner url')
    # args=parser.parse_args()
    # print args
    # inner_url=args['inner']
    argv1=sys.argv[1:]
    # print argv1
    global inner_url
    inner_url=''
    try:
        opts, args = getopt.getopt(argv1,"hi:",["innerurl="])
        # print opts
        # print args
    except getopt.GetoptError:
        print 'test.py -i <innerurl>'
        sys.exit(2)
    for opt, arg in opts:
        if opt == '-h':
            print 'test.py -i <innerurl>'
            sys.exit()
        elif opt in ("-i", "--innerurl"):
            inner_url = arg
            #print inner_url
        # elif opt in ("-o", "--ofile"):
        #     outputfile = arg
    # ----------------------------------------
    # add: 中断，在主程序运行过程中可随时键盘中断
    #
    class CountDown(Thread):
        def __init__(self):
            super(CountDown, self).__init__()
        def run(self):
            print('slave start')
            # --------------
            # 主函数start
            main()
            # --------------
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
