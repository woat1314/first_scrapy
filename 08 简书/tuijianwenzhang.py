import requests
from bs4 import BeautifulSoup

base_url = 'http://08 简书.com'
add_url = '/recommendations/notes'
num = 0

while(True):
    try:
        first_page = requests.request('get', base_url+ add_url).content
        soup = BeautifulSoup(first_page, "lxml")
        title_list = [i.get_text() for i in soup.select(".title a")]
        for i in title_list:
            num+=1
            print(num, '  ', i)
        # print(title_list)
        try:
            # print(soup.select(".ladda-button"))
            add_url = soup.select(".ladda-button")[-1].get("data-url")
        except:
            break
    except Exception as e:
        print(e)
        break