import json
import os

from django.core.files.storage import FileSystemStorage
from django.http import JsonResponse
from django.shortcuts import render, redirect
from django.db.models import Max

from app.models import AdminInfo, SightInfo, CommentInfo, UserInfo, ProvinceCity, UserSearchRecords, UserFavorites, \
    UserBrowses

from app.utils import getHomeData, getSightData, updateUserData, getAddCommentsData, getTime, getSightEchartsData, \
    getCommentEchartsData, getCommentData, getRecommendSight, getUserBehaviorData, getUserData, updateAdminData
from app.utils.pagination import Pagination
import bcrypt

from util.filter import truncate_chinese
from project import settings


def register(request):
    """ 用户注册 """
    # POST请求处理登录信息
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        confirm_password = request.POST.get('confirm_password')

        # 验证用户名是否已存在
        if UserInfo.objects.filter(username=username).exists():
            return JsonResponse({'error': '用户名已存在'})

        # 验证密码和确认密码是否一致
        if password != confirm_password:
            return JsonResponse({'error': '两次输入的密码不一致'})

        # 使用bcrypt哈希密码
        hashed_password = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt()).decode('utf-8')

        # 创建新用户并保存
        user = UserInfo(username=username, password=hashed_password,sex='',address='',create_time=getTime.get_datetime())
        user.save()

        return JsonResponse({'success': '注册成功'})

    # GET请求则返回注册页面
    return render(request, 'register.html')

def to_login(request):
    return render(request, 'login.html')

def login(request):
    """ 用户登录 """
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        try:
            # 尝试获取用户信息
            user = UserInfo.objects.get(username=username)
            if bcrypt.checkpw(password.encode('utf-8'), user.password.encode('utf-8')):
                request.session['username'] = username
                user.last_login_time = getTime.get_datetime()
                user.save()
                return redirect('/app/home')
            else:
                return JsonResponse({'error': '密码输入错误'})
        except UserInfo.DoesNotExist:
            # 用户未注册
            return JsonResponse({'error': '用户未注册'})

    return render(request, 'login.html')

def logout(request):
    """ 退出登录 """
    request.session.clear()  # 删除当前会话中的所有数据
    return redirect('/app/login')

def update_user_Info(request):
    """ 修改个人信息 """
    username = request.session.get('username')
    userInfo = UserInfo.objects.get(username=username)
    if request.method == 'POST':
        updateUserData.update_user_info(username, request.POST, request.FILES)
        userInfo = UserInfo.objects.get(username=username)
    return render(request, 'updateUserInfo.html', {
        'userInfo': userInfo
    })

def update_password(request):
    """ 修改密码 """
    username = request.session.get('username')
    user = UserInfo.objects.get(username=username)
    if request.method == 'POST':
        return updateUserData.update_user_password(username, request.POST)

    return render(request, 'updatePassword.html', {
        'userInfo': user
    })

def user_comment_info(request):
    """ 我的评价 """
    username = request.session.get('username')
    userInfo = UserInfo.objects.get(username=username)

    comment_data = getCommentData.getUserCommentData(userInfo.id)
    page_object = Pagination(request, comment_data)

    context = {
        "query_set": page_object.page_queryset,
        "page_string": page_object.html()
    }

    return render(request, 'userCommentInfo.html', {
        'userInfo': userInfo,
        'context': context
    })

def delete_comment(request, id):
    """ 删除评论 """
    comment = CommentInfo.objects.get(id=id)
    if comment:
        comment.delete()
    return redirect('/app/userCommentInfo')

def home(request):
    """ 首页 """
    username = request.session.get('username')
    userInfo = UserInfo.objects.get(username=username)

    year, mon, day = getTime.get_date_separate()
    total_sight_count_5a = getHomeData.get_5A_counts()
    most_comments_sight = getHomeData.get_most_commented_sight()

    most_heat_score_city = getHomeData.get_most_heat_score_city()
    top_10_score_sight = getHomeData.get_sight_score_top_10()
    top_10_heat_scores_sight = getHomeData.get_sight_heat_score_top_10()
    geo_data = getHomeData.get_geo_data()
    return render(request, 'home.html',{
        'userInfo':userInfo,
        'total_sight_count_5a':total_sight_count_5a,
        'most_comments_sight':most_comments_sight,
        'most_heat_score_city':most_heat_score_city,
        'top_10_score_sight':top_10_score_sight,
        'top_10_heat_scores_sight':top_10_heat_scores_sight,
        'now_time':{
            'year': year,
            'mon': mon,
            'day': day
        },
        'geo_data':geo_data,
        'search_value':''
    })

def sight_data_list(request):
    """ 景点列表 """
    username = request.session.get('username')
    userInfo = UserInfo.objects.get(username=username)

    query_set = getSightData.getAllSightInfoData()

    page_object = Pagination(request, query_set)

    context = {
        "query_set" : page_object.page_queryset,
        "page_string" : page_object.html()
    }

    return render(request, 'sightDataList.html', {
        'userInfo': userInfo,
        'context': context
    })

def search_sight(request, search_value=None):
    """ 搜索景点 """
    username = request.session.get('username')
    userInfo = UserInfo.objects.get(username=username)

    if search_value:
        query_set = SightInfo.objects.filter(sight_name__icontains=search_value).order_by('-sight_id')
        getUserBehaviorData.save_user_search_records(userInfo.id, search_value) #记录用户搜索信息
    else:
        # 如果没有搜索值，返回一个空查询集
        query_set = SightInfo.objects.none()

    # 分页处理
    page_object = Pagination(request, query_set)
    context = {
        "query_set" : page_object.page_queryset,
        'search_value': search_value,
        "page_string" : page_object.html()
    }

    return render(request, 'sightDataList.html', {
        'userInfo': userInfo,
        'context': context
    })

def add_comment(request, sight_id):
    """ 添加评论 """
    username = request.session.get('username')
    userInfo = UserInfo.objects.get(username=username)

    sight_info = getSightData.getOneSightInfoData(sight_id)

    comment_datetime = getTime.get_datetime()
    if request.method == "POST":
        value = request.POST.get('score')
        if not value:
            score = 5  # 如果score为空，则将score设置为5
        else:
            score = int(value)
        getAddCommentsData.addComments({
            'sight_id': sight_id,
            'user_id': userInfo.id,
            'score': score,
            'content': request.POST.get('content'),
            'comment_datetime': comment_datetime
        })
        return redirect('/app/sightDataList')

    return render(request, 'addComment.html', {
        'userInfo': userInfo,
        'sight_id': sight_id,
        'sight_info': sight_info
    })

def recommend_personalized_sights(request):
    """ 景点实时推荐 """
    username = request.session.get('username')
    userInfo = UserInfo.objects.get(username=username)

    recommend_sights = getRecommendSight.get_personalized_recommendations(user_id=userInfo.id, k=10)

    return render(request, 'recommendPersonalizedSights.html', {
        'userInfo': userInfo,
        'recommend_sights': recommend_sights
    })

def recommend_popular_sight(request):
    """ 热门景点推荐 """
    username = request.session.get('username')
    userInfo = UserInfo.objects.get(username=username)
    province_values = ProvinceCity.objects.values_list('province', flat=True).distinct()

    return render(request, 'recommendPopularSight.html', {
        'userInfo': userInfo,
        'provinces': province_values
    })

def get_recommend_popular_sight(request):
    """ 获取热门景点 """
    if request.method == "GET":
        province = request.GET.get('province')
        city = request.GET.get('city')
        queryset = getRecommendSight.get_recommend_popular_sight(province, city)
        return JsonResponse(queryset, safe=False)

def recommend_level_sight(request):
    """ 等级景点推荐 """
    username = request.session.get('username')
    userInfo = UserInfo.objects.get(username=username)
    province_values = ProvinceCity.objects.values_list('province', flat=True).distinct()

    return render(request, 'recommendLevelSight.html', {
        'userInfo': userInfo,
        'provinces': province_values
    })

def get_recommend_level_sight(request):
    """ 获取等级景点 """
    if request.method == "GET":
        province = request.GET.get('province')
        city = request.GET.get('city')

        queryset = getRecommendSight.get_recommend_level_sight(province, city)
        # 创建一个包含修改后对象的列表
        return JsonResponse(queryset, safe=False)

def city_heat_score(request):
    """ 城市热度排行 """
    username = request.session.get('username')
    userInfo = UserInfo.objects.get(username=username)
    city_names, heat_scores = getSightEchartsData.get_city_heat_score_list()

    return render(request, 'cityHeatScore.html', {
        'userInfo': userInfo,
        'cities_with_heat': {
            'Xdata':city_names,
            'Ydata':heat_scores
        }
    })

def get_cities_by_province(request):
    """ 根据省份查询城市 """
    province = request.GET.get('province')
    cities = ProvinceCity.objects.filter(province=province).values_list('city', flat=True).distinct()
    return JsonResponse(list(cities), safe=False)

def sight_score_rate(request):
    """ 景点评分占比 """
    username = request.session.get('username')
    userInfo = UserInfo.objects.get(username=username)

    province_values = ProvinceCity.objects.values_list('province', flat=True).distinct()
    return render(request, 'sightScoreRate.html', {
        'userInfo': userInfo,
        'provinces': province_values
    })

def get_sight_score_rate(request):
    """ 计算景点评分占比 """
    if request.method == "GET":
        province = request.GET.get('province')
        city = request.GET.get('city')
        queryset = getSightEchartsData.get_sight_score_rate(province, city)
        return JsonResponse(list(queryset), safe=False)

def sight_score_top_10(request):
    """ 景点评分前十 """
    username = request.session.get('username')
    userInfo = UserInfo.objects.get(username=username)
    province_values = ProvinceCity.objects.values_list('province', flat=True).distinct()

    return render(request, 'sightScoreTop10.html', {
        'userInfo': userInfo,
        'provinces': province_values
    })

def get_sight_score_top_10(request):
    """ 获取景点评分前十 """
    if request.method == "GET":
        province = request.GET.get('province')
        city = request.GET.get('city')
        queryset = getSightEchartsData.get_sight_score_top_10(province, city)
        return JsonResponse(list(queryset.values()), safe=False)

def sight_heat_score_rate(request):
    """ 景点热度占比 """
    username = request.session.get('username')
    userInfo = UserInfo.objects.get(username=username)

    province_values = ProvinceCity.objects.values_list('province', flat=True).distinct()
    return render(request, 'sightHeatScoreRate.html', {
        'userInfo': userInfo,
        'provinces': province_values
    })

def get_sight_heat_score_rate(request):
    """ 计算景点热度占比 """
    if request.method == "GET":
        province = request.GET.get('province')
        city = request.GET.get('city')
        queryset = getSightEchartsData.get_sight_heat_score_rate(province, city)
        return JsonResponse(list(queryset), safe=False)

def sight_level_rate(request):
    """ 景点等级占比 """
    username = request.session.get('username')
    userInfo = UserInfo.objects.get(username=username)

    province_values = ProvinceCity.objects.values_list('province', flat=True).distinct()
    return render(request, 'sightLevelRate.html', {
        'userInfo': userInfo,
        'provinces': province_values
    })

def get_sight_level_rate(request):
    """ 计算景点等级占比 """
    if request.method == "GET":
        province = request.GET.get('province')
        city = request.GET.get('city')

        queryset = getSightEchartsData.get_sight_level_rate(province, city)
        return JsonResponse(list(queryset), safe=False)

def comment_score_rate(request):
    """ 用户评分占比 """
    username = request.session.get('username')
    userInfo = UserInfo.objects.get(username=username)

    province_values = ProvinceCity.objects.values_list('province', flat=True).distinct()
    return render(request, 'commentScoreRate.html', {
        'userInfo': userInfo,
        'provinces': province_values
    })

def get_comment_score_rate(request):
    """ 计算用户评分占比 """
    if request.method == "GET":
        province = request.GET.get('province')
        city = request.GET.get('city')
        queryset = getCommentEchartsData.get_comment_score_rate(province, city)
        return JsonResponse(list(queryset), safe=False)

def sight_intro_word_cloud(request):
    """ 景点简介词云图 """
    username = request.session.get('username')
    userInfo = UserInfo.objects.get(username=username)

    return render(request, 'sightIntroWordCloud.html', {
        'userInfo': userInfo
    })

def comment_word_cloud(request):
    """ 用户评论词云图 """
    username = request.session.get('username')
    userInfo = UserInfo.objects.get(username=username)

    return render(request, 'commentWordCloud.html', {
        'userInfo': userInfo
    })

def sight_detail_info(request, sight_id):
    username = request.session.get('username')
    userInfo = UserInfo.objects.get(username=username)

    sight_info = getSightData.getOneSightInfoData(sight_id)
    comments_count = getSightData.getSightCommentsCount(sight_id)
    sight_comment_info = getCommentData.getSightCommentData(sight_id)
    img_list = json.loads(sight_info.img_list)
    intro = truncate_chinese(sight_info.intro, 200)
    guess_user_likes = getRecommendSight.get_recommend_similar_sights(sight_info)
    is_favorited = UserFavorites.objects.filter(user_id=userInfo.id, sight_id=sight_id).exists()

    page_object = Pagination(request, sight_comment_info)
    context = {
        "query_set" : page_object.page_queryset,
        "page_string" : page_object.html()
    }

    getUserBehaviorData.save_user_browse_records(userInfo.id, sight_id) #记录用户浏览数据
    
    return render(request, 'sightDetailInfo.html', {
        'userInfo': userInfo,
        'sight_id': sight_id,
        'sight_info': sight_info,
        'img_list': img_list,
        'intro': intro,
        'comments_count': comments_count,
        'context': context,
        'guess_user_likes': guess_user_likes,
        'is_favorited': is_favorited
    })


def get_user_favorite_sight(request, sight_id):
    """收藏景点"""
    username = request.session.get('username')
    userInfo = UserInfo.objects.get(username=username)
    if request.method == 'POST':
        result = getUserBehaviorData.save_user_favorite_records(userInfo.id, sight_id)
        return JsonResponse({'is_favorited': True if result else False})
    else:
        return JsonResponse({'error': 'Invalid request method'}, status=400)


def cancel_user_favorite_sight(request, sight_id):
    """取消收藏"""
    username = request.session.get('username')
    userInfo = UserInfo.objects.get(username=username)
    if request.method == 'POST':
        result = getUserBehaviorData.cancel_user_favorite_records(userInfo.id, sight_id)
        return JsonResponse({'is_favorited': False if result else True, 'success': True})

def user_favorite_info(request):
    """ 用户收藏列表 """
    username = request.session.get('username')
    userInfo = UserInfo.objects.get(username=username)

    query_set = getUserBehaviorData.get_user_favorite_records(user_id=userInfo.id)

    # 分页处理
    page_object = Pagination(request, query_set)
    context = {
        "query_set": page_object.page_queryset,
        "page_string": page_object.html()
    }

    return render(request, 'userFavoriteInfo.html', {
        'userInfo': userInfo,
        'context': context
    })

def admin_register(request):
    if request.method == 'POST':
        adminname = request.POST.get('adminname')
        contact_info = request.POST.get('contact_info')
        password = request.POST.get('password')
        confirm_password = request.POST.get('confirm_password')

        # 验证密码和确认密码是否一致
        if password != confirm_password:
            return JsonResponse({'error': '两次输入的密码不一致'})

        # 验证用户名是否已存在
        if AdminInfo.objects.filter(adminname=adminname).exists():
            return JsonResponse({'error': '用户名已存在'})

        # 使用bcrypt哈希密码
        hashed_password = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt()).decode('utf-8')

        # 创建新用户并保存
        admin = AdminInfo(adminname=adminname, password=hashed_password,contact_info=contact_info,create_time=getTime.get_datetime())
        admin.save()

        return JsonResponse({'success': '注册成功'})

def admin_login(request):
    """ 管理员登录 """
    if request.method == 'POST':
        adminname = request.POST.get('adminname')
        password = request.POST.get('password')

        try:
            # 尝试获取用户信息
            admin = AdminInfo.objects.get(adminname=adminname)
            if bcrypt.checkpw(password.encode('utf-8'), admin.password.encode('utf-8')):
                request.session['adminname'] = adminname
                admin.last_login_time = getTime.get_datetime()
                admin.save()
                return redirect('/app/adminHome')
            else:
                return JsonResponse({'error': '密码输入错误'})
        except AdminInfo.DoesNotExist:
            # 用户未注册
            return JsonResponse({'error': '用户未注册'})

    return render(request, 'admin_login.html')

def admin_home(request):
    """ 管理员首页 """
    return admin_user_info_list(request)

def update_admin_info(request):
    """ 管理员修改信息 """
    adminname = request.session.get('adminname')
    adminInfo = AdminInfo.objects.get(adminname=adminname)

    if request.method == 'POST':
        updateAdminData.update_admin_info(adminname, request.POST, request.FILES)
        adminInfo = AdminInfo.objects.get(adminname=adminname)
    return render(request, 'updateAdminInfo.html', {
        'adminInfo': adminInfo
    })

def update_admin_password(request):
    """ 管理员修改密码 """
    adminname = request.session.get('adminname')
    adminInfo = AdminInfo.objects.get(adminname=adminname)

    if request.method == 'POST':
        return updateAdminData.update_admin_password(adminname, request.POST)

    return render(request, 'updateAdminPassword.html', {
        'adminInfo': adminInfo
    })

def admin_user_info_list(request):
    """ 管理员用户信息列表 """
    adminname = request.session.get('adminname')
    adminInfo = AdminInfo.objects.get(adminname=adminname)

    query_set = getUserData.getAllUserInfoData()

    page_object = Pagination(request, query_set)

    context = {
        "query_set": page_object.page_queryset,
        "page_string": page_object.html()
    }

    return render(request, 'adminUserInfoList.html', {
        'adminInfo': adminInfo,
        'context': context
    })

def admin_search_user_info_by_username(request, search_value):
    """ 管理员搜索用户 """
    adminname = request.session.get('adminname')
    adminInfo = AdminInfo.objects.get(adminname=adminname)
    if search_value:
        query_set = UserInfo.objects.filter(username__icontains=search_value).order_by('-create_time')
    else:
        query_set = getUserData.getAllUserInfoData()

    # 分页处理
    page_object = Pagination(request, query_set)
    context = {
        "query_set" : page_object.page_queryset,
        'search_value': search_value,
        "page_string" : page_object.html()
    }

    return render(request, 'adminUserInfoList.html', {
        'adminInfo': adminInfo,
        'context': context
    })

def admin_add_user(request):
    """ 新增用户 """
    adminname = request.session.get('adminname')
    adminInfo = AdminInfo.objects.get(adminname=adminname)
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        confirm_password = request.POST.get('confirm_password')
        contact_info = request.POST.get('contact_info')
        sex = request.POST.get('sex')
        address = request.POST.get('address')
        intro = request.POST.get('intro')
        avatar = request.FILES.get('avatar')

        # 校验用户名是否已存在
        if UserInfo.objects.filter(username=username).exists():
            return JsonResponse({'error': '用户名已存在'})

        # 校验密码和确认密码是否一致
        if password != confirm_password:
            return JsonResponse({'error': '两次输入的密码不一致'})

        # 使用bcrypt对密码进行加密
        hashed_password = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt()).decode('utf-8')

        # 创建UserInfo实例
        user_info = UserInfo(
            username=username,
            password=hashed_password,
            contact_info=contact_info,
            sex=sex,
            address=address,
            intro=intro,
            avatar=avatar,
            create_time=getTime.get_datetime()
        )
        user_info.save()

        return redirect('adminUserInfoList')

    return render(request, 'adminAddUser.html', {
        'adminInfo': adminInfo
    })

def admin_update_user_password(request, username):
    """ 修改用户密码 """
    adminname = request.session.get('adminname')
    adminInfo = AdminInfo.objects.get(adminname=adminname)

    userInfo = UserInfo.objects.get(username=username)
    if request.method == 'POST':
        form_data = request.POST
        try:
            user = UserInfo.objects.get(username=username)
            new_password = form_data['newPassword']
            confirm_password = form_data['confirmPassword']

            # 新密码与确认密码是否相等
            if new_password != confirm_password:
                return JsonResponse({'error': '新密码与确认密码不一致'})
            # 修改密码
            user.password = bcrypt.hashpw(new_password.encode('utf-8'), bcrypt.gensalt()).decode('utf-8')
            user.save()
            return JsonResponse({'success': '修改成功'})

        except:
            return JsonResponse({'error': '修改失败'})

    return render(request, 'adminUpdateUserPassword.html', {
        'adminInfo': adminInfo,
        'userInfo': userInfo
    })

def admin_update_user_info(request, username):
    """ 修改用户信息 """
    adminname = request.session.get('adminname')
    adminInfo = AdminInfo.objects.get(adminname=adminname)
    userInfo = UserInfo.objects.get(username=username)

    if request.method == 'POST':
        updateUserData.update_user_info(username, request.POST, request.FILES)
        userInfo = UserInfo.objects.get(username=username)
    return render(request, 'adminUpdateUserInfo.html', {
        'adminInfo': adminInfo,
        'userInfo': userInfo
    })

def admin_delete_user(request, username):
    user = UserInfo.objects.get(username=username)
    userInfo = UserInfo.objects.get(username=username)
    if user:
        user_favorites = UserFavorites.objects.filter(user_id=userInfo.id)
        user_favorites.delete()

        user_browses = UserBrowses.objects.filter(user_id=userInfo.id)
        user_browses.delete()

        user_search_records = UserSearchRecords.objects.filter(user_id=userInfo.id)
        user_search_records.delete()

        user.delete()
    return redirect('/app/adminUserInfoList')

def admin_sight_info_list(request):
    """ 管理员景点信息列表 """
    adminname = request.session.get('adminname')
    adminInfo = AdminInfo.objects.get(adminname=adminname)

    query_set = getSightData.getAllSightInfoData()

    page_object = Pagination(request, query_set)

    context = {
        "query_set": page_object.page_queryset,
        "page_string": page_object.html()
    }

    return render(request, 'adminSightInfoList.html', {
        'adminInfo': adminInfo,
        'context': context
    })

def admin_search_sight(request, search_value):
    """ 管理员搜索景点 """
    adminname = request.session.get('adminname')
    adminInfo = AdminInfo.objects.get(adminname=adminname)
    if search_value:
        query_set = SightInfo.objects.filter(sight_name__icontains=search_value).order_by('-sight_id')
    else:
        query_set = getSightData.getAllSightInfoData()

    # 分页处理
    page_object = Pagination(request, query_set)
    context = {
        "query_set": page_object.page_queryset,
        'search_value': search_value,
        "page_string": page_object.html()
    }

    return render(request, 'adminSightInfoList.html', {
        'adminInfo': adminInfo,
        'context': context
    })

def admin_update_sight_info(request, sight_id):
    adminname = request.session.get('adminname')
    adminInfo = AdminInfo.objects.get(adminname=adminname)
    sightInfo = SightInfo.objects.get(sight_id=sight_id)
    province_values = ProvinceCity.objects.values_list('province', flat=True).distinct()

    if request.method == 'POST':
        # 创建FileSystemStorage实例
        cover_storage = FileSystemStorage(location=os.path.join(settings.MEDIA_ROOT, 'cover'))
        img_list_storage = FileSystemStorage(location=os.path.join(settings.MEDIA_ROOT, 'img_list'))

        # 处理上传的cover
        cover = request.FILES.get('cover')
        if cover:
            cover_name = cover_storage.save(cover.name, cover)
            uploaded_cover_file = os.path.join(settings.MEDIA_URL, 'cover', cover_name).replace('\\', '/')
        else:
            uploaded_cover_file = None

        # 处理上传的img_list
        img_list_files = []
        for img in request.FILES.getlist('img_list'):
            img_name = img_list_storage.save(img.name, img)
            uploaded_img_file = os.path.join(settings.MEDIA_URL, 'img_list', img_name).replace('\\', '/')
            img_list_files.append(uploaded_img_file)

        sight_name = request.POST.get('sight_name')
        province = request.POST.get('province')
        city = request.POST.get('city')
        tag_list = request.POST.get('tag_list')
        level = request.POST.get('level')
        heat_score = request.POST.get('heat_score')
        score = request.POST.get('score')
        address = request.POST.get('address')
        telephone = request.POST.get('telephone')
        intro = request.POST.get('intro')
        opening_time = request.POST.get('opening_time')

        # 验证字段
        if len(province) == 0:
            return JsonResponse({'error': '请选择省份'})
        if len(city) == 0:
            return JsonResponse({'error': '请选择城市'})
        if len(score) == 0 or not (0 <= float(score) <= 5):
            return JsonResponse({'error': '评分必须在0到5之间'})
        if len(heat_score) == 0 or not (0 <= float(heat_score) <= 10):
            return JsonResponse({'error': '热度必须在0到10之间'})

        # 更新SightInfo数据
        sightInfo.sight_name = sight_name
        sightInfo.province = province
        sightInfo.city = city
        sightInfo.tag_list = tag_list
        sightInfo.level = level
        sightInfo.heat_score = heat_score
        sightInfo.score = score
        sightInfo.address = address
        sightInfo.telephone = telephone
        if len(intro) != 0 or intro:
            sightInfo.intro = intro
        sightInfo.opening_time = opening_time
        if uploaded_cover_file:
            sightInfo.cover = uploaded_cover_file
        if img_list_files:
            sightInfo.img_list = json.dumps(img_list_files)
        sightInfo.save()

    # 加载表单的初始数据
    return render(request, 'adminUpdateSightInfo.html', {
        'adminInfo': adminInfo,
        'sightInfo': sightInfo,
        'sight_id': sight_id,
        'provinces': province_values
    })

def admin_delete_sight(request, sight_id):
    sight = getSightData.getOneSightInfoData(sight_id=sight_id)
    # 删除景点，一并删除收藏、浏览和评论记录
    if sight:
        user_favorites = UserFavorites.objects.filter(sight_id=sight_id)
        user_favorites.delete()

        user_browses = UserBrowses.objects.filter(sight_id=sight_id)
        user_browses.delete()

        comment_info = CommentInfo.objects.filter(sight_id=sight_id)
        comment_info.delete()

        sight.delete()
    return redirect('/app/adminSightInfoList')

def admin_add_sight(request):
    """ 新增景点 """
    adminname = request.session.get('adminname')
    adminInfo = AdminInfo.objects.get(adminname=adminname)

    if request.method == 'POST':
        # 创建一个FileSystemStorage实例来保存上传的文件
        cover_storage = FileSystemStorage(location=os.path.join(settings.MEDIA_ROOT, 'cover'))
        img_list_storage = FileSystemStorage(location=os.path.join(settings.MEDIA_ROOT, 'img_list'))

        # 处理上传的cover图片
        cover = request.FILES.get('cover')
        if cover:
            cover_name = cover_storage.save(cover.name, cover)
            uploaded_cover_file = os.path.join(settings.MEDIA_URL, 'cover', cover_name).replace('\\', '/')
        else:
            uploaded_cover_file = None

        # 处理上传的img_list图片列表
        img_list_files = []
        for img in request.FILES.getlist('img_list'):
            img_name = img_list_storage.save(img.name, img)
            uploaded_img_file = os.path.join(settings.MEDIA_URL, 'img_list', img_name).replace('\\', '/')
            img_list_files.append(uploaded_img_file)

        # 其余字段的处理
        sight_name = request.POST.get('sight_name')
        province = request.POST.get('province')
        city = request.POST.get('city')

        tag_list_str = request.POST.get('tag_list','')
        tag_list = str(tag_list_str).split('，')
        tag_list = [tag.strip() for tag in tag_list]

        level = request.POST.get('level', '未评级')
        heat_score = request.POST.get('heat_score','0')
        score = request.POST.get('score','0')
        address = request.POST.get('address')
        telephone = request.POST.get('telephone')
        intro = request.POST.get('intro')
        opening_time = request.POST.get('opening_time')

        if len(province) == 0:
            return JsonResponse({'error': '请选择省份'})
        if len(city) == 0:
            return JsonResponse({'error': '请选择城市'})
        if len(score) == 0 or not (0 <= float(score) <= 5):
            return JsonResponse({'error': '评分必须在0到5之间'})
        if len(score) == 0 or not (0 <= float(heat_score) <= 10):
            return JsonResponse({'error': '热度必须在0到10之间'})

        # 获取当前的最大sight_id
        max_sight_id = SightInfo.objects.all().aggregate(max_id=Max('sight_id'))['max_id']
        if max_sight_id is None:
            next_sight_id = 1
        else:
            next_sight_id = max_sight_id + 1

        # 创建SightInfo实例并保存
        sight_info = SightInfo(
            sight_id=next_sight_id,
            sight_name=sight_name,
            province=province,
            city=city,
            tag_list=tag_list,
            level=level,
            heat_score=heat_score,
            score=score,
            address=address,
            telephone=telephone,
            intro=intro,
            opening_time=opening_time,
            cover=uploaded_cover_file,
        )
        sight_info.save()

        # 保存img_list到SightInfo实例中
        sight_info.img_list = json.dumps(img_list_files)  # 将Python对象转换为JSON字符串
        sight_info.save()

        return redirect('adminSightInfoList')

    province_values = ProvinceCity.objects.values_list('province', flat=True).distinct()

    return render(request, 'adminAddSight.html', {
        'adminInfo': adminInfo,
        'provinces': province_values
    })

def admin_sight_detail_info(request, sight_id):
    adminname = request.session.get('adminname')
    adminInfo = AdminInfo.objects.get(adminname=adminname)

    sight_info = getSightData.getOneSightInfoData(sight_id)
    comments_count = getSightData.getSightCommentsCount(sight_id)
    img_list = json.loads(sight_info.img_list)
    intro = truncate_chinese(sight_info.intro, 400)

    return render(request, 'adminSightDetailInfo.html', {
        'adminInfo': adminInfo,
        'sight_id': sight_id,
        'sight_info': sight_info,
        'img_list': img_list,
        'intro': intro,
        'comments_count': comments_count,
    })

def admin_comment_info_list(request):
    """ 管理员 评论信息列表 """
    adminname = request.session.get('adminname')
    adminInfo = AdminInfo.objects.get(adminname=adminname)

    query_set = getCommentData.getAllCommentData()

    page_object = Pagination(request, query_set)

    context = {
        "query_set": page_object.page_queryset,
        "page_string": page_object.html()
    }

    return render(request, 'adminCommentInfoList.html', {
        'adminInfo': adminInfo,
        'context': context
    })

def admin_search_comment_info_by_username(request, search_value):
    """ 管理员 通过用户名搜索评论 """
    adminname = request.session.get('adminname')
    adminInfo = AdminInfo.objects.get(adminname=adminname)
    if search_value:
        query_set = getCommentData.getCommentsContainingSearchUsername(search_value=search_value)
    else:
        query_set = getCommentData.getAllCommentData()

    # 分页处理
    page_object = Pagination(request, query_set)
    context = {
        "query_set": page_object.page_queryset,
        'search_value': search_value,
        "page_string": page_object.html()
    }

    return render(request, 'adminCommentInfoList.html', {
        'adminInfo': adminInfo,
        'context': context
    })

def admin_delete_comment(request, comment_id):
    comment = CommentInfo.objects.get(id=comment_id)
    if comment:
        comment.delete()
    return redirect('/app/adminCommentInfoList')

def admin_user_favorite_info_list(request):
    """ 管理员 用户收藏列表 """
    adminname = request.session.get('adminname')
    adminInfo = AdminInfo.objects.get(adminname=adminname)

    query_set = getUserBehaviorData.getAllUserFavoriteInfoData()

    page_object = Pagination(request, query_set)

    context = {
        "query_set": page_object.page_queryset,
        "page_string": page_object.html()
    }

    return render(request, 'adminUserFavoriteInfoList.html', {
        'adminInfo': adminInfo,
        'context': context
    })

def admin_search_user_favorite_by_username(request, search_value):
    adminname = request.session.get('adminname')
    adminInfo = AdminInfo.objects.get(adminname=adminname)
    if search_value:
        query_set = getUserBehaviorData.getUserFavoriteDataByUsername(search_value=search_value)
    else:
        query_set = getUserBehaviorData.getAllUserFavoriteInfoData()

    # 分页处理
    page_object = Pagination(request, query_set)
    context = {
        "query_set": page_object.page_queryset,
        'search_value': search_value,
        "page_string": page_object.html()
    }

    return render(request, 'adminUserFavoriteInfoList.html', {
        'adminInfo': adminInfo,
        'context': context
    })

def admin_user_search_records_list(request):
    """ 管理员 用户搜索列表 """
    adminname = request.session.get('adminname')
    adminInfo = AdminInfo.objects.get(adminname=adminname)

    query_set = getUserBehaviorData.getAllUserSearchRecords()

    page_object = Pagination(request, query_set)

    context = {
        "query_set": page_object.page_queryset,
        "page_string": page_object.html()
    }

    return render(request, 'adminUserSearchRecordsList.html', {
        'adminInfo': adminInfo,
        'context': context
    })

def admin_search_user_search_records_by_username(request, search_value):
    adminname = request.session.get('adminname')
    adminInfo = AdminInfo.objects.get(adminname=adminname)
    if search_value:
        query_set = getUserBehaviorData.getUserSearchRecordsByUsername(search_value=search_value)
    else:
        query_set = getUserBehaviorData.getAllUserSearchRecords()

    # 分页处理
    page_object = Pagination(request, query_set)
    context = {
        "query_set": page_object.page_queryset,
        'search_value': search_value,
        "page_string": page_object.html()
    }

    return render(request, 'adminUserSearchRecordsList.html', {
        'adminInfo': adminInfo,
        'context': context
    })


def admin_user_browse_info_list(request):
    """ 管理员 用户浏览列表 """
    adminname = request.session.get('adminname')
    adminInfo = AdminInfo.objects.get(adminname=adminname)

    query_set = getUserBehaviorData.getAllUserBrowseInfoData()

    page_object = Pagination(request, query_set)

    context = {
        "query_set": page_object.page_queryset,
        "page_string": page_object.html()
    }

    return render(request, 'adminUserBrowseInfoList.html', {
        'adminInfo': adminInfo,
        'context': context
    })

def admin_search_user_browse_by_username(request, search_value):
    adminname = request.session.get('adminname')
    adminInfo = AdminInfo.objects.get(adminname=adminname)
    if search_value:
        query_set = getUserBehaviorData.getUserBrowsesByUsername(search_value=search_value)
    else:
        query_set = getUserBehaviorData.getAllUserBrowseInfoData()

    # 分页处理
    page_object = Pagination(request, query_set)
    context = {
        "query_set": page_object.page_queryset,
        'search_value': search_value,
        "page_string": page_object.html()
    }

    return render(request, 'adminUserBrowseInfoList.html', {
        'adminInfo': adminInfo,
        'context': context
    })