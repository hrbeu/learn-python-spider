#-*- coding: utf-8 -*-
import re
import json
from lxml import etree
from zhuanlan import zhihu
import operator
import time

class question(zhihu):
    def __init__(self):
        self.answers=[]
        zhihu.__init__(self)
    #获取问题页面的xsrf值
    def get_qxsrf(self,qid,url):
        content = self.session.get(url, headers=self.headers)
        xsrf = re.findall(r'<input type=\"hidden\" name=\"_xsrf\" value=\"(\w+)\"', content.text)[0]
        #print xsrf
        return xsrf
    #获取该问题下全部答案
    def get_answers(self,qid):
        url = 'https://www.zhihu.com/question/' + qid
        qxsrf = self.get_qxsrf(qid,url)
        endflag=True
        count=0
        offset = 0
        while endflag:
            time.sleep(1)
            params = {"url_token":qid,"pagesize":10,"offset":offset}
            params_json=json.dumps(params)
            data = {
                'method': 'next',
                'params': params_json,
                #'_xsrf': str(xsrf)
            }
            self.headers['Referer']=url
            self.headers['Origin']='https://www.zhihu.com'
            self.headers['X-Xsrftoken']=str(qxsrf)
            try:
                r=self.session.post('https://www.zhihu.com/node/QuestionAnswerListV2',data=data,headers=self.headers)
                content=json.loads(r.content.decode('utf8','ignore'))
            except:
                break
            #print content
            #print content["msg"]
            #print len(content["msg"])
            #print type(content["msg"])
            for item in content["msg"]:
                answer = {}
                answer["html"]=item
                tree=etree.HTML(item)
                #提取答主头像的url
                answer['profile_photo'] = "Anonymous User"      #默认是匿名回答，没有答主头像
                for node in tree.xpath("//a[@class='zm-item-link-avatar avatar-link']"):        #如果能抓取到头像，则保持头像url地址
                    answer['profile_photo']=str(node.xpath("img/@src")[0])
                #提取回答中格式为origin_image zh-lightbox-thumb的图片
                answer['pics_list'] = []        #默认无图
                for node in tree.xpath("//img[@class='origin_image zh-lightbox-thumb']"):
                    answer['pics_list'].append(str(node.xpath("@src")[0]))      #保存全部图片的url
                #提取回答中格式为content_image的图片
                answer['images'] = []         #默认无图
                for node in tree.xpath("//img[@class='content_image']"):
                    answer['images'].append(str(node.xpath("@src")[0]))     #保存全部图片的url
                #提取回答内容
                for node in tree.xpath("//div[@class='zm-editable-content clearfix']"):
                    answer['content']=node.xpath('string(.)')
                #提取点赞数
                for node in  tree.xpath("//button[@class='up ']"):
                    answer['voteCount']=int(node.xpath("//span[@class='count']/text()")[0])
                #提取评论数
                for node in  tree.xpath("//a[@name='addcomment']"):
                    if node.xpath("text()")[1]!=u"添加评论":
                        answer['commentsCount']=int(node.xpath("text()")[1][0])
                    else:
                        answer['commentsCount']=0
                #提取编辑时间
                for node in tree.xpath("//a[@class='answer-date-link meta-item']"):
                    answer['editTime']=node.xpath("text()")[0][-10:]
                self.answers.append(answer)
            offset+=10
            count+=len(content["msg"])
            print u"获取了 %s 个答案" % count
            #如果页面答案数小于10，则到了最后一页，停止爬取
            if int(len(content["msg"])) < 10:
                endflag=False
                print
                print "共捕获%s个回答" % count
    #对答案进行排序
    def answers_sort(self,criterion="editTime"):
        sorted_answers = sorted(self.answers, key=operator.itemgetter(criterion), reverse=True)
        for answer in sorted_answers:
            print answer["content"]
            print u"作者头像：",answer['profile_photo']
            #计算回答中两种格式图片的总数
            pics_count=len(answer['pics_list'])+len(answer['images'])
            print u"共 %s 张图片" %   pics_count
            print criterion,":",answer[criterion]
        print "\n===========================   THE  END   ====================================\n"


a1=question()
a1.login()
a1.get_answers('29057201')
a1.answers_sort("commentsCount")







