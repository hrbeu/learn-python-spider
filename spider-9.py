#-*- coding:utf-8 -*-
#捕获异常
import urllib2
req=urllib2.Request('http://blog.csdn.net/cqcre')
try:
	urllib2.urlopen(req)
except urllib2.HTTPError,e:
	print e.code
except urllib2.URLError,e:
    print e.rason
else:
    print 'OK'
#或者	
import urllib2
 
req = urllib2.Request('http://blog.csdn.net/cqcre')
try:
    urllib2.urlopen(req)
except urllib2.URLError, e:
    if hasattr(e,"code"):
        print e.code
    if hasattr(e,"reason"):
        print e.reason
else:
    print "OK"