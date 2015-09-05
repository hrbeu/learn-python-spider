#-*- coding:utf-8 -*-
#GET Method

import urllib
import urllib2

values={ 'username':'1016902102@qq.com','passwd':'xxxx'}
data=urllib.urlencode(values)
origin_url="http://passport.csdn.net/account/login"
url=origin_url+"?"+data      #GET传参
request=urllib2.Request(url)
response=urllib2.urlopen(request)
print response.read().decode('utf-8')
