#!/win64/python2.7
# -*- coding:UTF-8 -*-
# Author: Fighting Bear XT.
# File: method_test.py

import urllib
import urllib2
import httplib
import sys,time
import getopt
from threading import Thread
from colorama import init,Fore
from urllib2 import Request, urlopen, URLError, HTTPError
import socket
from ssl import SSLError
import ssl

# 全局取消证书
ssl._create_default_https_context = ssl._create_unverified_context
# 创建输出文件
data=time.strftime('urlcheck '+'%Y-%m-%d',time.localtime(time.time()))
file_object = open(data+'.txt','w')
file_object.close()
# 初始化utf-8编码
reload(sys)
sys.setdefaultencoding('utf-8') #gbk 也乱码


# fix bug: IncompleteRead: IncompleteRead(5263 bytes read)-----
httplib.HTTPConnection._http_vsn = 10  
httplib.HTTPConnection._http_vsn_str = 'HTTP/1.0'  
#------


def http_get(url):  
    request = urllib2.Request(url)  
    request.get_method = lambda:'GET'           # 设置HTTP的访问方式  
    request = urllib2.urlopen(request,timeout=20)  
    reqback=request.read()    
    request.close()#记得要关闭
    return reqback

def http_options(url):     
    request = urllib2.Request(url)  
    request.get_method = lambda:'OPTIONS'           # 设置HTTP的访问方式  
    request = urllib2.urlopen(request,timeout=20)  
    reqback=request.read()    
    request.close()#记得要关闭
    return reqback

def http_trace(url):     
    request = urllib2.Request(url)  
    request.get_method = lambda:'TRACE'           # 设置HTTP的访问方式  
    request = urllib2.urlopen(request,timeout=20) 
    reqback=request.read()    
    request.close()#记得要关闭
    return reqback

def http_put(url):   
	url = url+'/hEaD.txt'
	request = urllib2.Request(url) #,headers= headers)  
	request.get_method = lambda:'PUT'           # 设置HTTP的访问方式  
	request = urllib2.urlopen(request,timeout=20)
	reqback=request.read()
	request.close() #记得要关闭
	return reqback

def http_delete(url):  
    url=url+'/hEaD.txt'  
    request = urllib2.Request(url)
    #request.add_header('Content-Type', 'your/conntenttype')  
    request.get_method = lambda:'DELETE'        # 设置HTTP的访问方式  
    request = urllib2.urlopen(request,timeout=20) 
    reqback=request.read()    
    request.close()#记得要关闭
    return reqback


# 结果保存到新的文档中
def output(texts):
    file_object2 = open(data+'.txt', 'a+')
    file_object2.write("[+]"+time.strftime("%Y%m%d %H:%M:%S ", time.localtime())+texts+'\n')
    file_object2.close()


def method_test(url):
	# print url
#test GET
	try:
		print 'GET: ',
		resg = http_get(url)
		print Fore.GREEN+'success...',
		#output(resg) #不保存get的页面
	except HTTPError, e:
	    #print 'The server couldn\'t fulfill the request.'
	    exr='Error reason: '+str(e.code)
	    print Fore.RED+exr+' '+e.reason,
	    output('[-]'+exr)
	    pass
	    #return "can't connect.","httperror"
	except URLError, e:
	    #print 'We failed to reach a server.'
	    exr='Failed reason: '+str(e.reason)
	    print Fore.RED+exr,
	    output('[-]'+exr)
	    pass
	    #return "can't connect.","urlerror"
	except socket.timeout as e:
	    #print type(e)    #catched
	    print Fore.RED+"timeout error catched",
	    pass
	    # return "can't connect.","urlerror"
	except (SSLError, socket.timeout) as error:
	    err_s = str(error)
	    if 'operation timed out' in err_s:
	        print Fore.RED+("ssl operation timed out"),
	        pass
	        # raise
	    pass
	except httplib.BadStatusLine:
		print Fore.RED+"BadStatusLine",
		pass
	print Fore.WHITE


#test OPTIONS	
	try:
		print 'OPTIONS: ',
		reso = http_options(url)
		print Fore.GREEN+'success...',
		# output(reso) #不保存options结果
		#print reso,
	except HTTPError, e:
	    #print 'The server couldn\'t fulfill the request.'
	    exr='Error reason: '+str(e.code)
	    print Fore.RED+exr+' '+e.reason,
	    output('[-]'+exr)
	    pass
	    #return "can't connect.","httperror"
	except URLError, e:
	    #print 'We failed to reach a server.'
	    exr='Failed reason: '+str(e.reason)
	    print Fore.RED+exr,
	    output('[-]'+exr)
	    pass
	    #return "can't connect.","urlerror"
	except socket.timeout as e:
	    #print type(e)    #catched
	    print Fore.RED+"timeout error catched",
	    pass
	    # return "can't connect.","urlerror"
	except (SSLError, socket.timeout) as error:
	    err_s = str(error)
	    if 'operation timed out' in err_s:
	        print Fore.RED+("ssl operation timed out"),
	        pass
	        # raise
	    pass
	    # raise NetworkError(err_s)
	except httplib.BadStatusLine:
		print Fore.RED+"BadStatusLine",
		pass
	print Fore.WHITE

#test put
	try:
		print 'PUT:',
		resp = http_put(url)
		print Fore.GREEN+'[!]Worning PUT Method found:'+url,
		output('[!]Worning PUT Method found:'+url)
		output(resp) 
		#print resp,
	except HTTPError, e:
	    #print 'The server couldn\'t fulfill the request.'
	    exr='Error reason: '+str(e.code)
	    print Fore.RED+exr+' '+e.reason,
	    output('[-]'+exr)
	    pass
	    #return "can't connect.","httperror"
	except URLError, e:
	    #print 'We failed to reach a server.'
	    exr='Failed reason: '+str(e.reason)
	    print Fore.RED+exr,
	    output('[-]'+exr)
	    pass
	    #return "can't connect.","urlerror"
	except socket.timeout as e:
	    #print type(e)    #catched
	    print Fore.RED+"timeout error catched",
	    pass
	    # return "can't connect.","urlerror"
	except (SSLError, socket.timeout) as error:
	    err_s = str(error)
	    if 'operation timed out' in err_s:
	        print Fore.RED+("ssl operation timed out"),
	        pass
	        # raise
	    pass
	    # raise NetworkError(err_s)
	except httplib.BadStatusLine:
		print Fore.RED+"BadStatusLine",
		pass
	print Fore.WHITE

#test delete
	try:
		print 'delete: ',
		resd = http_delete(url)
		print Fore.GREEN+'[!]Worning DELETE Method found:'+url,
		output('[!]Worning DELETE Method found:'+url)
		output(resd)
		# print resd,
	except HTTPError, e:
	    #print 'The server couldn\'t fulfill the request.'
	    exr='Error reason: '+str(e.code)
	    print Fore.RED+exr+' '+e.reason,
	    output('[-]'+exr)
	    pass
	    #return "can't connect.","httperror"
	except URLError, e:
	    #print 'We failed to reach a server.'
	    exr='Failed reason: '+str(e.reason)
	    print Fore.RED+exr,
	    output('[-]'+exr)
	    pass
	    #return "can't connect.","urlerror"
	except socket.timeout as e:
	    #print type(e)    #catched
	    print Fore.RED+"timeout error catched",
	    pass
	    # return "can't connect.","urlerror"
	except (SSLError, socket.timeout) as error:
	    err_s = str(error)
	    if 'operation timed out' in err_s:
	        print Fore.RED+("ssl operation timed out"),
	        pass
	        # raise
	    pass
	    # raise NetworkError(err_s)
	except httplib.BadStatusLine:
		print Fore.RED+"BadStatusLine",
		pass
	print Fore.WHITE



# test trace
	try:
		print 'trace: ',
		rest=http_trace(url)
		print Fore.GREEN+'[!]Worning TRACE Method found:'+url,
		output('[!]Worning TRACE Method found:'+url)
		output(rest)
		# print rest,
	except HTTPError, e:
	    #print 'The server couldn\'t fulfill the request.'
	    exr='Error reason: '+str(e.code)
	    print Fore.RED+exr+' '+e.reason,
	    output('[-]'+exr)
	    pass
	    #return "can't connect.","httperror"
	except URLError, e:
	    #print 'We failed to reach a server.'
	    exr='Failed reason: '+str(e.reason)
	    print Fore.RED+exr,
	    output('[-]'+exr)
	    pass
	    #return "can't connect.","urlerror"
	except socket.timeout as e:
	    #print type(e)    #catched
	    print Fore.RED+"timeout error catched",
	    pass
	    # return "can't connect.","urlerror"
	except (SSLError, socket.timeout) as error:
	    err_s = str(error)
	    if 'operation timed out' in err_s:
	        print Fore.RED+("ssl operation timed out"),
	        pass
	        # raise
	    pass
	    # raise NetworkError(err_s)
	except httplib.BadStatusLine:
		print Fore.RED+"BadStatusLine",
		pass
	print Fore.WHITE

# main主逻辑
def main():
    # 文件读取
    try:
        urllist=open(filepath,'r')
        url_target=urllist.readlines()
        url_target=[n.rstrip("\n") for n in url_target]
    except:
        print "[!]读取under_detection_targets.txt失败，请确保当前目录存在targets.txt且含有内容。"
    for n in url_target:  
        output(str(n))
        print Fore.WHITE+"Target:"+n
        method_test(n)



# 主流程调用，并引入中断
if __name__ == '__main__':
	# 抓取程序参数
	argv1=sys.argv[1:]
	#print argv1
	global filepath
	global single_url
	single_url =''
	filepath =''
	try:
		opts, args = getopt.getopt(argv1,"hu:r:",["innerurl="])
        # print opts
        # print args
	except getopt.GetoptError:
	    print 'method_test.py [option] [parameter]\t\n-u <url>\n-r <FilePath>'
	    sys.exit(2)
	for opt, arg in opts:
	    if opt == '-h':
	        print 'method_test.py [option] [parameter]\t\n-u <url>\n-r <FilePath> '
	        sys.exit()
	    elif opt in ("-u", "--url"):
	        single_url = arg
	        method_test(single_url)
	        break
	    elif opt in ("-r", "--file"):
	        filepath = arg
	        print filepath
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
		    print(Fore.WHITE+'stopped by keyboard')
		print(Fore.WHITE+'[!]KeyboardInterrupt quited listen')
		#-------------------------------------