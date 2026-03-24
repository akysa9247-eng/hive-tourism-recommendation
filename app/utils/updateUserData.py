import bcrypt
from django.http import JsonResponse

from app.models import UserInfo


def update_user_info(username, form_data, file_data):
    """ 修改个人信息 """
    user = UserInfo.objects.get(username=username)
    user.sex = form_data['sex']

    if form_data['address']:
        user.address = form_data['address']

    if form_data['intro']:
        user.intro = form_data['intro']

    if form_data['contact_info']:
        user.contact_info = form_data['contact_info']

    if file_data.get('avatar') != None:
        user.avatar = file_data.get('avatar')

    user.save()

def update_user_password(username, form_data):
    try:
        user = UserInfo.objects.get(username=username)
        old_password = form_data['oldPassword']
        new_password = form_data['newPassword']
        confirm_password = form_data['confirmPassword']
        # 原始密码是否正确
        if not bcrypt.checkpw(old_password.encode('utf-8'), user.password.encode('utf-8')):
            return JsonResponse({'error': '原始密码错误'})
        # 新密码与确认密码是否相等
        if new_password != confirm_password:
            return JsonResponse({'error': '新密码与确认密码不一致'})
        # 原始密码与新密码是否相等
        if old_password == new_password:
            return JsonResponse({'error': '新密码与原始密码不能一致'})
        # 修改密码
        user.password = bcrypt.hashpw(new_password.encode('utf-8'), bcrypt.gensalt()).decode('utf-8')
        user.save()
        return JsonResponse({'success': '修改成功'})

    except:
        return JsonResponse({'error': '修改失败'})






