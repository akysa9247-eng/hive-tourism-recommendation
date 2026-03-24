#encoding=utf-8

import json
import csv
import os
import time
import datetime
import traceback

import bcrypt
import django
import pandas as pd

from app.utils import getTime
from util import filter, match, csv_to_mysql
from DrissionPage import ChromiumPage, ChromiumOptions
from DrissionPage import SessionPage
from DrissionPage import WebPage
from DrissionPage.errors import ElementNotFoundError
from DrissionPage.common import Settings

Settings.singleton_tab_obj=False
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'hive-tourism-recommendation.settings')
django.setup()
from app.models import SightInfo, UserInfo, CommentInfo, AdminInfo  # 注意在setup()之后导入！

class SpiderMain(object):
    def __init__(self, city_link_path, sight_poiId_path, sight_data_path, comment_data_path):
        self.comments_url = 'https://m.ctrip.com/restapi/soa2/13444/json/getCommentCollapseList' # 爬取评论数据的url
        self.city_link_path = city_link_path # 城市链接文件
        self.sight_poiId_path = sight_poiId_path # 景点id数据文件
        self.sight_data_path = sight_data_path # 景点数据存储文件
        self.comment_data_path = comment_data_path # 评论数据存储文件

    def init(self):
        """创建存储文件"""
        if not os.path.exists(self.sight_data_path):  # 创建sight_data.csv,记录景点数据
            with open(self.sight_data_path, 'w', encoding='utf8', newline='') as sight_csv:
                sight_writer = csv.writer(sight_csv)
                sight_writer.writerow([
                    'sight_id',
                    'sight_name',
                    'province',
                    'city',
                    'tag_list',
                    'detail_url',
                    'level',
                    'heat_score',
                    'score',
                    'comments_count',
                    'address',
                    'telephone',
                    'intro',
                    'opening_time',
                    'img_list',
                    'cover'
                ])

        if not os.path.exists(self.comment_data_path):  # 创建comment_data.csv,记录评论数据
            with open(self.comment_data_path, 'w', encoding='utf8', newline='') as comment_csv:
                comment_writer = csv.writer(comment_csv)
                comment_writer.writerow([
                    'comment_id',
                    'sight_id',
                    'user_name',
                    'content',
                    'score',
                    'date'
                ])

    def save_to_csv(self, path, row):
        """将数据写入csv文件"""
        with open(path, 'a', encoding='utf8', newline='') as csvfile:
            writer = csv.writer(csvfile)
            writer.writerow(row)

    def create_request_data(poiId, page):
        data = {
            "arg": {
                "channelType": 2,
                "collapseType": 0,
                "commentTagId": 0,
                "pageIndex": str(page + 1),
                "pageSize": 10,
                "poiId": int(poiId),
                "sourceType": 1,
                "sortType": 3,
                "starType": 0
            },
            "head": {
                "cid": "09031058118828194114",
                "ctok": "",
                "cver": "1.0",
                "lang": "01",
                "sid": "8888",
                "syscode": "09",
                "auth": "",
                "xsid": "",
                "extension": []
            }
        }
        return data

    def get_poiId_data(self, city, sight_name):
        """获取景点id"""
        try:
            df = pd.read_csv(self.sight_poiId_path)
            items = df.loc[(df['city_name'] == city) & (df['sight_name'] == sight_name)] #根据城市名称和景点名称查找景点信息

            if items.empty:
                return
            dataframe = items.iloc[0]

            city_name = dataframe['city_name']
            poiId = dataframe['sight_poiId']
            tag_list = dataframe['tag_list']
            level = dataframe['level']
            heat_score = dataframe['heat_score']
            score = dataframe['score']
            comments_count = dataframe['comments_count']
            cover = dataframe['cover']

            data_list = []
            data_list.append(city_name)
            data_list.append(int(poiId))
            data_list.append(tag_list)
            data_list.append(level)
            data_list.append(heat_score)
            data_list.append(score)
            data_list.append(comments_count)
            data_list.append(cover)
            return data_list
        except:
            print(traceback.format_exc())
            print('%s poiId is None' % sight_name)
            return

    def spider_sight_comment_data(self, poiId, pageNum):
        """ 爬取评论数据 """
        for page in range(0, pageNum):  #设置评论爬取页数
            # 设置请求头信息，传入景点ID和爬取的页数
            data = self.create_request_data(poiId=poiId,page=page)
            spider_comment = SessionPage() #创建一个收发数据包的对象
            spider_comment.post(url=self.comments_url, data=json.dumps(data))  # 发送请求
            comments_list = json.loads(spider_comment.response.text)['result']['items']  # 将接收的数据转化为json格式，并提取信息
            if comments_list:
                for comment in comments_list:  # 提取评论数据
                    try:
                        comments = []
                        comment_id = comment['commentId']
                        user_name = comment['userInfo']['userId']
                        content = filter.remove_special_characters(comment['content'])
                        date = match.match_date(comment['publishTypeTag'])
                        score = comment['score']
                        # 封装评论数据
                        comments.append(comment_id)
                        comments.append(user_name)
                        comments.append(poiId)
                        comments.append(content)
                        comments.append(score)
                        comments.append(date)
                        # 将数据写入文件
                        self.save_to_csv(self.comment_data_path, comments)
                    except:
                        continue

    def spider_sight_data(self, province, city, sight_tab):
        """"爬取景点数据"""
        base_info = sight_tab.s_ele('.baseInfoMain')

        sight_name = base_info.ele('.title').ele('tag:h1').text #景点名称
        poiId_data = self.get_poiId_data(city, sight_name) #获取景点id
        if poiId_data is None:
            return

        detail_url = sight_tab.url #景点url
        city_name = poiId_data[0]
        if city_name != city:
            return

        # 景点数据
        sight_id = poiId_data[1]
        tag_list = poiId_data[2]
        level = poiId_data[3]
        heat_score = poiId_data[4]
        score = poiId_data[5]
        comments_count = poiId_data[6]
        cover = poiId_data[7]

        # 详情爬取
        address = None #景点地址
        telephone = None #官方电话
        opening_time = None #开放时间
        try:
            items = base_info.ele('.baseInfoContent').s_eles('.baseInfoItem')
            for item in items:
                item_title = item.ele('.baseInfoTitle').text
                if ('地址' in item_title):
                    address = item.ele('.baseInfoText').text
                if ('官方电话' in item_title):
                    telephone = item.ele('.baseInfoText').text.split(',')[0]
                if ('开放时间' in item_title):
                    opening_time = filter.get_opening_time(item.ele('.baseInfoText cursor openTimeText').text)
        except ElementNotFoundError:
            pass

        # 景点介绍
        try:
            intro = filter.remove_special_characters(sight_tab.ele('.LimitHeightText').text)
        except ElementNotFoundError:
            intro = ''

        img_list = [] #景点图片列表
        try:
            for img in sight_tab.ele('.swiper-wrapper').children():
                img_list.append(match.match_url(img.attr('style')).strip(')'))
        except ElementNotFoundError:
            img_list = ''

        # 封装景点数据
        sight_data = []
        sight_data.append(sight_id)
        sight_data.append(sight_name)
        sight_data.append(province)
        sight_data.append(city_name)
        sight_data.append(tag_list)
        sight_data.append(detail_url)
        sight_data.append(level)
        sight_data.append(heat_score)
        sight_data.append(score)
        sight_data.append(comments_count)
        sight_data.append(address)
        sight_data.append(telephone)
        sight_data.append(intro)
        sight_data.append(opening_time)
        sight_data.append(json.dumps(img_list))
        sight_data.append(cover)
        # 景点数据存入csv文件
        self.save_to_csv(self.sight_data_path, sight_data)

        # 评论爬取
        self.spider_sight_comment_data(sight_id, 5)

    def spider_sigth_link(self, spider):
        """爬取城市景点链接"""
        sight_links = []
        sight_link_list = spider.s_eles('.list_mod2')
        for item in sight_link_list:
            sight_links.append(str(item.ele('.rdetailbox').ele('tag:dt').child('tag:a').link))
        return sight_links

    def spider_main(self, province, city, spider, spider_city):
        """"爬取数据"""
        sight_link_list = self.spider_sigth_link(spider_city) #获取该页所有景点的详情页网址
        sight_tab = spider.new_tab()  # 创建一个标签页，用于访问景点详情页网址
        spider.wait.new_tab()  # 等待标签页出现
        for index, sight_link in enumerate(sight_link_list):
            print('正在爬取该页第 %s 个景点，网址：%s' % (str(index + 1), sight_link))
            sight_tab.get(url=sight_link)   #访问景点详情页网址
            self.spider_sight_data(province, city, sight_tab)  #爬取景点数据
        sight_tab.close()

    def start(self,):
        with open(self.city_link_path, 'r', encoding='utf8') as readerfile:
            reader = csv.reader(readerfile)
            next(reader)  # 跳过第一行的属性名称

            co = ChromiumOptions().headless()  # 设置无头模式，关闭旧的无头浏览器再启动新的
            spider = ChromiumPage(co)  # 创建浏览器控制对象
            spider_city = spider.new_tab()  # 创建一个标签页，用于查询城市每页的景点
            spider.wait.new_tab()  # 等待标签页出现
            try:
                for city_data in reader:  # 遍历所有城市
                    if not city_data:  # 城市数据为空跳过
                        continue
                    spider_url = city_data[2]  # 城市景点网址
                    spider_city.get(spider_url)
                    spider_city.wait.load_start()  # 等待标签页加载

                    if not spider_city.url_available:  # 若网址不可用，跳过
                        continue
                    for page in range(1, 8):  # 爬取城市的前7页的景点数据
                        try:
                            province = city_data[0]  # 获取省份
                            city = city_data[1]  # 获取城市名称
                            print('正在爬取的城市是 %s，正在爬取第 %s 页的景点数据， 网址：%s' % (
                                city,
                                page,
                                spider_city.url
                            ))
                            self.spider_main(province, city, spider, spider_city)

                            # 翻页
                            spider_city('下一页').click()  # 点击页面中的'下一页'
                            spider_city.wait.load_start()  # 等待页面资源加载
                        except Exception as e:
                            print(traceback.format_exc())
                            print('该页爬取失败')
                            continue

                    spider_city.reconnect(1)  #重新连接，释放内存 ，防止浏览器占用内存过大 导致运行效率低

                spider.quit()
            except:
                spider.quit()
                print(traceback.format_exc())

if __name__ == '__main__':
    city_link_path = './city.csv'  #爬取城市的链接
    sight_poiId_path = 'sight_poiId.csv'  #景点id数据文件
    sight_data_path = './sight_data1.csv'  #景点数据存储文件
    comment_data_path = './comment_data2.csv'  #评论数据存储文件

    # spiderObj = SpiderMain(city_link_path, sight_poiId_path, sight_data_path, comment_data_path)

    # start_time = datetime.datetime.now() # 记录爬取开始时间
    # print('程序初始化...')
    # spiderObj.init()
    # print('开始爬取数据...')
    # spiderObj.start()
    # end_time = datetime.datetime.now() # 记录爬取结束时间
    # print('爬取开始时间: %s, 爬取结束时间: %s, 总用时: %s' % (start_time, end_time, end_time - start_time))

    csv_to_mysql.save_sight_to_mysql(sight_data_path) #将景点数据保存到mysql
    # csv_to_mysql.save_province_city_to_mysql(city_link_path)