import os
import django
import math
import numpy as np
from decimal import Decimal
# from sklearn.metrics.pairwise import cosine_similarity

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'hive-tourism-recommendation.settings')
django.setup()
from app.models import CommentInfo, UserInfo, SightInfo, AdsSightHeatScoreTop10Stats
from django.db.models import Count

# def calculate_similarity(user1_ratings, user2_ratings):
#     """余弦相似度：计算两个用户之间的相似度"""
#     common_sights = set(user1_ratings.keys()) & set(user2_ratings.keys())
#     if not common_sights:
#         return 0
#
#     ratings1 = np.array([user1_ratings[sight] for sight in common_sights])
#     ratings2 = np.array([user2_ratings[sight] for sight in common_sights])
#
#     similarity = cosine_similarity(ratings1.reshape(1, -1), ratings2.reshape(1, -1))[0][0]
#     return similarity

def get_user_ratings(username):
    """获取用户的评分数据"""
    comments = CommentInfo.objects.filter(username=username).values('sight_id', 'score')
    ratings = {comment['sight_id']: comment['score'] for comment in comments}
    return ratings

def get_sight_frequencies():
    """统计每个景点被评价过的次数"""
    sight_frequencies = CommentInfo.objects.values('sight_id').annotate(freq=Count('sight_id')).order_by('sight_id')
    # 转换为字典
    return {sight['sight_id']: sight['freq'] for sight in sight_frequencies}

# 缓存景点评价频次
SIGHT_FREQUENCIES = get_sight_frequencies()

# def calculate_adjusted_cosine_similarity(user1_ratings, user2_ratings):
#     """ 计算修正的余弦相似度，并融入惩罚热门景点因子 """
#     common_sights = set(user1_ratings.keys()) & set(user2_ratings.keys())
#     if not common_sights:
#         return 0
#
#     # 计算向量的点积
#     dot_product = sum(user1_ratings[sight] * user2_ratings[sight] for sight in common_sights)
#
#     # 计算向量A和向量B的模长
#     norm_user1 = math.sqrt(sum(user1_ratings[sight] ** 2 for sight in common_sights))
#     norm_user2 = math.sqrt(sum(user2_ratings[sight] ** 2 for sight in common_sights))
#
#
#     # 计算热门景点频次的惩罚因子
#     sight_frequencies = [SIGHT_FREQUENCIES[sight] for sight in common_sights]
#
#     penalty_factor = math.prod([math.log(1 + freq) for freq in sight_frequencies]) ** (1 / len(sight_frequencies))
#
#     # 转换为Decimal类型进行计算
#     dot_product = Decimal(str(dot_product))
#     norm_user1 = Decimal(str(norm_user1))
#     norm_user2 = Decimal(str(norm_user2))
#     penalty_factor = Decimal(str(penalty_factor))
#
#     # 使用融入热门景点频次的惩罚因子来修正相似度
#     adjusted_cosine_similarity = dot_product / (norm_user1 * norm_user2 * penalty_factor)
#
#     return adjusted_cosine_similarity


def calculate_adjusted_cosine_similarity(sight1_scores, sight2_scores, sight1_id, sight2_id):
    common_users = set(sight1_scores.keys()) & set(sight2_scores.keys())

    if not common_users:
        return Decimal(0)

    # 计算点积
    dot_product = sum(sight1_scores[user] * sight2_scores[user] for user in common_users)

    # 计算两个向量的模长
    norm_sight1 = math.sqrt(sum(sight1_scores[user] ** 2 for user in common_users))
    norm_sight2 = math.sqrt(sum(sight2_scores[user] ** 2 for user in common_users))

    # 获取两个景点的评价频率
    sight1_frequency = SIGHT_FREQUENCIES.get(sight1_id, 0)
    sight2_frequency = SIGHT_FREQUENCIES.get(sight2_id, 0)

    # 计算惩罚因子，降低热门景点的权重
    penalty_factor = math.sqrt(math.log(1 + sight1_frequency, 10) * math.log(1 + sight2_frequency, 10))

    # 转换为Decimal类型以提高精度
    dot_product = Decimal(str(dot_product))
    norm_sight1 = Decimal(str(norm_sight1))
    norm_sight2 = Decimal(str(norm_sight2))
    penalty_factor = Decimal(str(penalty_factor))

    # 计算出相似度
    if norm_sight1 == 0 or norm_sight2 == 0:
        return Decimal(0)
    else:
        # 应用惩罚因子
        return dot_product / (norm_sight1 * norm_sight2 * penalty_factor)

def recommend_sights(target_username, k=10):
    """为目标用户推荐景点"""
    # 获取目标用户的评分数据
    target_user_ratings = get_user_ratings(target_username)

    # 获取所有其他用户的评分数据，并计算与目标用户的相似度
    all_users = UserInfo.objects.exclude(username=target_username)
    user_similarities = {}
    for user in all_users:
        user_ratings = get_user_ratings(user.username)
        similarity = calculate_adjusted_cosine_similarity(target_user_ratings, user_ratings)
        if similarity > 0:  # 考虑相似度大于0的用户
            user_similarities[user.username] = similarity

    # 按相似度降序排序，并选择前k个相似用户
    top_k_users = sorted(user_similarities, key=user_similarities.get, reverse=True)[:k]

    # 获取这些用户评价过的景点，并计算推荐分数
    recommended_sights_dict = {}
    similarity_sum = {}
    for user in top_k_users:
        user_ratings = get_user_ratings(user)
        similarity = user_similarities[user]
        normalized_similarity = Decimal(str(similarity))
        # 遍历用户评价过的景点
        for sight_id, score in user_ratings.items():
            # 如果目标用户未评价过该景点
            if sight_id not in target_user_ratings:
                # 初始化该景点的推荐分数和相似度总和
                if sight_id not in recommended_sights_dict:
                    recommended_sights_dict[sight_id] = Decimal(0)
                    similarity_sum[sight_id] = Decimal(0)
                # 根据相似度和评分计算推荐分数
                recommended_sights_dict[sight_id] += score * normalized_similarity
                # 更新相似度总和
                similarity_sum[sight_id] += normalized_similarity

    # 如果推荐的景点数量少于k个，则补充热门景点
    recommended_sights_list = sorted(recommended_sights_dict, key=recommended_sights_dict.get, reverse=True)
    while len(recommended_sights_list) < k:
        hot_sights = AdsSightHeatScoreTop10Stats.objects.exclude(
            sight_id__in=recommended_sights_list).order_by('-heat_score')[:k - len(recommended_sights_list)]
        for hot_sight in hot_sights:
            recommended_sights_list.append(hot_sight.sight_id)
            recommended_sights_dict[hot_sight.sight_id] = hot_sight.heat_score
            if len(recommended_sights_list) == k:
                break  # 当补充到k个景点时退出循环

    # 根据景点ID查询出推荐的景点，格式为QuerySet
    recommended_sights_queryset = SightInfo.objects.filter(sight_id__in=recommended_sights_list)
    return recommended_sights_queryset

if __name__ == '__main__':
    recommended_sights_for_user = recommend_sights('allen')
    for sight in recommended_sights_for_user:
        print(sight.sight_id, sight.sight_name)
