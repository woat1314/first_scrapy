import requests
from bs4 import BeautifulSoup
import re

for i in range(1,5,1):
    url = 'http://bosszhipin.kanzhun.com/c101010100/h_101010100/?query=java&page={}&ka=page-2'.format(i)
    soup = requests.get(url).text
    body = BeautifulSoup(soup,'lxml')
    salarys = body.select("div.info-primary > h3.name > span")
    locates = body.select('div.info-primary > p')
    companys = body.select('div.info-comapny > div.company-text > h3.name')
    for salary,locate,company in zip(salarys, locates,companys):
        location = re.sub('<em(.*)',"",str(locate))
        ww = re.sub('<p>','',location)
        data = {
            '薪水': salary.get_text(),
            '地点': ww,
            '公司': company.get_text()
        }
        print(data)