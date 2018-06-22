# http method 安全检测工具[批量]
### 简介
由于实际安全检测中经常会遇到大量PUT，DELETE，OPTIONS，TRACE类型http头method开启，为防止遗漏，需要对于此类漏洞进行批量检测以节约检测时间。基于此类实际需要制作了此类工具。


###使用语法：
```
method_test.py [option] [parameter]
-h this help
-u <url>
-r <FilePath>
```
eg. ”method_test.py -u http://baidu.com"\
eg. "method_test.py -r d:\url.txt" (url.txt内容需统一带http/https://)
