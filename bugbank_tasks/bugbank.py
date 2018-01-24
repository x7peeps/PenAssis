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
#browser=webdriver.PhantomJS() #不行登录处暂时需要
browser.get('https://www.bugbank.cn/signin.html')
browser.find_element_by_name("username").send_keys(username)#input your account
browser.find_element_by_name("password").send_keys(password)# input your password
#time.sleep(10)
time.sleep(5)




def get_cookie():
    #x_cookies = browser.manage().getCookies()
    #print 'get cookies:'+x_cookies
    #return x_cookies
    #get the session cookie


    for item in browser.get_cookies():
        if item["name"]=="AUTH":
            global auth
            auth=str(item["value"])
            print "auth is :"+auth
    #cookie=[item["name"] + ":" + item["value"]]
    cookie = [item["name"] + ":" + item["value"]  for item in browser.get_cookies()]

    #print cookie
    #----------证明cookie是list型-------
    # if type(cookie)==str:
    #     print "cookie is dict"
    # if type(cookie)==list:
    #     print "cookie is list"
    #--------------------------------
    #print "cookie is: "+str(cookie)
    cookiestr = ','.join(item for item in cookie)
    #print "cookiestr is :"+str(cookiestr)
    return cookiestr
# browser.get('https://www.bugbank.cn/task/view.html?tid=5a0bab3b4544b33370ceb2e3')
# link=browser.find_element_by_id('testranges')
# print link

#--------登录之后的head
set_cookie=str(get_cookie())
header={"Host":"www.bugbank.cn",
"User-Agent":"Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/62.0.3202.75 Safari/537.36",
"Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8",
"Accept-Language":"zh-CN,zh;q=0.8,en-US;q=0.5,en;q=0.3",
#"Accept-Charset":"utf-8;q=0.7,*;q=0.7",
#"Accept-Encoding":"gzip, deflate, br",  #压缩导致，request(url,header)乱码
"x-client-id": "user-web",
"X-Requested-With":"XMLHttpRequest",
"Referer":"https://www.bugbank.cn/task/",
"Cookie":set_cookie,
"authorization":"Bearer "+auth
}
#print "header is :"+str(header)





def getHtml(reurl):
    req=urllib2.Request(url=reurl,headers=header)
    #page=urllib2.urlopen(reurl)
    page=urllib2.urlopen(req)
    #print page.read().decode('utf-8')
    html=page.read().decode('utf-8')
    print page.getcode(),
    return html





html=getHtml("https://www.bugbank.cn/api/firmtask?isnew=true")
response=html  #之前是好的，gethtml加了headers导致，decode报错
#response=html
#print response  #test page
#print response.replace(u'\xa0', u' ')
soup=BeautifulSoup(response,'lxml')

#soup.replace(u'\xa0', u' ')
#str(soup).replace(u'\xa0', u' ')
#print soup #带有网页标签，下面过滤
texts=soup.find('p')
#print texts.get_text().encode('utf-8')  #test还是乱码中文，先不管了，直接找web
jsons=texts.get_text().encode('utf-8')
#--------------print to file-----------
# file_object = open('thefile.txt', 'w')
# file_object.write(jsons)
# file_object.close( )
q=json.loads(jsons,"UTF-8")
jsons_list=q["unclaim"]
#jsons_list=jsons_list.encode('utf-8')  #语法错的，这里乱码u\开头
#print jsons_list
# #判断jsons_list是list-------------------
# if type(jsons_list)==list:
#     print "jsons_list is lists"
# ---------------------------------




#建立以时间为名字的txt------------------
data=time.strftime('Bugbank '+'%Y-%m-%d',time.localtime(time.time()))
file_object = open(data+'.txt','w')
file_object.close()
#------------------------





for lists in jsons_list:
    #lists=lists.replace("'", "\"")
    #s=json.loads(lists,"UTF-8")
    #-----------lists 是字典-------------
    # if type(lists)==dict:
    #     print "lists is dict.."
    # #print lists['firm']
    #----------------------------------
    tmp=lists['firm']
    tmp=json.dumps(tmp,encoding='utf-8',ensure_ascii=False)
    tmp=eval(tmp)
    #print tmp
    hosts=tmp['website']
    #dayin
    file_object = open(data+'.txt', 'a+')
    #file_object= open(str(time.time()),"a")
    file_object.write(hosts+'\n')
    file_object.close()
    print hosts
    #----这里想要规范hosts输出格式，去掉乱码的，有的在加上http或https
    #-----
