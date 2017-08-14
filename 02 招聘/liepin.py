import requests
from bs4 import  BeautifulSoup
import codecs
import time

for i in range(0, 5, 1):  # 这里的  range（初始，结束，间隔）
    html = requests.get('https://www.liepin.com/zhaopin/?imscid=R000000058&dqs=060020&industries=&salary=*&key=%E4%BA%A7%E5%93%81%E7%BB%8F%E7%90%86&industryType=&&ckid=a7e881d9f3eb52f5&curPage=').content
    soup = BeautifulSoup(html, 'lxml')
    print(soup)
    #job_name = soup.select("ul.sojob-list > li > div.02 招聘-info > span > a")
   # print(job_name)
    time.sleep(2)







