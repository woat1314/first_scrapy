import requests
from bs4 import BeautifulSoup
import re
import random
import time
csvfile = open("boss.csv","a") #新建一个文件
def get_ip_list(url, headers):
    web_data = requests.get(url, headers=headers)
    soup = BeautifulSoup(web_data.text, 'lxml')
    ips = soup.find_all('tr')
    ip_list = []
    for i in range(1, len(ips)):
        ip_info = ips[i]
        tds = ip_info.find_all('td')
        ip_list.append(tds[1].text + ':' + tds[2].text)
    return ip_list

def get_random_ip(ip_list):
    proxy_list = []
    for ip in ip_list:
        proxy_list.append('http://' + ip)
    proxy_ip = random.choice(proxy_list)
    proxies = {'http': proxy_ip}
    return proxies

if __name__ == '__main__':
    url = 'http://www.xicidaili.com/nn/'
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/53.0.2785.143 Safari/537.36'
    }
    ip_list = get_ip_list(url, headers=headers)
    proxies = get_random_ip(ip_list)
    print(proxies)


header = {
    'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_12_3) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/56.0.2924.87 Safari/537.36',
    'Connection': 'keep-alive',
    'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
    'Accept-Encoding':'gzip, deflate, sdch'
    }

for i in range(1,31,1):
    url = 'http://bosszhipin.kanzhun.com/c101190100/h_101190100/?query=%E4%BA%A7%E5%93%81%E7%BB%8F%E7%90%86&page={}&ka=page-{}'.format(i,i)

    soup = requests.get(url,headers=header, proxies=proxies).content
    body = BeautifulSoup(soup,'lxml')
    urls_title = body.select("div.job-list > ul > li > a")
    # print(urls_title)
    for link in urls_title:
        links='http://bosszhipin.kanzhun.com/'+link.get('href')
        # print(links)
        xq_soup = requests.get(links,headers=header, proxies=proxies).content
        xq_body = BeautifulSoup(xq_soup,'lxml')
        location = xq_body.select('div.location-address')
        for list in location:
            list_text =list.get_text()
            print(list_text)
            # csvfile.write(list_text+ "\r\n")
        time.sleep(1)
