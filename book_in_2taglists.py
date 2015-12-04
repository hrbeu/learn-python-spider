# -*- coding:utf-8 -*-
#找拥有两种标签的豆瓣图书
import urllib2
from multiprocessing import Pool
from multiprocessing.dummy import Pool as ThreadPool
from bs4 import BeautifulSoup
from lxml import etree 

import sys
reload(sys)
sys.setdefaultencoding('utf-8')


religion_books=[]
symbol_books=[]
filtered_books=[]
religion_urls=[]
symbol_urls=[]
#搜索全部宗教类、符号类书籍
for i in range(0,510,15):
    x="http://www.douban.com/tag/%E5%AE%97%E6%95%99/book?start="+str(i)
    y="http://www.douban.com/tag/%E7%AC%A6%E5%8F%B7/book?start="+str(i)
    religion_urls.append(x)
    symbol_urls.append(x)


#把宗教类列表中的书籍按页找到
def get_religion_book_info(url):
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
        religion_books.append(item)

#把符号类列表中的书籍按页找到
def get_symbol_book_info(url):
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
        symbol_books.append(item)


    

if __name__=="__main__":

    pool=ThreadPool(4)
    religion_results=pool.map(get_religion_book_info,religion_urls)   
    pool.close()
    pool.join()
    
    pool=ThreadPool(4)
    symbol_results=pool.map(get_symbol_book_info,symbol_urls)
    pool.close()
    pool.join()
#找到宗教类和符号类列表中同名的书
    for religion_book in religion_books:
        for symbol_book in symbol_books:
            if religion_book['name']==symbol_book['name']:
                print religion_book['name'].encode('utf-8')+":"+religion_book['link']
                

