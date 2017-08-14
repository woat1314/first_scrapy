from selenium import webdriver
import time
from bs4 import BeautifulSoup
import requests
import threading
import multiprocessing
import gevent
import re
from selenium.webdriver.support.ui import WebDriverWait
from gevent import monkey
from lxml import etree
from pymongo import MongoClient
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities

# Mongodb连接、数据库、集合
coon = MongoClient('127.0.0.1',27017)
# db = coon.lagou
db = coon.first_db
my_set = db.lagou_set

monkey.patch_all()

# selenium方法
options = webdriver.ChromeOptions()
# 设置中文
options.add_argument('lang=zh_CN.UTF-8')
# 更换头部
options.add_argument('User-Agent:"Mozilla/5.0 (Macintosh; Intel Mac OS X 10_12_4) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/57.0.2987.110 Safari/537.36"',
                    )
#浏览器头设置
driver = webdriver.Chrome('/usr/local/Cellar/chromedriver/chromedriver',chrome_options=options)

# phantomjs方法
# 加载无头浏览器，没有dcap部分会被拉勾识别为爬虫
# dcap = dict(DesiredCapabilities.PHANTOMJS)
# dcap["phantomjs.page.settings.userAgent"] = ( "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/57.0.2987.133 Safari/537.36" )
# driver = webdriver.PhantomJS(executable_path='/usr/local/Cellar/phantomjs/bin/phantomjs', desired_capabilities=dcap)
# 打开页面
driver.get("https://www.lagou.com/jobs/list_%E4%BA%A7%E5%93%81%E7%BB%8F%E7%90%86?px=default&yx=15k-25k&city=%E5%8D%97%E4%BA%AC#order")
wait = WebDriverWait(driver,5)

# XPATH方式————————————————问题：经验每隔3条记录才能抓取
# for i in range(0,2):
#     i=0
#     html = driver.page_source
#     selector = etree.HTML(html)
#     experiences = selector.xpath('//div[@class="p_bot"]/div[@class="li_b_l"]/text()')
#     companys = selector.xpath('//div[@class="company_name"]/a/text()')
#     titles = selector.xpath('//a[@class="position_link"]/h3/text()')
#     moneys = selector.xpath('//div[@class="li_b_l"]/span[@class="money"]/text()')
#     # experiences = selector.xpath('//*[@id = "s_position_list"] / ul / li/ div[1] / div[1] / div[2] / div / text()')
#     submits = selector.xpath('//span[@class="format-time"]/text()')
#     job_details = selector.xpath('//a[@class="position_link"]/@href')
#
#     driver.find_element_by_css_selector('div.item_con_pager > div.pager_container > span.pager_next').click()
#     time.sleep(5)
#
#     for company,title,money,experience,submit,job_detail in zip (companys,titles,moneys,experiences,submits,job_details):
#         print(company,title,money,experience,submit,job_detail)
#
#         lagou_set = {}
#         lagou_set['职位'] = title
#         lagou_set['公司名'] = company
#         lagou_set['薪水'] = money
#         lagou_set['经验要求'] = experience
#         lagou_set['发布时间'] = submit
#         lagou_set['链接地址'] = job_detail
#         my_set.insert_one(lagou_set)
#
#         i=i+1


# CSS选择器方式——————————————————问题：经验文字未去除薪水
# 注意先确定筛选条件后的翻页数量
for i in range(0,2):
    i=0
    html = driver.page_source
    soup = BeautifulSoup(html,'lxml')
    companys = soup.select('div.company_name > a')
    titles = soup.select('a.position_link > h3')
    moneys = soup.select('div.li_b_l > span.money')
    experiences = soup.select('div.p_bot > div.li_b_l')
    submit_times = soup.select('span.format-time')
    job_details = soup.select('a.position_link')
    details = soup.select('div.list_item_bot > div.li_b_r')

    driver.find_element_by_css_selector('div.item_con_pager > div.pager_container > span.pager_next').click()
    time.sleep(5)

    for company,title,money,experience,submit_time,job_detail,detail in zip(companys, titles,moneys,experiences,submit_times,job_details,details):
        title = title.text
        company = company.text
        money = money.text
        experience = experience.get_text()
        # 文字拆分和拼接
        experience = '经' + experience.split('经')[1]
        # experience = experience.split('k')[2]
        submit_time = submit_time.text
        job_detail = job_detail.get('href')
        detail = detail.text
        print(company,title,money,experience,submit_time,job_detail,detail)

        # 插表操作
        lagou_set = {}
        lagou_set['职位'] = title
        lagou_set['公司名'] = company
        lagou_set['薪水'] = money
        lagou_set['经验要求'] = experience
        lagou_set['发布时间'] = submit_time
        lagou_set['链接地址'] = job_detail
        lagou_set['特别说明'] = detail
        my_set.insert_one(lagou_set)

        # 计数加1
        i=i+1

# 从mongodb导出csv的方法：mongoexport -d lagou -c lagou_set --csv -f 发布时间,公司名,薪水,经验要求,职位,链接地址 -o mongodb_import/lagou_csv.csv
# lagou:数据库名
# lagou_set:集合名
# --csv:导出文件格式，csv/json
# -f:导出字段
# -o:导出路径