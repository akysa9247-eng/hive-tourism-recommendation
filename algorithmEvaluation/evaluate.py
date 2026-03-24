
import datetime
import os
import django
import item_cf_recommendations, item_cf_recommendations_penalty

from collections import defaultdict
from itertools import chain

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'hive-tourism-recommendation.settings')
django.setup()
from app.models import CommentInfoTest, SightInfo, UserRecommendationValuesTest, UserRecommendationValuesWithPenaltyTest, UserFavoritesTest

def calculate_accuracy(recommended_sights, liked_sights):
    """计算准确率"""
    accuracy = len(set(recommended_sights) & set(liked_sights)) / len(recommended_sights)
    return accuracy


def calculate_recall(recommended_sights, liked_sights):
    """计算召回率"""
    recall = len(set(recommended_sights) & set(liked_sights)) / len(liked_sights)
    return recall

# 获取用户喜欢的景点ID列表
def get_liked_sights(user_id):
    comment_liked_sights = CommentInfoTest.objects.filter(user_id=user_id, score__gt=3).values_list('sight_id', flat=True)
    favorite_liked_sights = UserFavoritesTest.objects.filter(user_id=user_id).values_list('sight_id', flat=True)
    merged_sights = list(set(chain(comment_liked_sights, favorite_liked_sights)))
    return merged_sights

# 获取所有景点的ID列表
def get_all_sights():
    all_sights = SightInfo.objects.values_list('sight_id', flat=True)
    return list(all_sights)

def mock_recommend_sights(user_id, k):
    item_cf_recommendations.recommend_sights(user_id=user_id, k=k)

def mock_recommend_sights_with_penalty(user_id, k):
    item_cf_recommendations_penalty.recommend_sights(user_id=user_id, k=k)

# 测试推荐算法的函数
def test_recommend_algorithm(user_id, ks=[5, 10, 15, 20]):
    print('Item-CF算法：')
    print('start:', datetime.datetime.now())
    # 获取用户真正喜欢的景点
    liked_sights = get_liked_sights(user_id)

    # 启动算法
    mock_recommend_sights(user_id, max(ks))
    print('end:', datetime.datetime.now())

    results = defaultdict(dict)
    # 测试不同的k值
    for k in ks:
        # 从数据库中获取推荐结果
        recommended_sights = UserRecommendationValuesTest.objects.filter(user_id=user_id).order_by('-recommendation_value')[:k].values_list('sight_id', flat=True)

        # 计算准确率和召回率
        accuracy = calculate_accuracy(list(recommended_sights), liked_sights)
        recall = calculate_recall(list(recommended_sights), liked_sights)
        # 存储结果
        results[k]['accuracy'] = accuracy
        results[k]['recall'] = recall

        # 打印或返回结果
    for k, metrics in results.items():
        print(
            f"k={k}: 准确率={metrics['accuracy']:.2f}, 召回率={metrics['recall']:.2f}")

def test_recommend_algorithm_with_penalty(user_id, ks=[5, 10, 15, 20]):
    print('融入惩罚因子的Item-CF算法：')
    print('start:', datetime.datetime.now())
    # 获取用户真正喜欢的景点
    liked_sights = get_liked_sights(user_id)

    mock_recommend_sights_with_penalty(user_id, max(ks))
    print('end:', datetime.datetime.now())

    results = defaultdict(dict)
    # 测试不同的k值
    for k in ks:
        recommended_sights = UserRecommendationValuesWithPenaltyTest.objects.filter(user_id=user_id).order_by(
            '-recommendation_value')[:k].values_list('sight_id', flat=True)

        # 计算准确率和召回率
        accuracy = calculate_accuracy(list(recommended_sights), liked_sights)
        recall = calculate_recall(list(recommended_sights), liked_sights)
        # 存储结果
        results[k]['accuracy'] = accuracy
        results[k]['recall'] = recall

        # 打印或返回结果
    for k, metrics in results.items():
        print(
            f"k={k}: 准确率={metrics['accuracy']:.2f}, 召回率={metrics['recall']:.2f}")

if __name__ == '__main__':
    user_id = 1081
    test_recommend_algorithm(user_id)
    print('====================================')
    test_recommend_algorithm_with_penalty(user_id)