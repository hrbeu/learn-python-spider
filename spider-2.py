#-*- coding:utf-8 -*-
#构造一个request请求,它其实就是一个Request类的实例，构造时需要传入Url,Data等等的内容。
import urllib2

request=urllib2.Request("http://www.baidu.com")
response=urllib2.urlopen(request)
print response.read().decode('utf-8')
