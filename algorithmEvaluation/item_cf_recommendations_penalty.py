
import math
import django
import os

from collections import defaultdict
from django.db.models import Count

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'hive-tourism-recommendation.settings')
django.setup()
from app.models import CommentInfoTest, AdsSightHeatScoreTop10Stats, UserFavoritesTest, UserBrowsesTest, \
    UserRecommendationValuesWithPenaltyTest

"""
相似度计算方法：
评分数据相似度、收藏与浏览数据相似度：使用余弦相似度
加权相似度：
综合考虑评分、收藏、浏览数据的相似度，分别赋予0.5、0.3、0.2的权重，通过加权求和得到综合相似度。
"""
def get_sight_frequencies():
    sight_frequencies = {}
    sights_with_comments = CommentInfoTest.objects.values('sight_id').annotate(Count('sight_id'))
    for sight_with_comments in sights_with_comments:
        sight_id = sight_with_comments['sight_id']
        comment_count = sight_with_comments['sight_id__count']
        sight_frequencies[sight_id] = comment_count
    return sight_frequencies

SIGHT_FREQUENCIES = get_sight_frequencies()  # 缓存景点评论频次字典

# 构建全局的景点-用户交互矩阵
user_item_interaction_matrix = defaultdict(dict)
ITEM_SIMILARITY = None

def build_user_item_interaction_matrix():
    # 构建用户评分矩阵
    for comment in CommentInfoTest.objects.all():
        if comment.score < 3:
            continue
        user_id = comment.user_id
        sight_id = comment.sight_id
        score = comment.score
        # 确保用户与景点的交互字典存在
        user_item_interaction_matrix[sight_id][user_id] = {
            'rating': score,
            'favorite': 0,
            'browse': 0
        }

    # 构建用户收藏矩阵
    for favorite in UserFavoritesTest.objects.all():
        user_id = favorite.user_id
        sight_id = favorite.sight_id
        if user_id not in user_item_interaction_matrix[sight_id]:
            user_item_interaction_matrix[sight_id][user_id] = {
                'rating': 0,
                'favorite': 0,
                'browse': 0
            }
            # 更新收藏状态
        user_item_interaction_matrix[sight_id][user_id]['favorite'] = 1

        # 构建用户浏览矩阵
    for browse in UserBrowsesTest.objects.all():
        user_id = browse.user_id
        sight_id = browse.sight_id
        # 如果用户与景点的交互字典不存在，则添加基础结构
        if user_id not in user_item_interaction_matrix[sight_id]:
            user_item_interaction_matrix[sight_id][user_id] = {
                'rating': 0,
                'favorite': 0,
                'browse': 0
            }
            # 更新浏览状态
        user_item_interaction_matrix[sight_id][user_id]['browse'] = 1

    # 构建用户评分矩阵
    for comment in CommentInfoTest.objects.all():
        if comment.score < 3:
            continue
        user_id = comment.user_id
        sight_id = comment.sight_id
        score = comment.score
        # 确保用户与景点的交互字典存在
        user_item_interaction_matrix[sight_id][user_id] = {
            'rating': score,
            'favorite': 0,
            'browse': 0
        }
        # 构建用户收藏矩阵
    for favorite in UserFavoritesTest.objects.all():
        if favorite.user_id not in user_item_interaction_matrix[favorite.sight_id]:
            user_item_interaction_matrix[favorite.sight_id][favorite.user_id] = {
                'rating': 0,
                'favorite': 0,
                'browse': 1
            }
        else:
            user_item_interaction_matrix[favorite.sight_id][favorite.user_id]['favorite'] = 0
        # 构建用户浏览矩阵
    for browse in UserBrowsesTest.objects.all():
        if browse.user_id not in user_item_interaction_matrix[browse.sight_id]:
            user_item_interaction_matrix[browse.sight_id][browse.user_id] = {
                'rating': 0,
                'favorite': 0,
                'browse': 1
            }
        else:
            user_item_interaction_matrix[browse.sight_id][browse.user_id]['browse'] = 1

def calculate_similarity():
    ITEM_SIMILARITY = defaultdict(dict)
    for item1, users_dict1 in user_item_interaction_matrix.items():
        for item2, users_dict2 in user_item_interaction_matrix.items():
            if item1 != item2:
                dot_product = 0
                norm1 = 0
                norm2 = 0
                user_ids_set2 = set(users_dict2.keys())
                for user_id, interaction1 in users_dict1.items():
                    if user_id in user_ids_set2:
                        interaction2 = users_dict2[user_id]
                        rating1, rating2 = interaction1['rating'], interaction2['rating']
                        favorite1, favorite2 = interaction1['favorite'], interaction2['favorite']
                        browse1, browse2 = interaction1['browse'], interaction2['browse']

                        # 计算点积
                        dot_product += (0.5 * rating1 * rating2 +
                                        0.3 * int(favorite1) * int(favorite2) +
                                        0.2 * int(browse1) * int(browse2))
                        # 计算模长
                        norm1 += (0.5 * rating1 ** 2 +
                                  0.3 * int(favorite1) ** 2 +
                                  0.2 * int(browse1) ** 2)

                        norm2 += (0.5 * rating2 ** 2 +
                                  0.3 * int(favorite2) ** 2 +
                                  0.2 * int(browse2) ** 2)


                if norm1 and norm2:
                    similarity = dot_product / (norm1 * norm2)
                    # 融入热门景点惩罚因子
                    sight_freq1 = SIGHT_FREQUENCIES.get(item1, 1)
                    sight_freq2 = SIGHT_FREQUENCIES.get(item2, 1)
                    # 计算最终相似度
                    ITEM_SIMILARITY[item1][item2] = round(similarity / (math.log(1 + sight_freq1) * math.log(1 + sight_freq2)), 4)

    return ITEM_SIMILARITY

def recommend_sights(user_id, k=20):
    build_user_item_interaction_matrix()
    ITEM_SIMILARITY = calculate_similarity()
    # 初始化用户评分字典
    rated_items = {}
    # 遍历所有景点，检查用户是否对它们有评分
    for sight_id, user_dict in user_item_interaction_matrix.items():
        if user_id in user_dict and user_dict[user_id]['rating'] > 0:
            rated_items[sight_id] = user_dict[user_id]['rating']

    recommendations = defaultdict(float)
    # 计算推荐度：相似度乘以用户对已评分景点的评分
    for rated_item, rating in rated_items.items():
        if rating < 3:
            continue
        for similar_item, similarity in ITEM_SIMILARITY[rated_item].items():
            if similarity > 0 and similar_item not in rated_items:
                recommendations[similar_item] += similarity * rating

    print(recommendations)

    # 补充热门景点，直到达到k个景点
    # extra_sights_needed = k - len(recommendations)
    # if extra_sights_needed > 0:
    #     extra_sights = AdsSightHeatScoreTop10Stats.objects.order_by('-heat_score')[:extra_sights_needed]
    #     for sight in extra_sights:
    #         if sight.sight_id not in recommendations.keys():
    #             recommendations[sight.sight_id] = -1  #热门景点的推荐度设为-1
    #             extra_sights_needed -= 1
    #             if extra_sights_needed == 0:
    #                 break

    # 将景点推荐度保存到UserRecommendationSightValues中
    for similar_item, recommendation_value in recommendations.items():
        # 删除旧的推荐度
        UserRecommendationValuesWithPenaltyTest.objects.filter(
            user_id=user_id,
            sight_id=similar_item
        ).delete()

        # 插入新的推荐度
        UserRecommendationValuesWithPenaltyTest.objects.create(
            user_id=user_id,
            sight_id=similar_item,
            recommendation_value=recommendation_value
        )
