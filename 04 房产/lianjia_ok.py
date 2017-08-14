from bs4 import BeautifulSoup #导入bs4
import requests #爬虫请求利器 requests
csvfile = open("lianjia.csv","a") #新建一个文件
headers = {'User-Agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/55.0.2883.98 Safari/537.36 Vivaldi/1.6.689.40'} #模拟浏览器

for k in range(1,2):#总共100页
    req = requests.get("http://bj.lianjia.com/ershoufang/pg"+str(k),headers = headers)
    req.encoding = ('utf8')
    soup = BeautifulSoup(req.text, "html.parser")
    for tag in soup.find_all("div","info clear"):
        tag_addr = tag.find("div", "address")
        # print(tag_addr.text.replace("|",","))
        tag_total_price = tag.find("div","totalPrice")
        tag_unit_price = tag.find("div","unitPrice")
        addr = tag_addr.text.replace("|",",")
        csvfile.write(tag_addr.text +" | " + tag_total_price.text + " | "+ tag_unit_price.text+"\r\n")
csvfile.close()