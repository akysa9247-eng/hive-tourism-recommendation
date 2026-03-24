from app.models import UserSearchRecords, UserFavorites, UserBrowses, SightInfo, UserInfo
from app.utils import getTime

def save_user_search_records(id, search_value):
    if search_value:
        UserSearchRecords.objects.create(user_id=id, search_value=search_value, search_time=getTime.get_datetime())

def save_user_favorite_records(id, sight_id):
    return UserFavorites.objects.create(user_id=id, sight_id=sight_id, favorited_time=getTime.get_datetime())

def save_user_browse_records(id, sight_id):
    return UserBrowses.objects.create(user_id=id, sight_id=sight_id, browse_time=getTime.get_datetime())

def cancel_user_favorite_records(user_id, sight_id):
    return UserFavorites.objects.get(user_id=user_id, sight_id=sight_id).delete()

def get_user_favorite_records(user_id):
    query_set = UserFavorites.objects.filter(user_id=user_id).order_by('-favorited_time')

    # 创建一个空列表来存储景点和评论信息
    user_favorite_records = []

    # 遍历每条评论
    for favorite in query_set:
        # 根据景点id查询出景点信息
        sight = SightInfo.objects.get(sight_id=favorite.sight_id)
        user = UserInfo.objects.get(id=favorite.user_id)
        # 将评论信息和景点信息组合成一个字典
        user_favorite_records.append({
            'favorite': favorite,
            'sight': sight
        })

    return user_favorite_records


def getAllUserFavoriteInfoData():
    query_set = UserFavorites.objects.all().order_by('-favorited_time')

    # 创建一个空列表
    favorites_data = []
    if not query_set:
        return favorites_data

    for favorite in query_set:
        # 根据景点id查询出景点信息
        sight = SightInfo.objects.get(sight_id=favorite.sight_id)
        user = UserInfo.objects.get(id=favorite.user_id)

        favorites_data.append({
            'favorite': favorite,
            'sight': sight,
            'user': user
        })
    return favorites_data

def getUserFavoriteDataByUsername(search_value):
    """ 根据用户名获取用户的收藏信息 """

    users = UserInfo.objects.filter(username__icontains=search_value)

    # 创建一个空列表
    favorites_data = []
    if not users:
        return favorites_data

    for user in users:
        favorites = UserFavorites.objects.filter(user_id=user.id).order_by('-favorited_time')
        for favorite in favorites:
            sight = SightInfo.objects.get(sight_id=favorite.sight_id)
            favorites_data.append({
                'favorite': favorite,
                'sight': sight,
                'user': user
            })

    return favorites_data

def getAllUserSearchRecords():
    query_set = UserSearchRecords.objects.all().order_by('-search_time')

    # 创建一个空列表
    search_records = []
    if not query_set:
        return search_records

    for search_record in query_set:
        # 根据景点id查询出景点信息
        user = UserInfo.objects.get(id=search_record.user_id)

        search_records.append({
            'search_record': search_record,
            'user': user
        })
    return search_records

def getUserSearchRecordsByUsername(search_value):
    """ 根据用户名获取用户的搜索信息 """

    users = UserInfo.objects.filter(username__icontains=search_value)

    # 创建一个空列表
    search_records = []
    if not users:
        return search_records

    for user in users:
        query_set = UserSearchRecords.objects.filter(user_id=user.id).order_by('-search_time')
        for search_record in query_set:
            search_records.append({
                'search_record': search_record,
                'user': user
            })

    return search_records

def getAllUserBrowseInfoData():
    query_set = UserBrowses.objects.all().order_by('-browse_time')

    # 创建一个空列表
    browses_data = []
    if not query_set:
        return browses_data

    for browse in query_set:
        # 根据景点id查询出景点信息
        sight = SightInfo.objects.get(sight_id=browse.sight_id)
        user = UserInfo.objects.get(id=browse.user_id)

        browses_data.append({
            'browse': browse,
            'sight': sight,
            'user': user
        })
    return browses_data

def getUserBrowsesByUsername(search_value):
    """ 根据用户名获取用户的搜索信息 """

    users = UserInfo.objects.filter(username__icontains=search_value)

    # 创建一个空列表
    browses_data = []
    if not users:
        return browses_data

    for user in users:
        query_set = UserBrowses.objects.filter(user_id=user.id).order_by('-browse_time')
        for browse in query_set:
            sight = SightInfo.objects.get(sight_id=browse.sight_id)
            browses_data.append({
                'browse': browse,
                'sight': sight,
                'user': user
            })

    return browses_data