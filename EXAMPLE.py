# encoding:utf-8
import urllib
import urllib2
import re
import cookielib

r=re.compile('name=\"_xsrf\" value=\"(.+)\"/>')
xsrf=r.findall(urllib.urlopen("http://www.zhihu.com").read())[0]
print xsrf
values={
        "_xsrf":xsrf,
	"email":"940971769@qq.com",
	"passwd":"jiangbo885080",
        "rememberme":"y"
}
data=urllib.urlencode(values)
headers={
    "User-Agent":"Mozilla/5.0 (Windows NT 6.3; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/40.0.2214.111 Safari/537.36"
}
request=urllib2.Request("http://www.zhihu.com",data,headers)
cj=cookielib.CookieJar()
opener=urllib2.build_opener(urllib2.HTTPCookieProcessor(cj))
for item in cj:
    print item.name+':'+item.value
print opener.open(request).read().decode('utf-8')


