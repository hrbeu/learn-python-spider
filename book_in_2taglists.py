# -*- coding:utf-8 -*-
#找拥有两种标签的豆瓣图书
import urllib2
import urllib
from multiprocessing import Pool
from multiprocessing.dummy import Pool as ThreadPool
from bs4 import BeautifulSoup
from lxml import etree
import time
import cookielib

import sys
reload(sys)
sys.setdefaultencoding('utf-8')

#随机的headers值
hds=[{'User-Agent':'Mozilla/5.0 (Windows; U; Windows NT 6.1; en-US; rv:1.9.1.6) Gecko/20091201 Firefox/3.5.6'},\
{'User-Agent':'Mozilla/5.0 (Windows NT 6.2) AppleWebKit/535.11 (KHTML, like Gecko) Chrome/17.0.963.12 Safari/535.11'},\
{'User-Agent': 'Mozilla/5.0 (compatible; MSIE 10.0; Windows NT 6.2; Trident/6.0)'}]

religion_urls=[]
religion_books=[]
filtered_religion_books=[]
symbol_urls=[]
symbol_books=[]
filtered_symbol_books=[]
filtered_books=[]
#搜索全部宗教类、符号类书籍
for i in range(0,510,15):
    x="http://www.douban.com/tag/%E5%AE%97%E6%95%99/book?start="+str(i)
    y="http://www.douban.com/tag/%E7%AC%A6%E5%8F%B7/book?start="+str(i)
    religion_urls.append(x)
    symbol_urls.append(y)


#把宗教类列表中的书籍按页找到
def get_religion_book_info(url):
    time.sleep(5)
    print url
    x=url.split('=')[1]
    x=int(x)
    try:
        req=urllib2.Request(url,headers=hds[x%len(hds)])
        res=urllib2.urlopen(req).read()
    except (urllib2.HTTPError, urllib2.URLError), e:
            print e
    tree=etree.HTML(res)

    nodes=tree.xpath('//div[@class="mod book-list"]//dl')
    for node in nodes:
        item={}
        item['name']=node.xpath('dd/a[@class="title"]/text()')[0]
        item['link']=node.xpath('dd/a/@href')[0].split('?')[0]
        item['stars']=node.xpath('dd/div[@class="rating"]/span/@class')
        religion_books.append(item)

#把符号类列表中的书籍按页找到
def get_symbol_book_info(url):
    time.sleep(5)
    print url
    #用x随机使用一个headers
    x=url.split('=')[1]
    x=int(x)
    try:
        req=urllib2.Request(url,headers=hds[x%len(hds)])
        res=urllib2.urlopen(req).read()
    except (urllib2.HTTPError, urllib2.URLError), e:
        print e
    tree=etree.HTML(res)

    nodes=tree.xpath('//div[@class="mod book-list"]//dl')
    for node in nodes:
        item={}
        item['name']=node.xpath('dd/a[@class="title"]/text()')[0]
        item['link']=node.xpath('dd/a/@href')[0].split('?')[0]
        item['stars']=node.xpath('dd/div[@class="rating"]/span/@class')
        symbol_books.append(item)

#登录豆瓣
def login():
    cj=cookielib.CookieJar()
    handler=urllib2.HTTPCookieProcessor(cj)
    opener=urllib2.build_opener(handler)
    url='https://www.douban.com/accounts/login'
    headers={'User-Agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/46.0.2490.80 Safari/537.36'}

    data={'source':'None',
        'redir':'https://www.douban.com',
        'form_email':'豆瓣邮箱',
        'form_password':'豆瓣密码',
        'checkbox':'',
        'login':'登录'}
    data=urllib.urlencode(data)
    try:
        req=urllib2.Request(url,data,headers)
        res=opener.open(req).read()
        print url
    except (urllib2.HTTPError, urllib2.URLError), e:
        print e
    return opener
#用多线程的方法进行处理
def multi_thread(func,parameter):
    pool=ThreadPool(4)
    symbol_results=pool.map(func,parameter)
    pool.close()
    pool.join()

if __name__=="__main__":
    #建立一个opener
    douban_opener=login()
    urllib2.install_opener(douban_opener)
    #使用多线程对宗教类书籍进行提取 
    multi_thread(get_religion_book_info,religion_urls)
    #过滤重复信息
    [filtered_religion_books.append(item) for item in religion_books if item not in filtered_religion_books]

    print 'now...'
    #使用多线程对符号类书籍进行提取
    multi_thread(get_symbol_book_info,symbol_urls)
    #过滤重复信息
    [filtered_symbol_books.append(item) for item in symbol_books if item not in filtered_symbol_books]

#找到宗教类和符号类列表中同名的书
    for religion_book in filtered_religion_books:
        for symbol_book in filtered_symbol_books:
            if religion_book['name'].strip()==symbol_book['name'].strip():
                filtered_books.append(religion_book)

    #对检索到的书籍按星级有高到低进性排序
    filtered_books=sorted(filtered_books,key=lambda x:x['stars'][0],reverse=True)
    
    raw_input('PRESS ENTER TO　CONTINUE...')

    for filtered_book in filtered_books:
        print filtered_book['name'].encode('utf-8')+' : '+str(filtered_book['stars'][0])+' '+str(filtered_book['link'])

                

