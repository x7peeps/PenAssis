#coding=utf-8
import urllib2
from bs4 import BeautifulSoup
import sys
reload(sys)
sys.setdefaultencoding('utf-8')
import json
import time


"""
> configure your accounts and password.
"""
username="account here"   #your bugbank account
password="password here"   #your bugbank password



#--------------登录用head
#调用webdriver自动登录
from selenium import webdriver
import time
browser = webdriver.Chrome()
browser.get('https://www.bugbank.cn/signin.html')
browser.find_element_by_name("username").send_keys(username)#input your account
browser.find_element_by_name("password").send_keys(password)# input your password
time.sleep(5)




def get_cookie():
    for item in browser.get_cookies():
        if item["name"]=="AUTH":
            global auth
            auth=str(item["value"])
            print "auth is :"+auth
    cookie = [item["name"] + ":" + item["value"]  for item in browser.get_cookies()]
    cookiestr = ','.join(item for item in cookie)
    return cookiestr

#--------登录之后的head
set_cookie=str(get_cookie())
header={"Host":"www.bugbank.cn",
"User-Agent":"Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/62.0.3202.75 Safari/537.36",
"Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8",
"Accept-Language":"zh-CN,zh;q=0.8,en-US;q=0.5,en;q=0.3",
"x-client-id": "user-web",
"X-Requested-With":"XMLHttpRequest",
"Referer":"https://www.bugbank.cn/task/",
"Cookie":set_cookie,
"authorization":"Bearer "+auth
}






def getHtml(reurl):
    req=urllib2.Request(url=reurl,headers=header)
    page=urllib2.urlopen(req)
    html=page.read().decode('utf-8')
    print page.getcode(),
    return html





html=getHtml("https://www.bugbank.cn/api/firmtask?isnew=true")
response=html 
soup=BeautifulSoup(response,'lxml')
texts=soup.find('p')
jsons=texts.get_text().encode('utf-8')
#--------------print to file-----------
q=json.loads(jsons,"UTF-8")
jsons_list=q["unclaim"]





#建立以时间为名字的txt------------------
data=time.strftime('Bugbank '+'%Y-%m-%d',time.localtime(time.time()))
file_object = open(data+'.txt','w')
file_object.close()
#------------------------





for lists in jsons_list:
    tmp=lists['firm']
    tmp=json.dumps(tmp,encoding='utf-8',ensure_ascii=False)
    tmp=eval(tmp)
    hosts=tmp['website']
    file_object = open(data+'.txt', 'a+')
    file_object.write(hosts+'\n')
    file_object.close()
    print hosts
