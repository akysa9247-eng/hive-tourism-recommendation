from app.models import CommentInfo

def addComments(comment_data):
    """添加用户评论"""
    sight_id = comment_data['sight_id']
    user_id = comment_data['user_id']
    score = comment_data['score']
    content = comment_data['content']
    comment_datetime = comment_data['comment_datetime']

    # 删除旧的评论
    try:
        existing_comment = CommentInfo.objects.get(user_id=user_id, sight_id=sight_id)
        existing_comment.delete()
    except CommentInfo.DoesNotExist:
        pass

    # 保存新的评论
    comment = CommentInfo(user_id=user_id, sight_id=sight_id, content=content, score=score, date=comment_datetime)
    comment.save()
