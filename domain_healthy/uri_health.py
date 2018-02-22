#!/win64/python2.7
# -*- coding:UTF-8 -*-
# by xt.
#
# 功能目标：
#   实现批量对域名中的不能访问uri网页的域名的判断，并输出
#   实现对返回页面判断，全文搜索forbidden或apache或IBM或IIS或page not found或...
#   基本逻辑：
#     1. 抓response如果包含缺uri关键字（forbidden或apache或IBM或IIS或page not found或...），直接后追加“可访问无后缀”，满足此条件直接输出并跳出此次查询，不进行下面的操作；
#     2. 所有response都应该判断是否含有title，如果有title则进行输出text，并追加域名后面；
#         如果没有判断有没有h1标签或h2标签，输出h1和h2标签的值（it works页面使用h1,）；
#     3. 如果有title，判断是否存在300+跳转，输出跳转的url，追加“正常访问”，输出url
#     4.
#   实现规范输出，



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

#socket.setdefaulttimeout(10.0)


#function
# -----------------------------------------
# 输出到文本并换行
# -----------------------------------------
def output(texts):
    file_object2 = open(data+'.txt', 'a+')
    file_object2.write("[+]"+time.strftime("%Y%m%d %H:%M:%S ", time.localtime())+texts+'\n')
    file_object2.close()




# ----------------------------------------------------
# 处理http请求
# 输入：url
# 输出：html(str),str(page.getcode())(str)；当无法连接时返回的是"can't connect.","error"
# page:
#   str,页面
# rescode：
#   str,返回http，https状态判断“access”“urlerror”“httperror”
# 全局变量：重定向relocation
# ---------------------------------------------------
def gethttp(reurl_http):
    # 逻辑：尝试不加头部请求，如果不成功则加head头重新请求geturl_multiTry()。
    #reurl_http="http://"+reurl
    print '[+]'+reurl_http+' ',
    output('[+]'+reurl_http)
    req=urllib2.Request(reurl_http)
    #
    # 尝试获取页面，错误则获取错误页面同时调用getUrl_multiTry重试几次，错误则写入文件，正确则返回page
    #
    try:
        #fix:socket timeout.
        timeout = 20
        socket.setdefaulttimeout(timeout)
        # -------------------------
        response=urllib2.urlopen(req,timeout=8)
        page=response.read()
        # output---------
        print 'Response:'+str(response.getcode())+' ',
        res_output="Response:"+str(response.getcode())
        output("[+]"+res_output)
        #--------------------
        #
        # 实例化opener继承class SmartRedirectHandler。获取重定向地址relocation
        #
        # if response.getcode()==300 or response.getcode()==301:
        #     print response.getcode()
            # opener = urllib2.build_opener(SmartRedirectHandler)
            # global relocation
            # relocation=opener.open(reurl_http)
            # print "redirect:"+relocation
            # output("redirect:"+str(relocation))
            # rescode=str(response.getcode())
        #print head
        head=response.info()
        try:
            re_header =head['server']
            print "Server: "+re_header
            server="Server: "+re_header
            output(server)
        except:
            print "\n[-]Header didn't get server."
            output("[-]Header didn't get server.")
        return page,"access" #（等待开发，page通过opener获取，还没有合适的测试站，遇到再说）
    #
    # response error exception reload.
    #
    #
    except HTTPError, e:
        #print 'The server couldn\'t fulfill the request.'
        exr='Error reason: '+str(e.code)
        print exr+' '+e.reason
        output(exr)
        return "can't connect.","httperror"
    except URLError, e:
        #print 'We failed to reach a server.'
        exr='Failed reason: '+str(e.reason)
        print exr
        output(exr)
        return "can't connect.","urlerror"
    # fix bug: socket.timeout: timed out
    except socket.timeout as e:
        #print type(e)    #catched
        print "timeout error catched"
        return "can't connect.","urlerror"


def getping(ip):
    print "[+]Starting ping:"
    backinfo =  os.system('ping -c 1 -w 1 %s'%ip) # 实现pingIP地址的功能，-c1指发送报文一次，-w1指等待1秒
    #print 'backinfo'
    #print backinfo
    #print type(backinfo)
    if backinfo:
        text="[-]Ping error."
        output(text)
        print text
        return "None"
    else:
        text="[+]Ping success."
        output(text)
        print text
        return ip





#
# 加head头重新请求,如果请求成功则返回page，否则将错误写入文件
# 传入：url
# 输出：页面内容str或none
#
def getUrl_multiTry(url):
    user_agent ="Mozilla/5.0 (Windows NT 6.2; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/38.0.2125.122 Safari/537.36"
    headers = { 'User-Agent' : user_agent }
    maxTryNum=6
    html=u"init"
    for tries in range(maxTryNum):
        try:
            req = urllib2.Request(url, headers = headers)
            html=urllib2.urlopen(req).read()
            break
        except Exception,e:
            print e, page.read()
            if tries <(maxTryNum-1):
                continue
            else:
                print "Has tried %d times to access url %s, all failed!" % (maxTryNum,url)
                #html=None
                break
    return html



def writename_check(soup):
    writename=["forbidden","apache","IBM","Page Not Found"]
    try:
        for m in writename:
            check=soup.find(writename[m]).text
            if len(check)!=0:
                print check,
                print "白名单判定服务器开启缺少uri "
                output("白名单判定服务器开启缺少uri"+'\n')
                break
                return 0  #发送个continue指令回传
            else:
                print writename[m]+'check:'+len(check) +"白名单认为不存在于白名单内"
    except:
        print "白名单判定发生错误 "+str(check)+' ',
        output("白名单判定发生错误 "+str(check)+' ')
        pass



def title_check(soup):
    try:
        title=soup.find("title").text
        if len(title)!=0:
            print title,
            print "title存在 ",
            output("title:"+title+' ')
            return 1  #回传title_state=1存在
        elif len(title)==0:
            print "title空 "
            output("title空 ")
            return 0  #回传title_state=0为空
    except:
        print "title出错",
        output("title error! ")
        return 0
        pass

def htag_check(soup):
    try:
        h1tag=soup.find("h1").text
        h2tag=soup.find("h2").text
        if len(h1tag)!=0:
            print h1tag,
            print "h1tag存在 ",
            output("h1tag:"+h1tag+' ')
            return 1  #回传title_state=1存在
        elif len(h2tag)!=0:
            print h1tag,
            print "h1tag存在 ",
            output("h1tag:"+h1tag+' ')
            return 1  #回传title_state=0为空
        else:
            print "htag空 "
            output("htag空 ")
            return 0
    except:
        print "htag出错",
        output("htag error! ")
        return 0
        pass



class SmartRedirectHandler(urllib2.HTTPRedirectHandler):
    RedURLs301 = []
    RedURLs302 = []

    def Getredurl301(self):
        return SmartRedirectHandler.RedURLs301

    def Getredurl302(self):
        return SmartRedirectHandler.RedURLs302

    def http_error_301(self, req, fp, code, msg, headers):
        if headers.has_key("Location"):
            SmartRedirectHandler.RedURLs301.append(headers["Location"])
        result = urllib2.HTTPRedirectHandler.http_error_301(
            self, req, fp, code, msg, headers)
        return result

    def http_error_302(self, req, fp, code, msg, headers):
        if headers.has_key("Location"):
            SmartRedirectHandler.RedURLs302.append(headers["Location"])
        result = urllib2.HTTPRedirectHandler.http_error_302(
            self, req, fp, code, msg, headers)
        return result
#
# 对文件中批量内容过滤获取其中域名或ip部分
#
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
    # try:

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

#main
#实现主逻辑
#   基本逻辑：
#     1. 抓response如果包含缺uri关键字（forbidden或apache或IBM或IIS或page not found或...），直接后追加“可访问无后缀”，满足此条件直接输出并跳出此次查询，不进行下面的操作；
#     2. 所有response都应该判断是否含有title，如果有title则进行输出text，并追加域名后面；
#         如果没有判断有没有h1标签或h2标签，输出h1和h2标签的值（it works页面使用h1,）；
#     3. 如果有title，判断是否存在300+跳转，输出跳转的url，追加“正常访问”，输出url
#
#   实现规范输出，
#输入：under_detection_targets.txt，每行一个域名不包含http/https
#输出：
#读取文件,获取response
def main():
    #
    # 文件读取
    #
    try:
        urllist=open('under_detection_targets.txt','r')
        url_target=urllist.readlines()
        url_target=[n.rstrip("\n") for n in url_target] # fix bug: ValueError: Invalid header value 'https://xxx.com\n'，优化：由于从target中读取的列表都带换行符，这里去掉列表中的"\n"
        #print url_target
        #pdb.set_trace()  #debug
    except:
        print "[!]读取under_detection_targets.txt失败，请确保当前目录存在under_detection_targets.txt且含有内容。"
    for n in url_target:  # n 目标文件中取出的不包含http/https的域名
        #（优化：去除文件中http、https、去除/后面的内容只保留域名）
        n=filter_target(n)
        #
        output(str(n))
        print "Target:"+n
        # ----------------------------
        # 获取请求的页面以及页面状态码
        # 可选项:location(开发阻塞)
        #
        print "n is:"+n
        response_http,pagecode_http=gethttp("http://"+n)
        response_https,pagecode_https=gethttp("https://"+n)
        # ------------------------------------
        #
        # 针对三种返回状态进行处理,得出服务器关闭，无法访问页面，web服务正常，
        # functions
        # ------------------------------------
        #
        # 获取IP
        try:
            ip = socket.gethostbyname(n)
            print "[+]Getip: "+ip
            output("[+]Getip: "+ip)
        except:
            print "[!]Python socket couldn't get IP."
            getip_error="[!]Python socket couldn't get IP."
            output(getip_error)
            pass
        #(后续要补上)
        # ----------------------------
        #
        # 获取ping的情况
        pingstate=getping(n)
        print "end"
        # ---------------------------



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




# debug：正常情况测试
#---------start----------
#print "[D]http debug"
#pdb.set_trace() #debug
# --------end---------------

#-------异常捕获标准-------
# except Exception,e:
#     print 'str(Exception):\t', str(Exception)
#     print "e:\t\t",e
#     print 'str(e):\t\t', str(e)   #用于输出
#     print 'repr(e):\t', repr(e)
#     print 'e.message:\t', e.message
#     print 'traceback.print_exc():'; traceback.print_exc()
#     print 'traceback.format_exc():\n%s' % traceback.format_exc()  #详细
#     print e  #缩略用于判断
