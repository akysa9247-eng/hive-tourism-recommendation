import csv
import os
import traceback
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'hive-tourism-recommendation.settings')
django.setup()
from app.models import UserInfo, SightInfo,CommentInfo, ProvinceCity

def save_user_to_mysql(path):
    with open(path, 'r', encoding='utf8') as csvfile:
        comment_reader = csv.reader(csvfile)
        next(comment_reader)
        for comment in comment_reader:
            try:
                userinfo = UserInfo.objects.filter(user_name=comment[1])
                if userinfo.exists():
                    print('%s is register' % comment[1])
                else:
                    UserInfo.objects.create(
                        user_name=comment[1],
                    )
            except:
                print(traceback.format_exc())
                print('save_user_to_mysql error')
                continue

def save_sight_to_mysql(path):
    with open(path, 'r', encoding='utf8') as csvfile:
        sight_reader = csv.reader(csvfile)
        next(sight_reader)
        for sight in sight_reader:
            try:
                SightInfo.objects.create(
                    sight_id=int(sight[0]),
                    sight_name=sight[1],
                    province=sight[2],
                    city=sight[3],
                    tag_list=sight[4],
                    level=sight[6],
                    heat_score=sight[7],
                    score=sight[8],
                    address=sight[10],
                    telephone=sight[11],
                    intro=sight[12],
                    opening_time=sight[13],
                    img_list=sight[14],
                    cover=sight[15]
                )
            except:
                print(traceback.format_exc())
                print('save_sight_to_mysql error')
                continue

def save_comment_to_mysql(path):
    with open(path, 'r', encoding='utf8') as csvfile:
        comment_reader = csv.reader(csvfile)
        next(comment_reader)
        for comment in comment_reader:
            try:
                CommentInfo.objects.create(
                    comment_id=comment[0],
                    user_name=comment[1],
                    sight_id=comment[2],
                    content=comment[3],
                    score=comment[4],
                    date=comment[5]
                )
            except:
                print(traceback.format_exc())
                print('save_comment_to_mysql error')
                continue

def save_province_city_to_mysql(path):
    with open(path, 'r', encoding='utf8') as csvfile:
        reader = csv.reader(csvfile)
        next(reader)
        for data in reader:
            try:
                ProvinceCity.objects.create(
                    province=data[0],
                    city=data[1],
                    city_link=data[2]
                )
            except:
                print(traceback.format_exc())
                print('save_province_city_to_mysql error')
                continue



