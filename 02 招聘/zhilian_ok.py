# coding:utf-8

import requests
from bs4 import BeautifulSoup
import time

num=0
for i in range(0, 2, 1):  # 这里的  range（初始，结束，间隔）
    wbdata = requests.get('http://sou.zhaopin.com/jobs/searchresult.ashx?jl=%E5%8D%97%E4%BA%AC&kw=%E4%BA%A7%E5%93%81%E7%BB%8F%E7%90%86&kt=3&isfilter=1&sf=15001&st=20000&sg=c04890256c7245c0825effd7556834f9&p='+str(i)).content
    soup = BeautifulSoup(wbdata,'lxml')
    job_name = soup.select("table.newlist > tr > td.zwmc > div > a")
    salarys = soup.select("table.newlist > tr > td.zwyx")
    locations = soup.select("table.newlist > tr > td.gzdd")
    times = soup.select("table.newlist > tr > td.gxsj > span")
    companys = soup.select("table.newlist > tr > td.gsmc > a" )
    links = soup.select("table.newlist > tr > td.gsmc > a['href']")

    for link,company,name, salary, location, time in zip(links,companys,job_name, salarys, locations, times):
        data = {
            '职位名称':name.get_text(),
            '薪水':salary.get_text(),
            '地点':location.get_text(),
            '发布时间':time.get_text(),
            '公司名称':company.get_text(),
            '链接地址':link.get('href')
        }
        num=num+1
        print(list(data.values()),num)
