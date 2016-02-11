# -*- coding:utf-8 -*-
#找拥有两种标签的豆瓣图书
try:  
    import json  
except ImportError:  
    import simplejson as json  
import cookielib  
import urllib
import urllib2
from multiprocessing import Pool
from multiprocessing.dummy import Pool as ThreadPool
from bs4 import BeautifulSoup
from lxml import etree 

import sys
reload(sys)
sys.setdefaultencoding('utf-8')

'''
#用editthiscookie导出chrome的cookie至cookies.txt
cookie_jar = cookielib.MozillaCookieJar()  
cookies = open('cookies.txt').read()  
for cookie in json.loads(cookies):  
    print cookie['name']  
    cookie_jar.set_cookie(cookielib.Cookie(version=0, name=cookie['name'], value=cookie['value'], port=None, port_specified=False, domain=cookie['domain'], domain_specified=False, domain_initial_dot=False, path=cookie['path'], path_specified=True, secure=cookie['secure'], expires=None, discard=True, comment=None, comment_url=None, rest={'HttpOnly': None}, rfc2109=False))   
'''




books=[]
filtered_books=[]
result_books=[]
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
    nodes=tree.xpath('//div[@class="mod book-list"]//dl')
    for node in nodes:
        item={}
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
'''
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
'''
def multi_thread(func,parameter):
    pool=ThreadPool(4)
    symbol_results=pool.map(func,parameter)
    pool.close()
    pool.join()

    
if __name__=="__main__":

   # douban_opener=login()
    #urllib2.install_opener(douban_opener)
    multi_thread(one_page_book_info,start_urls)
    
#    for url in start_urls:
#        books.extend(one_page_book_info(url))
    [filtered_books.append(book) for book in books if book not in filtered_books]
    for book in filtered_books:
        if check_tag(book['link']):
            result_books.append(book)
    print result_books


    

