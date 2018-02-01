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




#init
# 初始化utf-8编码
reload(sys)
sys.setdefaultencoding('utf-8')
# 创建输出文件
data=time.strftime('urlcheck '+'%Y-%m-%d',time.localtime(time.time()))
file_object = open(data+'.txt','w')
file_object.close()
http_mark=0
https_mark=1





#function
# 输出到文本并换行
def output(texts):
    file_object2 = open(data+'.txt', 'a+')
    file_object2.write(texts+'\n')
    file_object2.close()

def gethttp(reurl):
    # head头初始化
    #
    try:
        #test http
        reurl_http="http://"+reurl
        print '[|]'+reurl_http+' ',
        try:
            req=urllib2.Request(reurl_http)
            page=urllib2.urlopen(req)
        except:
            header_http={"Host": reurl_http,
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:59.0) Gecko/20100101 Firefox/59.0"
            ,"Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8",
            "Accept-Language": "zh-CN",
            "Accept-Encoding": "gzip, deflate",
            #"Referer": "http://target.com/something_referer",
            "Content-Type": "application/x-www-form-urlencoded",
            "Connection": "close",
            "Upgrade-Insecure-Requests": "1"}
            req=urllib2.Request(url=reurl_http,headers=header_http)
            page=urllib2.urlopen(req)
        html=page.read().decode('utf-8')
        print 'http:'+str(page.getcode())+' '+'\n',
        http_output="http: "+str(page.getcode())
        output(http_output)
        return html,http_mark,page.getcode()
    except:
        traceback.print_exc()
        # info=sys.exc_info()
        # print info[0],":",info[1],#,'\n'
        # print 'str(Exception):\t', str(Exception)
        # print 'str(e):\t\t', str(e)
        # print 'repr(e):\t', repr(e)
        # print 'e.message:\t', e.message
        # print 'traceback.print_exc():', traceback.print_exc()
        # print 'traceback.format_exc():\n%s' % traceback.format_exc()
        # return "error",http_mark,page.getcode()
        pass
    # except urllib2.URLError, e:
    #     print e.code

def gethttps(reurl):
    try:
        #test https
        reurl_https="https://"+reurl
        print '[|]'+reurl_https+' ',
        try:
            reqs=urllib2.Request(reurl_https)
            pages=urllib2.urlopen(reqs)
        except:
            header_https={"Host": reurl_https,
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:59.0) Gecko/20100101 Firefox/59.0"
            ,"Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8",
            "Accept-Language": "zh-CN",
            "Accept-Encoding": "gzip, deflate",
            #"Referer": "http://target.com/something_referer",
            "Content-Type": "application/x-www-form-urlencoded",
            "Connection": "close",
            "Upgrade-Insecure-Requests": "1"}
            reqs=urllib2.Request(url=reurl_https,headers=header_https)
            pages=urllib2.urlopen(reqs)
        htmls=pages.read().decode('utf-8')
        print 'https:'+str(pages.getcode())+' ', #打印
        https_output="https:"+str(pages.getcode())
        output(https_output)
        return htmls,https_mark,pages.getcode()
    except:
        traceback.print_exc()
        # info=sys.exc_info()
        # print info[0],":",info[1],#,'\n'
        # print 'str(Exception):\t', str(Exception)
        # print 'str(e):\t\t', str(e)
        # print 'repr(e):\t', repr(e)
        # print 'e.message:\t', e.message
        # print 'traceback.print_exc():', traceback.print_exc()
        # print 'traceback.format_exc():\n%s' % traceback.format_exc()
        # https_output="httpserror:"+str(pages.getcode())
        # output(https_output)
        #return "error",https_mark,pages.getcode()
        pass
    # except urllib2.URLError, e:
    #     print e.code

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







#main
#实现主逻辑
#   基本逻辑：
#     1. 抓response如果包含缺uri关键字（forbidden或apache或IBM或IIS或page not found或...），直接后追加“可访问无后缀”，满足此条件直接输出并跳出此次查询，不进行下面的操作；
#     2. 所有response都应该判断是否含有title，如果有title则进行输出text，并追加域名后面；
#         如果没有判断有没有h1标签或h2标签，输出h1和h2标签的值（it works页面使用h1,）；
#     3. 如果有title，判断是否存在300+跳转，输出跳转的url，追加“正常访问”，输出url
#     4.
#   实现规范输出，
#读取文件,获取response
if __name__ == '__main__':
    try:
        urllist=open('under_detection_targets.txt','r')
        url_target=urllist.readlines()
    except:
        print "[!]读取under_detection_targets.txt失败，请确保当前目录存在under_detection_targets.txt且含有内容。"
    for n in url_target:
        output(str(n)+' ')
        print "[+]Target:"+n+'\n'
        try:
            response_http,connect_mark_http,pagecode_http=gethttp(n)
            if response_http=="error":
                print "[!]http connection error. \n"
            #print response_http,connect_mark_http,pagecode_http,
        except:
            pass   #继续下一个

        else:
            response_https,connect_mark_https,pagecode_https=gethttps(n)
            # if response_https=="error":
            #     print "[!]https connection error. \n"
            #print response_https,connect_mark_https,pagecode_https,
        finally:
            pass   #继续下一个
        #connect_markde的值0-http,1-https
        #
        # 内容检测部分
        soup_http=BeautifulSoup(response_http,'lxml')
        soup_https=BeautifulSoup(response_https,'lxml')
        # 符合白名单的直接标记无uri
        state_http=writename_check(soup_http)
        state_https=writename_check(soup_https)
        if state_http==0 or state_https==0:
            continue
        # title判定
        title_state_http=title_check(soup_http)
        title_state_https=title_check(soup_https)
        if title_state_http==1 or title_state_https==1:
            if (title_state_http==1 and pagecode_http==200) or (title_state_https==1 and pagecode_https==200):
                output("访问正常"+'\n')
            elif (title_state_http==0 and pagecode_http==200) or (title_state_https==0 and pagecode_https==200):
                try:
                    htag_state_http=htag_check(soup_http)
                    htag_state_https=htag_check(soup_https)
                    if htag_state_http==0 or htag_state_https==0:
                        continue
                except:
                    pass
        elif (re(pagecode_http,r"30[0-9]") or re(pagecode_https,r"30[0-9]")):
            #获取跳转之后的url
            res = requests.head(url)
            location=res.headers['Location']
            output("可访问跳转"+location+'\n')
        else:
            print 'continue.\n'
