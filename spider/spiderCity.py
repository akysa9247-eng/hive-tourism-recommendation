import csv
import os
import datetime

from DrissionPage import SessionPage
from util import match

class SpiderCity(object):
    def __init__(self, url, city_data_path):
        self.url = url
        self.city_data_path = city_data_path

    def init(self):
        """ 创建数据存储文件 """
        if not os.path.exists(self.city_data_path):
            with open(self.city_data_path, 'w', encoding='utf8', newline='') as csvfile:
                writer = csv.writer(csvfile)
                writer.writerow(['province', 'city', 'cityLink'])

    def save_to_csv(self, row):
        """将数据写入csv文件"""
        with open(city_data_path, 'a', encoding='utf8', newline='') as csvfile:
            writer = csv.writer(csvfile)
            writer.writerow(row)

    def spider_city(self, page):
        """ 爬取城市名称和城市链接 """
        main_city = page.s_eles('.city-selector-tab-main-city')
        for item in main_city:
            spider_province = item.s_ele('.city-selector-tab-main-city-title').text
            if not spider_province:  #跳过没有省份/自治区/直辖市信息的标签
                continue
            city_list = item.s_eles('.city-selector-tab-main-city-list-item') #爬取省份/自治区/直辖市下的城市信息
            for city in city_list:
                province = spider_province
                city_name = city.attr('title') #获取城市名称
                city_link = str(city.link).replace('place', 'sight') #获取网址并将网址中的place替换为sight
                # print(province, city_name, city_link)
                if spider_province in ['港澳台', '直辖市']:  # 直辖市、港澳台等‘省份’更换为对应省份
                    match_province = match.get_province(city_name)
                    if match_province is not None:
                        province = match_province
                self.save_to_csv([province, city_name, city_link]) #将省份、城市名称和城市网址写入city.csv

    def start(self):
        spider = SessionPage()
        spider.get(self.url)

        if spider.url_available:
            self.spider_city(spider)

if __name__ == '__main__':
    url = 'https://you.ctrip.com/'
    city_data_path = 'city.csv'

    spiderObj = SpiderCity(url, city_data_path)
    start_time = datetime.datetime.now() # 记录爬取开始时间
    print('程序初始化...')
    spiderObj.init()
    print('准备开始爬取数据...')
    spiderObj.start()
    end_time = datetime.datetime.now() # 记录爬取结束时间
    print('爬取开始时间: %s, 爬取结束时间: %s, 总用时: %s' % (start_time, end_time, end_time - start_time))
