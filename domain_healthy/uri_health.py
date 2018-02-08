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
import urllib,urllib2
from bs4 import BeautifulSoup
import time
import sys
import traceback    #需要导入traceback模块，此时获取的信息最全
import requests
import re
import pdb


# 解决https报错：<urlopen error [SSL: CERTIFICATE_VERIFY_FAILED] certificate verify failed (_ssl.c:661)>，全局证书关闭
import ssl
ssl._create_default_https_context = ssl._create_unverified_context
# import requests.packages.urllib3.util.ssl_
# requests.packages.urllib3.util.ssl_.DEFAULT_CIPHERS = 'ALL'
# ssl_version=ssl.PROTOCOL_TLSv1
# from urllib3.contrib import pyopenssl
# pyopenssl.inject_into_urllib3()


#init
# 初始化utf-8编码
reload(sys)
sys.setdefaultencoding('utf-8')
# 创建输出文件
data=time.strftime('urlcheck '+'%Y-%m-%d',time.localtime(time.time()))
file_object = open(data+'.txt','w')
file_object.close()




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
        response=urllib2.urlopen(req,timeout=18)
        page=response.read()
        # output---------
        print 'rescode:'+str(response.getcode())+' '+'\n',
        res_output="rescode:"+str(response.getcode())
        output("[+]"+res_output)
        #
        # 实例化opener继承class SmartRedirectHandler。获取重定向地址relocation
        #
        if response.getcode()==300 or response.getcode()==301:
            opener = urllib2.build_opener(SmartRedirectHandler)
            global relocation
            relocation=opener.open(reurl_http)
            print "redirect:"+relocation
            output("redirect:"+str(relocation))
        return page,str(response.getcode())
    except Exception,e:
        print "ResponseError:",
        #当使用不安全的sslv3连接的时候，<urlopen error [SSL: SSLV3_ALERT_HANDSHAKE_FAILURE] sslv3 alert handshake failure (_ssl.c:661)>，则报使用了不受支持的协议。
        if str(e)=="<urlopen error [SSL: SSLV3_ALERT_HANDSHAKE_FAILURE] sslv3 alert handshake failure (_ssl.c:661)>":
            e="Using SSLv3 not secure.[SSL: SSLV3_ALERT_HANDSHAKE_FAILURE]"
        elif str(e)=="<urlopen error [Errno 10061] >" or str(e)=="<urlopen error [Errno 10060] >":
            e="Connecttion refused.[Errno 10060]"
        elif str(e)=="<urlopen error [Errno 11001] getaddrinfo failed>"
            e="Cannot visit, no ip can't get host."
        print e
        output("[+]ResponseError:"+str(e))
        return "can't connect.","error"  #防止nonetype回传











#
# 加head头重新请求,如果请求成功则返回page，否则将错误写入文件
# 传入：url
# 输出：页面内容str或none
#
def getUrl_multiTry(url):
    user_agent ="Mozilla/5.0 (Windows NT 6.2; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/38.0.2125.122 Safari/537.36"
    #"Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:59.0) Gecko/20100101 Firefox/59.0"
    #
    # header_http={"Host": reurl_http,
    # "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:59.0) Gecko/20100101 Firefox/59.0"
    # ,"Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8",
    # "Accept-Language": "zh-CN",
    # "Accept-Encoding": "gzip, deflate",
    # #"Referer": "http://target.com/something_referer",
    # "Content-Type": "application/x-www-form-urlencoded",
    # "Connection": "close",
    # "Upgrade-Insecure-Requests": "1"}
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
if __name__ == '__main__':
    #
    # 文件读取
    #
    try:
        urllist=open('under_detection_targets.txt','r')
        url_target=urllist.readlines()
        url_target=[n.rstrip("\n") for n in url_target] ##fix bug: ValueError: Invalid header value 'https://xxx.com\n'，优化：由于从target中读取的列表都带换行符，这里去掉列表中的"\n"
        #print url_target
        #pdb.set_trace()  #debug
    except:
        print "[!]读取under_detection_targets.txt失败，请确保当前目录存在under_detection_targets.txt且含有内容。"
    for n in url_target:
        output(str(n))
        print "[+]Target:"+n
        #
        # 连接并接收http请求
        #
        #pdb.set_trace()#debug
        #
        # 获取请求的页面以及页面状态码
        # 可选项:location
        #
        response_http,pagecode_http=gethttp("http://"+n)
        response_https,pagecode_https=gethttp("https://"+n)
        #
        # 获取ping的情况
        #
        #
        #pingcheck(n)
        print "end"




        #
        # print type(response_https)
        # print response_https
        # if response_https=="error":
        #     print "[!]https connection error. \n"
        # # print response_https,connect_mark_https,pagecode_https,
        #
        # #connect_markde的值0-http,1-https
        # #
        # # 内容检测部分
        # soup_http=BeautifulSoup(response_http,'lxml')
        # soup_https=BeautifulSoup(response_https,'lxml')
        # # 符合白名单的直接标记无uri
        # state_http=writename_check(soup_http)
        # state_https=writename_check(soup_https)
        # if state_http==0 or state_https==0:
        #     continue
        # # title判定
        # title_state_http=title_check(soup_http)
        # title_state_https=title_check(soup_https)
        # if title_state_http==1 or title_state_https==1:
        #     if (title_state_http==1 and pagecode_http==200) or (title_state_https==1 and pagecode_https==200):
        #         output("访问正常"+'\n')
        #     elif (title_state_http==0 and pagecode_http==200) or (title_state_https==0 and pagecode_https==200):
        #         try:
        #             htag_state_http=htag_check(soup_http)
        #             htag_state_https=htag_check(soup_https)
        #             if htag_state_http==0 or htag_state_https==0:
        #                 continue
        #         except:
        #             pass
        # elif (re(pagecode_http,r"30[0-9]") or re(pagecode_https,r"30[0-9]")):
        #     #获取跳转之后的url
        #     res = requests.head(url)
        #     location=res.headers['Location']
        #     output("可访问跳转"+location+'\n')
        # else:
        #     print 'continue.\n'

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
