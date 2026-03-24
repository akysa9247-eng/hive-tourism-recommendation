
from app.models import UserInfo, SightInfo, CommentInfo, UserFavorites


def getAllUserInfoData():
    """返回所有用户数据"""
    return UserInfo.objects.all().order_by('-last_login_time')

def getOneUserInfoData(username):
    """返回指定用户名的用户数据"""
    return UserInfo.objects.get(username=username)



