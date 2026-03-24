from app.models import AdsCityStats, AdsSightScoreRate, AdsSightHeatScoreRate, AdsSightScoreTop10Stats,  \
    AdsSightHeatScoreTop10Stats
from django.db.models import Sum, F

def queryset_filter(queryset, province, city):
    """ 根据省份、城市进行过滤 """
    if len(province) != 0:
        queryset = queryset.filter(province=province)
    if len(city) != 0:
        queryset = queryset.filter(city=city)

    return queryset

def get_city_heat_score_list():
    """ 获取城市热度排行"""
    # 获取所有城市名称和热度，按热度降序排序
    cities_with_heat_dict = AdsCityStats.objects.annotate().order_by('-heat_score').values('city', 'heat_score')

    # 将数据转换为字典列表
    cities_with_heat_dict_list = list(cities_with_heat_dict)
    cities_heat_dict = {item['city']: item['heat_score'] for item in cities_with_heat_dict_list}

    # 返回结果
    return list(cities_heat_dict.keys()), list(cities_heat_dict.values())

# 根据省份或城市计算景点等级占比
def get_sight_level_rate(province=None, city=None):
    """ # 根据省份或城市计算景点等级占比 """
    queryset = AdsCityStats.objects.values(
        'province',
        'city'
    )

    queryset = queryset_filter(queryset, province, city)

    queryset = queryset.annotate(
        sight_count=Sum('sight_count'),
        five_a_count=Sum('sight_count_5a'),
        four_a_count=Sum('sight_count_4a'),
        other_sight_count=F('sight_count') - F('five_a_count') - F('four_a_count')
    )

    result_data = []
    sight_count = 0
    five_a_count = 0
    four_a_count = 0
    other_sight_count = 0

    for field in queryset:
        sight_count += field['sight_count']
        five_a_count += field['five_a_count']
        four_a_count += field['four_a_count']
        other_sight_count += field['other_sight_count']

    if sight_count == 0:
        return {}

    result_data.append({
        'name': '5A级',
        'value': round(five_a_count / sight_count * 100, 2)
    })

    result_data.append({
        'name': '4A级',
        'value': round(four_a_count / sight_count * 100, 2)
    })

    result_data.append({
        'name': '其他',
        'value': round(other_sight_count / sight_count * 100, 2)
    })

    return result_data


def get_sight_score_rate(province=None, city=None):
    """ 根据省份或城市计算景点等级占比"""

    # 筛选指定省份和城市的数据
    queryset = AdsSightScoreRate.objects.all()
    queryset = queryset_filter(queryset, province, city)

    result_data = []
    # 遍历查询集，计算各分数段的数量
    sight_count = 0
    score_count_4_5_to_5 = 0
    score_count_4_to_4_5 = 0
    score_count_3_5_to_4 = 0
    score_count_3_to_3_5 = 0
    score_count_0_to_3 = 0
    for record in queryset:
        record_sight_count = record.sight_count
        if record_sight_count == 0:
           continue
        else:
            # 计算各分数段的数量
            sight_count += record_sight_count
            score_count_4_5_to_5 += record.score_count_4_5_to_5
            score_count_4_to_4_5 += record.score_count_4_to_4_5
            score_count_3_5_to_4 += record.score_count_3_5_to_4
            score_count_3_to_3_5 += record.score_count_3_to_3_5
            score_count_0_to_3 += record.score_count_0_to_3

    if sight_count == 0:
        return {}

    result_data.append({
        'name': '4.5-5分景点占比',
        'value': round(score_count_4_5_to_5 / sight_count * 100, 2)
    })
    result_data.append({
        'name': '4-4.5分景点占比',
        'value': round(score_count_4_to_4_5 / sight_count * 100, 2)
    })
    result_data.append({
        'name': '3.5-4分景点占比',
        'value': round(score_count_3_5_to_4 / sight_count * 100, 2)
    })
    result_data.append({
        'name': '3.5-3分景点占比',
        'value': round(score_count_3_to_3_5 / sight_count * 100, 2)
    })
    result_data.append({
        'name': '0-3分景点占比',
        'value': round(score_count_0_to_3 / sight_count * 100, 2)
    })
    return result_data

def get_sight_heat_score_rate(province=None, city=None):
    """ 根据省份或城市计算景点热度占比 """
    # 筛选指定省份和城市的数据
    queryset = AdsSightHeatScoreRate.objects.all()
    queryset = queryset_filter(queryset, province, city)

    result_data = []

    # 遍历查询集，计算各分数段的数量
    sight_count = 0
    heat_score_9_to_10 = 0
    heat_score_8_to_9 = 0
    heat_score_7_to_8 = 0
    heat_score_6_to_7 = 0
    heat_score_0_to_6 = 0
    for record in queryset:
        record_sight_count = record.sight_count
        if record_sight_count == 0:
           continue
        else:
            # 计算各分数段的数量
            sight_count += record_sight_count
            heat_score_9_to_10 += record.heat_score_9_to_10
            heat_score_8_to_9 += record.heat_score_8_to_9
            heat_score_7_to_8 += record.heat_score_7_to_8
            heat_score_6_to_7 += record.heat_score_6_to_7
            heat_score_0_to_6 += record.heat_score_0_to_6

    if sight_count == 0:
        return {}

    result_data.append({
        'name': '9-10热度景点占比',
        'value': round(heat_score_9_to_10 / sight_count * 100, 2)
    })
    result_data.append({
        'name': '8-9热度景点占比',
        'value': round(heat_score_8_to_9 / sight_count * 100, 2)
    })
    result_data.append({
        'name': '7-8热度景点占比',
        'value': round(heat_score_7_to_8 / sight_count * 100, 2)
    })
    result_data.append({
        'name': '6-7热度景点占比',
        'value': round(heat_score_6_to_7 / sight_count * 100, 2)
    })
    result_data.append({
        'name': '0-6热度景点占比',
        'value': round(heat_score_0_to_6 / sight_count * 100, 2)
    })

    return result_data

def get_sight_score_top_10(province=None, city=None):
    """ 根据省份或城市获取评分前十的景点 """
    queryset = AdsSightScoreTop10Stats.objects.all()
    queryset = queryset_filter(queryset, province, city)
    sight_score_top_10 = queryset.order_by('-score', '-heat_score')[:10]

    return sight_score_top_10

