# -*- coding=utf-8 -*-
import requests
from bs4 import BeautifulSoup
import time
import csv
import codecs

num = 1  # 用来计数，计算爬取的笑话一共有多少
start_time = time.time()  # 计算爬虫爬取过程时间

# 第一页网页网址http://zuimeia.com/?page=2&platform=1
# 第二页网页网址http://zuimeia.com/?page=2&platform=2
# 第三页网页网址http://zuimeia.com/?page=2&platform=3
# ......发现规律了吗
url = 'http://zuimeia.com/?page=%d&platform=1'

for i in range(1, 5, 1):  # 这里的  range（初始，结束，间隔）
    # requests库用来向该网服务器发送请求，请求打开该网址链接
    html = requests.get('http://zuimeia.com/?page=%d&platform=1' % i).content
    # BeautifulSoup库解析获得的网页，第二个参数一定记住要写上‘lxml’，记住就行
    bsObj = BeautifulSoup(html,'lxml')
   # % (i / 10 + 1) + '==============')
    # 分析网页发现，每页有10本书，而<h4>标签正好只有10个。
    app_list = bsObj.find_all('div',attrs={'class': 'left-side'})  # 这里返回的是content标签的list列表

    with codecs.open('zuimei.txt','a') as f:
        #f.write('\n****************我是分割线***************\n')
        for content_node in app_list:
            for span_node in content_node.find_all('h1'):
                #print(span_node.text)
                content_span = span_node.get_text()
    # 因为是列表，要用list[0]取出来<a>标签，在用<a>的string将文本取出来
                title = '"' + content_span + '"'
                name=('第%d个应用' % num + title)
                f.write(name + '\n')
                num = num + 1
                #print(num)
    # 设置抓数据停顿时间为1秒，防止过于频繁访问该网站，被封
    time.sleep(1)
