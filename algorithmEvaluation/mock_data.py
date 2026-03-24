
import random
import string
import django
import os

from faker import Faker

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'hive-tourism-recommendation.settings')
django.setup()
from app.models import UserFavoritesTest, CommentInfoTest, UserBrowsesTest, UserInfoTest, SightInfo

fake = Faker()
# 生成随机字符串的函数
def generate_random_string(length):
    letters_and_digits = string.ascii_letters + string.digits
    return ''.join(random.choice(letters_and_digits) for i in range(length))

def generate_random_score():
    weights = [1, 1, 1, 3, 3]  # 1到3的权重为1，4和5的权重为3

    score = random.choices(range(1, 6), weights=weights, k=1)[0]
    return score

def mock_user_info_data(user_num=10):

    for i in range(1, user_num + 1):
        username = 'user' + str(i)
        password = generate_random_string(10)
        sex = random.choice(['男', '女'])  # 随机性别
        address = generate_random_string(50)  # 随机地址
        avatar = 'avatar/default.jpg'  # 默认头像
        intro = username # 随机介绍
        create_time = fake.date_time_between(start_date="-30d", end_date="now")

        UserInfoTest.objects.create(
            username=username,
            password=password,
            sex=sex,
            address=address,
            avatar=avatar,
            intro=intro,
            create_time=create_time
        )

def mock_user_favorite_data():

    user_count = UserInfoTest.objects.count()

    # 获取sight_info表中的所有sight_id
    sight_ids = SightInfo.objects.all().values_list('sight_id', flat=True)

    # 设置每个用户的收藏数量区间
    favorites_per_user = random.randint(2, 8)

    # 循环遍历用户并随机选择景点
    for user_id in range(1, user_count + 1):
        for _ in range(favorites_per_user):
            sight_id = random.choice(sight_ids)
            favorited_time = fake.date_time_between(start_date="-30d", end_date="now")

            UserFavoritesTest.objects.create(
                user_id=user_id,
                sight_id=sight_id,
                favorited_time=favorited_time
            )

            if random.choice([True, False]):
                content = fake.text(max_nb_chars=10)
                score = generate_random_score()
                date = fake.date_time_between(start_date="-30d", end_date="now").strftime('%Y-%m-%d %H:%M:%S')

                CommentInfoTest.objects.create(
                    user_id=user_id,
                    sight_id=sight_id,
                    content=content,
                    score=score,
                    date=date
                )

def mock_user_browse_data():

    user_count = UserInfoTest.objects.count()

    # 获取sight_info表中的所有sight_id
    sight_ids = SightInfo.objects.all().values_list('sight_id', flat=True)

    # 设置每个用户的浏览数量区间
    browses_per_user = random.randint(1, 3)

    # 循环遍历用户并随机选择景点
    for user_id in range(1, user_count + 1):
        for _ in range(browses_per_user):
            sight_id = random.choice(sight_ids)
            browse_time = fake.date_time_between(start_date="-30d", end_date="now")  # 生成过去30天内的随机日期时间

            UserBrowsesTest.objects.create(
                user_id=user_id,
                sight_id=sight_id,
                browse_time=browse_time
            )

def mock_user_comment_data():

    user_count = UserInfoTest.objects.count()

    # 获取sight_info表中的所有sight_id
    sight_ids = SightInfo.objects.all().values_list('sight_id', flat=True)
    # 循环遍历用户
    for user_id in range(1, user_count + 1):
        comments_per_user = random.randint(3,5)
        # 随机选择5个景点
        for _ in range(comments_per_user):
            sight_id = random.choice(sight_ids)
            content = fake.text(max_nb_chars=10)  # 生成随机文本作为评论内容
            score = generate_random_score()
            date = fake.date_time_between(start_date="-30d", end_date="now")\
                .strftime('%Y-%m-%d %H:%M:%S')  # 生成过去30天内的随机日期时间

            CommentInfoTest.objects.create(
                user_id=user_id,
                sight_id=sight_id,
                content=content,
                score=score,
                date=date
            )

if __name__ == '__main__':
    mock_user_info_data(user_num=10000)
    mock_user_favorite_data()
    mock_user_browse_data()
    mock_user_comment_data()