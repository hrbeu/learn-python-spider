# -*- coding:utf-8 -*-
#找拥有两种标签的豆瓣图书
try:  
    import json  
except ImportError:  
    import simplejson as json  
import cookielib  
import urllib2  
import urllib2
from multiprocessing import Pool
from multiprocessing.dummy import Pool as ThreadPool
from bs4 import BeautifulSoup
from lxml import etree 

import sys
reload(sys)
sys.setdefaultencoding('utf-8')


#用editthiscookie到处chrome的cookie至cookies.txt
cookie_jar = cookielib.MozillaCookieJar()  
cookies = open('cookies.txt').read()  
for cookie in json.loads(cookies):  
    print cookie['name']  
    cookie_jar.set_cookie(cookielib.Cookie(version=0, name=cookie['name'], value=cookie['value'], port=None, port_specified=False, domain=cookie['domain'], domain_specified=False, domain_initial_dot=False, path=cookie['path'], path_specified=True, secure=cookie['secure'], expires=None, discard=True, comment=None, comment_url=None, rest={'HttpOnly': None}, rfc2109=False))   





books=[]
filtered_books=[]
start_urls=[]
#搜索全部宗教类书籍
for i in range(0,510,15):
    x="http://www.douban.com/tag/%E5%AE%97%E6%95%99/book?start="+str(i)
    start_urls.append(x)


#把宗教类列表中的书籍按页找到
def one_page_book_info(url):
    print url
    req=urllib2.Request(url,headers={'User-Agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/46.0.2490.80 Safari/537.36'})
    res=urllib2.urlopen(req).read()
    tree=etree.HTML(res)
    item={}
    nodes=tree.xpath('//div[@class="mod book-list"]//dl')
    for node in nodes:
        item['name']=node.xpath('dd/a[@class="title"]/text()')[0]
        item['link']=node.xpath('dd/a/@href')[0].split('?')[0]
        item['stars']=node.xpath('dd/div[@class="rating"]/span/@class')
        books.append(item)
        #yield item
#判断书籍是否有某类标签
def check_tag(url):
    print 'check'+url
    req=urllib2.Request(url,headers={'User-Agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/46.0.2490.80 Safari/537.36'})
    res=urllib2.urlopen(req).read()
    soup=BeautifulSoup(res)
    tags=[]
    for tag in soup.find_all('a','tag'):
        tags.append(tag.text)
    if u'符号' in tags:
        return True
    else:
        return False

    

if __name__=="__main__":
    pool=ThreadPool(4)
    results=pool.map(one_page_book_info,start_urls)
    pool.close()
    pool.join()
#    for url in start_urls:
#        books.extend(one_page_book_info(url))
    for book in books:
        if check_tag(book['link']):
            filtered_books.append(book)
    print filtered_books


    

