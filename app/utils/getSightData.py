import json
import time

from app.models import UserInfo, SightInfo, CommentInfo

def getAllSightInfoData():
    """返回所有景点数据"""
    return SightInfo.objects.all()

def getOneSightInfoData(sight_id):
    """返回指定景点id的景点数据"""
    return SightInfo.objects.get(sight_id=sight_id)

def get_sight_comment_count(sight_id):
    return CommentInfo.objects.filter(sight_id=sight_id).count()

def getSightCommentsCount(sight_id):
    """返回指定景点的评论数量"""
    count = CommentInfo.objects.filter(sight_id=sight_id).count()
    return count
