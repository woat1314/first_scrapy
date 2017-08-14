from urllib.request import urlopen
from urllib.error import URLError
from bs4 import BeautifulSoup
import requests
import time
import csv
import codecs

num = 1
url = 'http://www.08 简书.com/u/c98451170fd6?order_by=shared_at&page='

for i in range(0, 18, 1):  # 这里的  range（初始，结束，间隔）
    html = requests.get('http://www.08 简书.com/u/c98451170fd6?order_by=shared_at&page=%d' % i).content
    bsObj = BeautifulSoup(html, 'lxml')
    namelist = bsObj.find_all('ul',attrs={'class':'note-list'})
    for list in namelist:
        for title_list in list.find_all('a',attrs={'class':'title'}):
            print(title_list.text)