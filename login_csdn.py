#-*-coding:utf-8-*-
import requests
import os
from lxml import etree
from cookielib import LWPCookieJar
#CSDN登录页面地址
url='https://passport.csdn.net/account/login'
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
        html=s.get(url).text
        tree=etree.HTML(html)
        #获取流水号
        lt=tree.xpath('//*[@id="fm1"]/input[3]/@value')[0]
        #获取执行次数
        execution=tree.xpath('//*[@id="fm1"]/input[4]/@value')[0]
        #填充登录表单
        payload={'username':'jb19900111',
                'password':'jiangbo885080',
                'lt':lt,
                'execution':execution,
                '_eventId':'submit',
                }
        #显示表单内容
        print payload
        #表单发送地址也是本页
        r1=s.post(url,data=payload,headers=headers)
        #baocuncookie
        s.cookies.save(ignore_discard=True)
        print r1.text
else:
        print "Cookie already exists!Restore!"
        s.cookies.load(ignore_discard=True)
print "================================================================"
r2 = s.get("https://passport.csdn.net/content/loginbox/loginapi.js")
print r2.text
print "================================================================"
r3=s.get("http://blog.csdn.net/zhaoyl03/article/details/8631897",headers=headers,timeout=20)
print r3.text


'''
#-*-coding:utf-8-*-
#使用urllib2.opener登录csdn
import urllib,urllib2,cookielib
from bs4 import BeautifulSoup

cj=cookielib.CookieJar()
handler=urllib2.HTTPCookieProcessor(cj)
opener=urllib2.build_opener(handler)
url='https://passport.csdn.net/account/login'
headers={'User-Agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/46.0.2490.80 Safari/537.36'}

html=opener.open(url).read()
soup=BeautifulSoup(html)
#获取流水号
lt=soup.find_all("input")[3]['value']
#获取执行次数
execution=soup.find_all("input")[4]['value']
data={'username':'jb19900111',
      'password':'jiangbo885080',
      'lt':lt,
      'execution':execution,
      '_eventId':'submit',
      }
data=urllib.urlencode(data)
req=urllib2.Request(url,data,headers)
res=opener.open(req).read()
print res
print "====================================================================="
opener.addheaders=[('User-Agent','Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/46.0.2490.80 Safari/537.36')]
print opener.open("http://blog.csdn.net/jb19900111/article/details/50511471").read()
'''
