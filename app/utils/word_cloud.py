import os

import bcrypt
import jieba
import re
import django
import matplotlib.pyplot as plt
from wordcloud import WordCloud
from PIL import Image
from collections import Counter
from PIL import ImageFile

from app.utils import getTime

ImageFile.LOAD_TRUNCATED_IMAGES = True
Image.MAX_IMAGE_PIXELS = None

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'hive-tourism-recommendation.settings')
django.setup()
from app.models import SpiderCommentInfo, SightInfo, AdminInfo


def load_stopwords():
    stopword_path = '//app/files/stop_word.txt'
    with open(stopword_path, 'r', encoding='utf-8') as f:
        stopwords = set([word.strip() for word in f.readlines()])
    return stopwords


def word_cloud(top_n, top_n_words, output_path):

    wordcloud_data = dict(top_n_words)
    wordcloud = WordCloud(
        width=3090,
        height=1910,
        background_color='white',
        max_words=top_n,
        scale=32,
        margin=5,
        font_path='C:/Users/allen/AppData/Local/Microsoft/Windows/Fonts/方正粗黑宋简体.ttf',
    ).generate_from_frequencies(wordcloud_data)

    plt.figure(1)
    plt.imshow(wordcloud, interpolation='bilinear')
    plt.axis('off')

    # 保存词云图到指定路径
    plt.savefig(output_path)

def comment_word_cloud(top_n=10, output_path='C:/Users/allen/Desktop/hive-tourism-recommendation/static/wordcloud/commentCloud/comment_cloud.png'):

    word_counter = Counter()
    # 加载停用词
    stopwords = load_stopwords()

    for comment in SpiderCommentInfo.objects.all().iterator():
        # 使用jieba 精确分词
        words = jieba.lcut(comment.content)
        # 过滤停用词
        filtered_words = [word for word in words if
                          len(word) > 1 and not re.match(r'^\W+$', word) and word not in stopwords]
        # 更新词频计数器
        word_counter.update(filtered_words)

    # 取出词频最高的前n个词
    top_n_words = word_counter.most_common(top_n)

    word_cloud(top_n, top_n_words, output_path)

def sight_intro_word_cloud(top_n=10, output_path='C:/Users/allen/Desktop/hive-tourism-recommendation/static/wordcloud/sightIntroCloud/sight_intro_cloud.png'):
    # 初始化词频计数器
    word_counter = Counter()

    # 加载停用词
    stopwords = load_stopwords()

    for sight in SightInfo.objects.all().iterator():
        # 使用jieba 精确分词
        words = jieba.lcut(sight.intro)
        # 过滤停用词
        filtered_words = [word for word in words if
                          len(word) > 1 and not re.match(r'^\W+$', word) and word not in stopwords]
        # 更新词频计数器
        word_counter.update(filtered_words)

    # 取出词频最高的前n个词
    top_n_words = word_counter.most_common(top_n)

    word_cloud(top_n, top_n_words, output_path)

if __name__ == '__main__':
    # comment_word_cloud(top_n=50) #生成用户评论词云图
    # sight_intro_word_cloud(top_n=50) #生成景点简介词云图
    adminname = 'admin'
    password = 'admin'
    contact_info = '1753411615@qq.com'
    # 使用bcrypt哈希密码
    hashed_password = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt()).decode('utf-8')

    # 创建新用户并保存
    admin = AdminInfo(adminname=adminname, password=hashed_password, contact_info=contact_info,
                      create_time=getTime.get_datetime())
    admin.save()