# blueutils

这是一个python 的 crypto 工具集

## 安装
```
$ pip install blueutils
```

## 比特浏览器接口
比特浏览器官方虽然提供了api文档，但是没法直接拿来用，所以我对官方api文档进行封装了下，使用起来更简单了，使用方法如下：


```python
from blueutils.bitbrowser_api import BitBrowser

b = BitBrowser(id="你的浏览器id")    
b.open()
context = b.get_browser_context()
print(context)
b.close()
```




