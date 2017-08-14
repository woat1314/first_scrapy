from selenium import webdriver
import time
from bs4 import BeautifulSoup

driver = webdriver.Chrome('/usr/local/Cellar/chromedriver/chromedriver')

driver.get("http://www.zhihu.com")       #打开知乎我们要登录
time.sleep(2)                            #让操作稍微停一下
driver.find_element_by_link_text('登录').click() #找到‘登录’按钮并点击
time.sleep(2)
#找到输入账号的框，并自动输入账号 这里要替换为你的登录账号
driver.find_element_by_name('account').send_keys('13776628977')
time.sleep(2)
#密码，这里要替换为你的密码
driver.find_element_by_name('password').send_keys('Wwz_Ljj1314')
time.sleep(2)
#输入浏览器中显示的验证码，这里如果知乎让你找烦人的倒立汉字，手动登录一下，再停止程序，退出#浏览器，然后重新启动程序，直到让你输入验证码
# yanzhengma=input('验证码:')
# driver.find_element_by_name('captcha').send_keys(yanzhengma)
#找到登录按钮，并点击
driver.find_element_by_css_selector('div.button-wrapper.command > button').click()

#将登录页cookie带入后续页面
cookie=driver.get_cookies()
time.sleep(3)
driver.get('https://www.zhihu.com/search?type=content&q=python')
time.sleep(5)

#知乎关键词搜索和话题加载方式不一样；关键词加载需要点击"更多"；话题加载滚屏即可
driver.find_element_by_css_selector('a.zg-btn-white.zu-button-more').click()
time.sleep(5)
driver.find_element_by_css_selector('a.zg-btn-white.zu-button-more ').click()
time.sleep(5)

html = driver.page_source  #与普通页面爬取重要的区别
soup1 = BeautifulSoup(html,'lxml')
# print(soup1)

titles = soup1.select('div.title > a')
urls = soup1.select('div.title > a.js-title-link')

titles_alls = []
urls_alls = []

for title in titles:
    titles_alls.append(title.get_text())

for url in urls:
    urls_alls.append('http://www.zhihu.com'+url.get('href'))


for titles_all,urls_all in zip(titles_alls,urls_alls):
    data={
        'title':titles_all,
        'url':urls_all
    }
    print(data)



