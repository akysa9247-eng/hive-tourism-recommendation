from app.models import \
    AdsSightCountStats, \
    AdsCityStats, \
    AdsProvinceStats, \
    AdsSightScoreTop10Stats, \
    AdsSightHeatScoreTop10Stats,\
    SightInfo, CommentInfo

from django.db.models import Max, Count


def get_5A_counts():
    """获取5A级景点个数"""
    # 获取最新日期
    latest_date = AdsSightCountStats.objects.aggregate(latest_dt=Max('dt'))['latest_dt']

    # 使用最新日期查询
    try:
        latest_stats = AdsSightCountStats.objects.get(dt=latest_date)
        total_sight_count_5a = latest_stats.total_sight_count_5a
    except AdsSightCountStats.DoesNotExist:
        total_sight_count_5a = None

    return total_sight_count_5a


def get_most_commented_sight():
    """ 获取评论最多的景点 """
    # 按照sight_id进行分组和计数
    comments_count = CommentInfo.objects.values('sight_id').annotate(count=Count('id')).order_by('-count')

    # 获取评论次数最多的sight_id
    most_commented_sight_id = comments_count.first()['sight_id'] if comments_count.exists() else None
    most_commented_sight = SightInfo.objects.filter(sight_id=most_commented_sight_id).first()

    if most_commented_sight:
        return most_commented_sight
    else:
        return None


def get_most_heat_score_city():
    """ 获取热度最高的城市 """
    # 按照heat_score字段降序排序，获取热度最高的城市
    most_heat_score_city = AdsCityStats.objects.order_by('-heat_score').first()

    if most_heat_score_city:
        return most_heat_score_city
    else:
        return None

def get_sight_score_top_10():
    """ 获取评分前十的景点 """
    # 获取每个省份的最高评分
    province_max_scores = AdsSightScoreTop10Stats.objects.values('province').annotate(
        max_score=Max('score')
    )

    # 创建字典保存每个省份的最高评分
    province_max_score_dict = {
        item['province']: item['max_score'] for item in province_max_scores
    }

    # 查询每个省份评分最高和评论数最多的景点
    top_sights_per_province = []
    for province, max_score in province_max_score_dict.items():
        # 查询评分最高的景点，并按照热度降序排序
        sights = AdsSightScoreTop10Stats.objects.filter(
            province=province, score=max_score
        ).order_by('-heat_score')

        # 选择每个省份评分最高且评论数最多的景点
        top_sight = sights.first()
        if top_sight:
            top_sights_per_province.append(top_sight)

    # 按照评分、评论数降序排序，获取前十个对象
    top_10_sights = sorted(top_sights_per_province, key=lambda x: (-x.score, -x.heat_score))[:10]

    return top_10_sights

def get_sight_heat_score_top_10():
    """ 获取景区热度前十的景点 """
    # 获取每个省份的热度最高的值
    province_max_heat_scores = AdsSightHeatScoreTop10Stats.objects.values('province').annotate(
        max_heat_score=Max('heat_score')
    )

    # 创建字典保存每个省份的最高热度
    province_max_heat_score_dict = {
        item['province']: item['max_heat_score'] for item in province_max_heat_scores
    }

    # 查询每个省份热度最大和评分最高的景点
    top_sights_per_province = []
    for province, max_heat_score in province_max_heat_score_dict.items():
        # 查询每个省份最大热度的景点，并按照评分降序排序
        sights = AdsSightHeatScoreTop10Stats.objects.filter(
            province=province, heat_score=max_heat_score
        ).order_by('-score')

        # 选择每个省份热度最高且评分最高的景点
        top_sight = sights.first()
        if top_sight:
            top_sights_per_province.append(top_sight)

    # 按照热度、评分降序排序，获取前十个对象
    top_10_heat_scores_sight = sorted(top_sights_per_province, key=lambda x: (-x.heat_score, -x.score))[:10]

    return list(top_10_heat_scores_sight)

def get_geo_data():
    """获取省份热度"""
    result_data = []
    province_data_list = AdsProvinceStats.objects.all()

    for province_data in province_data_list:
        result_data.append({
            'name':province_data.province,
            'value':province_data.heat_score
        })

    return result_data
