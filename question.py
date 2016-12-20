#-*- coding: utf-8 -*-
import re
import json
from lxml import etree
from zhuanlan import zhihu
import operator

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
            r=self.session.post('https://www.zhihu.com/node/QuestionAnswerListV2',data=data,headers=self.headers)
            content=json.loads(r.content.decode('utf8','ignore'))
            #print content
            #print content["msg"]
            #print len(content["msg"])
            #print type(content["msg"])
            for item in content["msg"]:
                answer = {}
                answer["html"]=item
                tree=etree.HTML(item)
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
            #如果页面答案数小于10，则到了最后一页，停止爬取
            if int(len(content["msg"])) < 10:
                endflag=False
                print "共捕获%s个回答" % count
    #对答案进行排序
    def answers_sort(self,criterion="editTime"):
        sorted_answers = sorted(self.answers, key=operator.itemgetter(criterion), reverse=True)
        for answer in sorted_answers:
            print answer["content"]
            print criterion,":",answer[criterion]
        print "\n===========================   THE  END   ====================================\n"


a1=question()
a1.login()
a1.get_answers('23142571')
a1.answers_sort("commentsCount")







