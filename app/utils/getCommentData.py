from app.models import CommentInfo, SightInfo, UserInfo

def getAllCommentData():
    # 从CommentInfo模型中获取指定用户的评论信息，并按日期降序
    comments = CommentInfo.objects.all().order_by('-date')

    # 创建一个空列表来存储景点和评论信息
    comments_data = []
    if not comments:
        return comments_data

    # 遍历每条评论
    for comment in comments:
        # 根据景点id查询出景点信息
        sight = SightInfo.objects.get(sight_id=comment.sight_id)
        user = UserInfo.objects.get(id=comment.user_id)

        # 将评论信息、用户信息和景点信息组合成一个字典
        comments_data.append({
            'comment': comment,
            'sight': sight,
            'user': user
        })

    return comments_data

def getUserCommentData(user_id):
    """ 获取指定id的用户评论信息 """

    # 从CommentInfo模型中获取指定用户的评论信息，并按日期降序
    comments = CommentInfo.objects.filter(user_id=user_id).order_by('-date')

    # 创建一个空列表来存储景点和评论信息
    user_comment_data = []
    if not comments:
        return user_comment_data

    # 遍历每条评论
    for comment in comments:
        # 根据景点id查询出景点信息
        sight = SightInfo.objects.get(sight_id=comment.sight_id)

        # 将评论信息和景点信息组合成一个字典
        user_comment_data.append({
            'comment': comment,
            'sight': sight
        })

    return user_comment_data

def getCommentsContainingSearchUsername(search_value):
    """ 获取指定用户名的用户评论信息 """

    user_ids = UserInfo.objects.filter(username__icontains=search_value).values_list('id', flat=True)
    # 从CommentInfo模型中获取指定用户的评论信息，并按日期降序
    comments = CommentInfo.objects.filter(user_id__in=user_ids).order_by('-date')

    # 创建一个空列表来存储景点和评论信息
    comments_data = []
    if not comments:
        return comments_data

    # 遍历每条评论
    for comment in comments:
        # 根据景点id查询出景点信息
        sight = SightInfo.objects.get(sight_id=comment.sight_id)

        # 将评论信息和景点信息组合成一个字典
        comments_data.append({
            'comment': comment,
            'sight': sight
        })

    return comments_data

def getSightCommentData(sight_id):
    """ 获取景点的评论信息 """

    # 从CommentInfo模型中获取指定景点的评论信息，并按日期降序
    comments = CommentInfo.objects.filter(sight_id=sight_id).order_by('-date')

    # 创建一个空列表来存储用户和评论信息
    sight_comment_data = []
    if not comments:
        return sight_comment_data
    # 遍历每条评论
    for comment in comments:
        # 根据景点id查询出景点信息
        user = UserInfo.objects.get(id=comment.user_id)

        # 将评论信息和景点信息组合成一个字典
        sight_comment_data.append({
            'comment': comment,
            'user': user
        })

    for item in sight_comment_data:
        print(item['user'].username)
    return sight_comment_data