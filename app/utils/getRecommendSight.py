#encoding=utf-8

import ast
import json

from app.models import AdsSightHeatScoreTop10Stats, SightInfo, UserRecommendationValues
from recommendation import item_cf_recommendations
from django.db.models import Q

def queryset_filter(queryset, province, city):
    """ 根据省份、城市进行过滤 """
    if len(province) != 0:
        queryset = queryset.filter(province=province)
    if len(city) != 0:
        queryset = queryset.filter(city=city)

    return queryset

def sight_to_list(sights):
    sight_list = []
    for sight in sights:
        sight_dict = {
            'sight_id': sight.sight_id,
            'sight_name': sight.sight_name,
            'province': sight.province,
            'city': sight.city,
            'tag_list': sight.tag_list,
            'level': sight.level,
            'heat_score': sight.heat_score,
            'score': sight.score,
            'address': sight.address,
            'telephone': sight.telephone,
            'intro': sight.intro,
            'opening_time': sight.opening_time,
            'img_list': sight.img_list,
            'cover': sight.cover
        }
        sight_list.append(sight_dict)
    return sight_list

def get_personalized_recommendations(user_id, k=10):
    item_cf_recommendations.recommend_sights(user_id, k)
    recommend_sights = UserRecommendationValues.objects.filter(user_id=user_id).\
        order_by('-recommendation_value').values_list('sight_id', flat=True)


    sight_ids = list(recommend_sights)[:10]
    recommended_sights_info = SightInfo.objects.filter(sight_id__in=sight_ids)

    sight_list = sight_to_list(recommended_sights_info)
    return sight_list

def get_recommend_popular_sight(province=None, city=None):
    """ 根据省份或城市获取热度和评分前十的景点 """
    queryset = AdsSightHeatScoreTop10Stats.objects.all()
    queryset = queryset_filter(queryset, province, city)
    # 根据热度和评分降序排序，取前十个景点
    recommend_popular_sight = queryset.order_by('-heat_score','-score')[:10]

    sight_list = sight_to_list(recommend_popular_sight)
    return sight_list

def get_recommend_level_sight(province=None, city=None):
    """ 根据省份或城市获取A级景点中评分前十的景点 """
    queryset = SightInfo.objects.all()
    # 根据省份和城市进行过滤
    filtered_queryset = queryset_filter(queryset, province, city)
    # 筛选出level为5A或4A的景点，并根据score降序排序，取前十个
    recommend_level_sight = filtered_queryset.filter(Q(level='5A') | Q(level='4A')).order_by('-score')[:10]

    sight_list = sight_to_list(recommend_level_sight)
    return sight_list

def get_recommend_similar_sights(sight_info):

    if len(sight_info.tag_list) == 0:
        return None
    # 将目标景点的标签列表转换并过滤
    tag_list = ast.literal_eval(sight_info.tag_list)
    tag_list_filter = [tag.strip() for tag in tag_list if tag.strip()]  # 去除空白并过滤空标签

    # 构建查询条件
    query_conditions = Q()

    # 根据目标景点的标签，查询包含改标签的景点
    for tag in tag_list_filter:
        query_conditions |= Q(tag_list__icontains=tag)

    # 应用查询条件，然后排除选中的景点，按热度降序排序，选取选取前十个景点
    similar_sights = SightInfo.objects.filter(query_conditions) \
                         .exclude(sight_id=sight_info.sight_id) \
                         .order_by('-heat_score')[:10]

    for sight in similar_sights:
        sight.img_list = json.loads(sight.img_list)
    # 返回查询到的相似景点
    return similar_sights




