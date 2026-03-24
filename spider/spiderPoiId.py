import csv
import json
import os
import time
import datetime
import traceback

from DrissionPage import ChromiumPage, ChromiumOptions

# 爬取思路：
# 1.搜索城市city
# 2.点击‘只看*city*’，保证爬取city的景点数据
# 2.模拟页面下滑，动态加载出景点数据
# 3.爬取poiId，保存到csv文件
class SpiderPoiId(object):
    def __init__(self, url, city_link_path, sight_poiId_path):
        self.url = url
        self.city_link_path = city_link_path
        self.sight_poiId_path = sight_poiId_path

    def init(self):
        """ 创建存储文件"""
        if not os.path.exists(self.sight_poiId_path):  # 创建sight_poiId.csv,记录数据
            with open(self.sight_poiId_path, 'w', encoding='utf8', newline='') as csvfile:
                writer = csv.writer(csvfile)
                writer.writerow([
                    'city_name',
                    'sight_name',
                    'sight_poiId',
                    'tag_list',
                    'level',
                    'heat_score',
                    'score',
                    'comments_count',
                    'cover'
                ])

    def save_to_csv(self, row):
        """ 将数据写入csv文件"""
        with open(self.sight_poiId_path, 'a', encoding='utf8', newline='') as csvfile:
            writer = csv.writer(csvfile)
            writer.writerow(row)

    def get_poiId(self, spider, city_name):
        """ 爬取景点poiId"""
        try:
            # 点击搜索框
            # spider.ele('.h5_home_v1-Search icon-global-search').click()
            spider.ele('.search-index-box').click()
            # 输入城市名称 搜索框(输入框)input id = js-search-keyword-text
            spider.ele('#js-search-keyword-text').input(city_name)
            # 点击搜索按钮 button id = search_button_gs_global
            spider.ele('tag:button@@id=search_button_gs_global').click()
            spider.wait.load_start()
            sight_url = spider.ele('tag:div@@class=swiper_content').child(index=1).ele('tag:a').attr('data-appurl')
            spider.get(sight_url)
            spider.wait.load_start()
            filter_city = spider.ele('.quickScreenList').child()
            if '只看' in filter_city.text:
                filter_city.click() # 点击只看city
            time.sleep(1)
            view_box = spider.ele('.scrollViewBox')
            for i in range(20): #模拟下滑，动态获取网页元素
                view_box.scroll.to_bottom()
                time.sleep(0.5)

            for index, item in enumerate(spider.ele('.sightListScrollView').children()):
                if item is None or index == 80:
                    return

                itemobj = item.attr('itemobj')
                if itemobj is None:
                    continue
                data = json.loads(itemobj)
                data_list = []

                sight_name = data['poiName']
                sight_poiId = data['poiId']

                tag_list = []
                if 'tagNameList' in data:
                    tag_list = data['tagNameList']

                if 'sightLevelStr' in data:
                    level = data['sightLevelStr']
                else:
                    level = '未评级'

                if 'heatScore' in data:
                    heat_score = data['heatScore']
                else:
                    heat_score = '0'

                if 'commentScore' in data:
                    score = data['commentScore']
                else:
                    score = 0

                if 'commentCount' in data:
                    comments_count = data['commentCount']
                else:
                    comments_count = 0

                if 'coverImageUrl' in data:
                    cover = data['coverImageUrl']
                else:
                    cover = ''

                data_list.append(city_name)
                data_list.append(sight_name)
                data_list.append(sight_poiId)
                data_list.append(tag_list)
                data_list.append(level)
                data_list.append(heat_score)
                data_list.append(score)
                data_list.append(comments_count)
                data_list.append(cover)
                self.save_to_csv(data_list)
        except Exception as e:
            print(e.with_traceback())

    def start(self, spider):
        with open(city_link, 'r', encoding='utf8') as input:
            reader = csv.reader(input)
            next(reader)  # 跳过第一行(属性名称)

            for city_data in reader:  # 遍历所有城市
                city_name = city_data[1]
                try:
                    page = spider.new_tab()  # 创建新标签页
                    page.wait.load_start()  # 等待新标签页加载完成
                    page = spider.get_tab(0)  # 获取新标签页对象
                    page.get(url)  # 跳转到搜索页面
                    page.wait.load_start()  # 等待标签页加载
                    print(city_name)
                    self.get_poiId(page, city_name)

                    spider.close_other_tabs()  # 关闭除列表页外所有标签页，节省内存
                except:
                    print(traceback.format_exc())
                    print('get %s poiId error' % city_name)
                    continue

if __name__ == '__main__':

    url = 'https://m.ctrip.com' # 爬取网址
    city_link = 'get_poiId.csv' # 城市列表
    sight_poiId_path = 'sight_poiId3.csv' # 数据存储文件

    headless = ChromiumOptions().headless() #设置无头模式
    spider = ChromiumPage()  # 创建操作浏览器的页面对象

    spiderObj = SpiderPoiId(url, city_link, sight_poiId_path)

    start_time = datetime.datetime.now() # 记录爬取开始时间
    print('程序初始化...')
    spiderObj.init()
    print('开始爬取数据...')
    spiderObj.start(spider)
    spider.quit()
    end_time = datetime.datetime.now() # 记录爬取结束时间
    print('爬取开始时间: %s, 爬取结束时间: %s, 总用时: %s' % (start_time, end_time, end_time - start_time))






