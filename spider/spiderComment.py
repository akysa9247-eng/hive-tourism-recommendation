import csv
import json
import os
import time
import datetime

import pandas as pd
from DrissionPage import SessionPage

from util import match
from util import filter

class SpiderComment(object):
    def __init__(self, spider_comment_path, sight_poiId_path, comment_data_path):
        self.comments_url = 'https://m.ctrip.com/restapi/soa2/13444/json/getCommentCollapseList'  # 爬取评论数据的url
        self.spider_comment_path = spider_comment_path
        self.sight_poiId_path = sight_poiId_path
        self.comment_data_path = comment_data_path

    def init(self):
        if not os.path.exists(self.comment_data_path):  # 创建comment_data.csv,记录评论数据
            with open(self.comment_data_path, 'w', encoding='utf8', newline='') as comment_csv:
                comment_writer = csv.writer(comment_csv)
                comment_writer.writerow([
                    'comment_id',
                    'user_name',
                    'sight_id',
                    'content',
                    'score',
                    'date'
                ])

    def save_to_csv(self, path, row):
        with open(path, 'a', encoding='utf8', newline='') as csvfile:
            writer = csv.writer(csvfile)
            writer.writerow(row)

    def get_poiId_data(self, sight_name):  # 获取景点的poiId
        try:
            poiId_csv = pd.read_csv(self.sight_poiId_path, header=0, sep=',', index_col='sight_name')
            items = poiId_csv.loc[[sight_name]]  # dataframe若查询到一行返回的值Series，若多套一层[]，则查询到一行返回dataframe
            city_name = items.iloc[0]['city_name']
            poiId = items.iloc[0]['sight_poiId']
            level = items.iloc[0]['level']
            heat_score = items.iloc[0]['heat_score']
            comment_score = items.iloc[0]['comment_score']
            comments_count = items.iloc[0]['comments_count']
            cover = items.iloc[0]['cover']

            data_list = []
            data_list.append(city_name)
            data_list.append(int(poiId))
            data_list.append(level)
            data_list.append(heat_score)
            data_list.append(comment_score)
            data_list.append(comments_count)
            data_list.append(cover)
            return data_list
        except:
            print('%s poiId is None' % sight_name)
            return None

    def spider_sight_comment_data(self, city_name, sight_name, poiId):
        for page in range(0, 2):  # 设置评论爬取页数
            # 设置请求头信息
            data = {"arg": {"channelType": 2, "collapseType": 0, "commentTagId": 0, "pageIndex": str(page + 1),
                            "pageSize": 10, "poiId": poiId, "sourceType": 1, "sortType": 3, "starType": 0},
                    "head": {"cid": "09031058118828194114", "ctok": "", "cver": "1.0", "lang": "01", "sid": "8888",
                             "syscode": "09", "auth": "", "xsid": "", "extension": []}
                    }

            spider_comment = SessionPage()
            spider_comment.post(url=self.comments_url, data=json.dumps(data))  # 发送请求
            comments_list = json.loads(spider_comment.response.text)['result']['items']  # 将接收的str数据转化为json格式 并提取信息
            if comments_list:
                for comment in comments_list:  # 提取需要的信息
                    print('comment', comment)
                    print(comment['aaa'])
                    comments = []
                    comment_id = comment['commentId']
                    user_name = comment['userInfo']['userId']
                    content = filter.remove_emoji(filter.remove_line(comment['content']))
                    date = match.match_date(comment['publishTypeTag'])
                    score = comment['score']
                    # 封装评论数据
                    comments.append(comment_id)
                    comments.append(user_name)
                    comments.append(poiId)
                    comments.append(content)
                    comments.append(score)
                    comments.append(date)
                    self.save_to_csv(self.comment_data_path, comments)

    def start(self):
        with open(self.spider_comment_path, 'r', encoding='utf8') as readerfile:
            reader = csv.reader(readerfile)
            next(reader)  # 跳过第一行的属性名称

            for sight_data in reader:  # 遍历所有城市
                if not sight_data:  # 数据为空跳过
                    continue

                city_name = sight_data[0]
                sight_name = sight_data[1]
                if not sight_name:
                    continue

                data_list = self.get_poiId_data(sight_name)
                sight_id = data_list[1]
                print(sight_name, sight_id)

                self.spider_sight_comment_data(city_name, sight_name, sight_id)
                time.sleep(1)

if __name__ == '__main__':
    spider_comment_path = 'error.csv'
    sight_poiId_path = './sight_poiId.csv'
    comment_data_path = './comment_data2.csv'

    spiderObj = SpiderComment(spider_comment_path, sight_poiId_path, comment_data_path)

    start_time = datetime.datetime.now() # 记录爬取开始时间
    spiderObj.init()
    spiderObj.start()
    end_time = datetime.datetime.now() # 记录爬取结束时间
    print('爬取开始时间: %s, 爬取结束时间: %s, 总用时: %s' % (start_time, end_time, end_time - start_time))

