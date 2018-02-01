#useage：
把这个webdriver放在系统变量下，如python根目录。
```
bug:    
raise exception_class(message, screen, stacktrace)
selenium.common.exceptions.WebDriverException: Message: unknown error: cannot determine loading status
from unknown error: missing or invalid 'entry.level'
  (Session info: chrome=64.0.3282.119)
  (Driver info: chromedriver=2.25.426923 (0390b88869384d6eb0d5d09729679f934aab9eed),platform=Windows NT 10.0.16299 x86_64)

解决方法:
下载并替换最新的webdriver
http://npm.taobao.org/mirrors/chromedriver/
```