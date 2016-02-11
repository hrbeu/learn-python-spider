#-*-coding:utf-8-*-

import requests
import os
from lxml import etree
from cookielib import LWPCookieJar
#CSDN登录页面地址
url='https://www.douban.com/accounts/login'
#定义一个会话
s=requests.Session()
#LWPCookieJar继承自FileCookieJar,FileCookieJar继承自CookieJar
s.cookies=LWPCookieJar('cookiejar')

#必须有headers
headers={'Accept':'*/*',
        'Accept-Encoding':'gzip, deflate, sdch',
        'Accept-Language':'zh-CN,zh;q=0.8',
        'Connection':'keep-alive',
        'User-Agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/46.0.2490.80 Safari/537.36',
         }
#判断是否已有保存为文件的cookie
if not os.path.exists('cookiejar'):
        print "There is no cookie setting!"

        data={'source':'None',
              'redir':'https://www.douban.com',
              'form_email':'',
              'form_password':'',
              'checkbox':'',
              'login':'登录'}
        #显示表单内容
        print data
        #表单发送地址也是本页
        r1=s.post(url,data=data,headers=headers)
        #baocuncookie
        s.cookies.save(ignore_discard=True)
        print r1.text


'''
import urllib2
import cookielib
import urllib

cj=cookielib.CookieJar()
handler=urllib2.HTTPCookieProcessor(cj)
opener=urllib2.build_opener(handler)
url='https://www.douban.com/accounts/login'
headers={'User-Agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/46.0.2490.80 Safari/537.36'}

data={'source':'None',
      'redir':'https://www.douban.com',
      'form_email':'',
      'form_password':'',
      'checkbox':'',
      'login':'登录'}
data=urllib.urlencode(data)
req=urllib2.Request(url,data,headers)
res=opener.open(req).read()
print res
'''
