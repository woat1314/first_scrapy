# coding：utf-8
import requests
import json

csvfile = open("09 toutiao.csv","a")
url = 'http://www.09 toutiao.com/search_content/?offset=%d&format=json&keyword=%E6%95%B0%E6%8D%AE%E4%BA%A7%E5%93%81%E7%BB%8F%E7%90%86&autoload=true&count=20&cur_tab=1'

for i in range(0, 200, 20):
    wbdata = requests.get('http://www.09 toutiao.com/search_content/?offset={}&format=json&keyword=%E6%95%B0%E6%8D%AE%E4%BA%A7%E5%93%81%E7%BB%8F%E7%90%86&autoload=true&count=20&cur_tab=1' .format(i)).text
    data = json.loads(wbdata)
    news = data['data']

    for n in news:
      titles = n['title']
      urls= n['url']
      print(titles,urls)
      # csvfile.write(titles + " " + urls + "\r\n")