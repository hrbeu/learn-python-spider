#-*- coding:utf-8 -*-
#爬虫是一种按照一定的规则，自动的抓取万维网信息的程序或者脚本。
#最简单的爬网页
import urllib2

response=urllib2.urlopen("http://www.baidu.com")
print response
print response.read().decode('utf-8')
