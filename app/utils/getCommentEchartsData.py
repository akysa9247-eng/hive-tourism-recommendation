from app.models import AdsCommentSightScoreRate
from app.utils.getSightEchartsData import queryset_filter


def get_comment_score_rate(province=None, city=None):
    """"计算用户评论各分值占比"""

    # 筛选指定省份和城市的数据
    queryset = AdsCommentSightScoreRate.objects.all()
    queryset = queryset_filter(queryset, province, city)

    result_data = []

    # 遍历查询集，记录每个分数段的数量
    sight_count = 0
    comment_score_count_5 = 0
    comment_score_count_4 = 0
    comment_score_count_3 = 0
    comment_score_count_2 = 0
    comment_score_count_1 = 0
    for record in queryset:
        record_sight_count = record.score_count
        if record_sight_count == 0:
           continue
        else:
            # 计算每个分数段的数量
            sight_count += record_sight_count
            comment_score_count_5 += record.comment_score_count_5
            comment_score_count_4 += record.comment_score_count_4
            comment_score_count_3 += record.comment_score_count_3
            comment_score_count_2 += record.comment_score_count_2
            comment_score_count_1 += record.comment_score_count_1

    if sight_count == 0:
        return {}

    result_data.append({
        'name': '5分占比',
        'value': round(comment_score_count_5 / sight_count * 100, 2)
    })
    result_data.append({
        'name': '4分占比',
        'value': round(comment_score_count_4 / sight_count * 100, 2)
    })
    result_data.append({
        'name': '3分占比',
        'value': round(comment_score_count_3 / sight_count * 100, 2)
    })
    result_data.append({
        'name': '2分占比',
        'value': round(comment_score_count_2 / sight_count * 100, 2)
    })
    result_data.append({
        'name': '1分占比',
        'value': round(comment_score_count_1 / sight_count * 100, 2)
    })

    return result_data

