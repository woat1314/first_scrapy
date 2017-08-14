from tinydb import TinyDB
db = TinyDB('collection_db.json')
# 这里我们尝试下tinydb，一句话就获得了新建的数据库对象
import csv
csvfile = open("1.csv", "w", encoding='utf-8') # 先保存为utf8编码，以免出现gbk编码错误
fieldnames = ["cname", "href", "focus_number", "essays", "hot_url", "new_url"] # 设定Excel文件的列表头
writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
# 这里我们获取csv的字典插入器，可以直接插入字典，键为列表头中的内容
writer.writeheader()
# 写入列表头

import requests
from bs4 import BeautifulSoup
import re
reg = re.compile('(\d+)篇')
# 使用正则匹配来获取篇数，(\d+)表示多个数字

base_url = "http://08 简书.com"
collectionlist_url = "http://www.08 简书.com/collections?order_by=score&page=%d"
# collection_url = 'http://www.jianshu.com/collections/%d/notes?order_by=added_at&page=1'
add_url = 1
# collection_num = 1

collection_selector = "h5 a" # 专题名
focus_on_selector = ".follow > span" # 关注人数
total_essay_selector = ".blue-link" # 总篇数
hot_selector = ".top-articles a" # 热门排序
new_selector = ".latest-articles a" # 最新收入

total_collection_list = []


while(add_url < 300):
    try: # 请求并获取各种数据
        first_page = requests.request('get', collectionlist_url% add_url).content
        soup = BeautifulSoup(first_page, "lxml")

        collection_list = [[i.get_text(),i.get('href')] for i in soup.select(collection_selector)] # 一组24个
        if not collection_list : break

        focus_on_list = [i.get_text() for i in soup.select(focus_on_selector)]
        focus_on_list = [int(float(i.replace('K', ''))*1000) if ('K' in i) else int(i) for i in focus_on_list]
        # 对尾缀K处理，将K去掉，将数字乘以1000

        total_essay_list =[ int( reg.findall(i.get_text())[0] ) for i in soup.select(total_essay_selector)]
        # 使用zip将多个可迭代对象合并在一起使用
        for c,f,e in zip(collection_list, focus_on_list, total_essay_list):
            c.append(f);c.append(e)
            second_page = requests.request('get', base_url+c[1]).content
            # 访问专题页面，获取该专题的热门链接和最新加入文章页的链接。
            soup = BeautifulSoup(second_page, "lxml")
            hot_url = soup.select(hot_selector)[0].get('href')
            new_url = soup.select(new_selector)[0].get('href')
            c += [hot_url, new_url]

        for i in collection_list:
            #print(add_url, '  ', i)
            collection_dict = {"cname": i[0], "href":i[1], "focus_number":i[2], "essays":i[3], "hot_url":i[4], "new_url":i[5]}
            db.insert(collection_dict)
            # 一句话插入数据库
            writer.writerow(collection_dict)
            # 写入csv文件

        print(add_url)
        add_url += 1
        total_collection_list += collection_list

    except Exception as e:
        print(e)
        break

csvfile.close()
# 关闭文件