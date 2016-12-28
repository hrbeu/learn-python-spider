# -*- coding: utf-8 -*-

import requests
try:
    import cookielib
except:
    import http.cookiejar as cookielib
import re
import time
import os.path
try:
    from PIL import Image
except:
    pass
import operator
import logging
import loggingconfig
loggingconfig.config_logging("C:\Users\win\Desktop\zhuanlan.log")
LOG=logging.getLogger("__name__")

class zhihu():
    def __init__(self):
        self.agent = 'Mozilla/5.0 (Linux; Android 6.0; Nexus 5 Build/MRA58N) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/55.0.2883.75 Mobile Safari/537.36'
        self.headers = {
            'Accept': '*/*',
            "Host": "www.zhihu.com",
            "Referer": "https://www.zhihu.com/",
            'User-Agent': self.agent,
            'Origin': 'https://www.zhihu.com',
            'Accept-Language': 'zh-CN,zh;q=0.8,en;q=0.6',
            'Connection': 'keep-alive',
            'X-Requested-With': 'XMLHttpRequest',

        }
        # 使用登录cookie信息
        self.session = requests.session()
        self.session.cookies = cookielib.LWPCookieJar(filename='cookies')
        try:
            self.session.cookies.load(ignore_discard=True)
        except:
            print "Cookie 未能加载"
        self.articles=[]

    def get_xsrf(self):
        '''_xsrf 是一个动态变化的参数'''
        index_url = 'https://www.zhihu.com'
        # 获取登录时需要用到的_xsrf
        index_page = self.session.get(index_url, headers=self.headers)
        html = index_page.text
        pattern = r'name="_xsrf" value="(.*?)"'
        # 这里的_xsrf 返回的是一个list
        _xsrf = re.findall(pattern, html)
        return _xsrf[0]

    # 获取验证码
    def get_captcha(self):
        t = str(int(time.time() * 1000))
        captcha_url = 'https://www.zhihu.com/captcha.gif?r=' + t + "&type=login"
        r = self.session.get(captcha_url, headers=self.headers)
        with open('captcha.jpg', 'wb') as f:
            f.write(r.content)
            f.close()
        # 用pillow 的 Image 显示验证码
        # 如果没有安装 pillow 到源代码所在的目录去找到验证码然后手动输入
        try:
            im = Image.open('captcha.jpg')
            im.show()
            im.close()
        except:
            print(u'请到 %s 目录找到captcha.jpg 手动输入' % os.path.abspath('captcha.jpg'))
        captcha = input("please input the captcha\n>")
        return captcha

    def isLogin(self):
        # 通过查看用户个人信息来判断是否已经登录
        url = "https://www.zhihu.com/settings/profile"
        login_code = self.session.get(url, headers=self.headers, allow_redirects=False).status_code
        if login_code == 200:
            return True
        else:
            return False

    def __login(self,secret, account):
        # 通过输入的用户名判断是否是手机号
        if re.match(r"^1\d{10}$", account):
            print("手机号登录 \n")
            post_url = 'https://www.zhihu.com/login/phone_num'
            postdata = {
                '_xsrf': self.get_xsrf(),
                'password': secret,
                'remember_me': 'true',
                'phone_num': account,
            }
        else:
            if "@" in account:
                print "邮箱登录 \n"
            else:
                print "你的账号输入有问题，请重新登录"
                return 0
            post_url = 'https://www.zhihu.com/login/email'
            postdata = {
                '_xsrf': self.get_xsrf(),
                'password': secret,
                'remember_me': 'true',
                'email': account,
            }
        try:
            # 不需要验证码直接登录成功
            login_page = self.session.post(post_url, data=postdata, headers=self.headers)
            login_code = login_page.text
            print login_page.status_code
            print login_code
        except:
            LOG.error("Need to type in the captcha manually")
            # 需要输入验证码后才能登录成功
            postdata["captcha"] = self.get_captcha()
            login_page = self.session.post(post_url, data=postdata, headers=self.headers)
            login_code = eval(login_page.text)
            print login_code['msg']
        self.session.cookies.save()

    def login(self):
        if self.isLogin():
            print '您已经登录'
        else:
            account = raw_input('请输入你的用户名\n>  ')
            secret = raw_input("请输入你的密码\n>  ")
            self.__login(secret, account)
            self.session.get('https://www.zhihu.com',headers=self.headers)

class zhuanlan(zhihu):
    def __init__(self):
        zhihu.__init__(self)
    #获取专栏信息
    def get_zhuanlan(self,zhuanlan):
        self.headers['Referer'] = 'https://zhuanlan.zhihu.com/' + str(zhuanlan)
        self.headers['Host'] = 'zhuanlan.zhihu.com'
        TextAPI = 'https://zhuanlan.zhihu.com/api/columns/' + str(zhuanlan) + '/posts?limit=20&offset='
        endflag = True
        offset = 0
        while endflag:
            TextContentHTML = self.session.get(TextAPI + str(offset), headers=self.headers).json()
            # print session.get(TextAPI + str(offset),headers=headers)
            for everText in TextContentHTML:
                article={}
               # '文章作者相关
               # 地址
                article['author_profileUrl']=everText['author']['profileUrl'].encode('utf-8')
                #签名
                article['author_bio']=everText['author']['bio'].encode('utf-8')
                #昵称
                article['author_name']=everText['author']['name'].encode('utf-8')
                #hash
                article['author_hash']=everText['author']['hash'].encode('utf-8')
                #介绍
                article['author_description']=everText['author']['description'].encode('utf-8')
                #文章信息
                #文章标题
                article['title']=everText['title'].encode('utf-8')
                #地址
                article['url']=everText['url'].encode('utf-8')
                #推送时间
                article['publishedTime']= everText['publishedTime'].encode('utf-8')
                #评论数量
                article['commentsCount']= int(everText['commentsCount'])
                #点赞数量
                article['likesCount']=int(everText['likesCount'])
                #内容
                article['content']=everText['content'].encode('utf-8')
                self.articles.append(article)
            if len(TextContentHTML)<20:
                endflag=False
            offset += 20
    #对文章排序
    def zhuanlan_sort(self,criterion):
        try:
            sorted_articles=sorted(self.articles,key=operator.itemgetter(criterion),reverse=True)
        except Exception,e:
            LOG.error("Criterion %s doesn't exist" % criterion)
            exit(1)
        else:
            LOG.info("Answers sorted by %s" % criterion)
        for article in sorted_articles:
            print article['title'],criterion+':',article[criterion]


if __name__=='__main__':
    z=zhuanlan()
    z.login()
    z.get_zhuanlan('KarolusSericus')
    print "一共%s篇文章" % len(z.articles)
    z.zhuanlan_sort('likesCount')