import traceback

import bcrypt
from django.http import JsonResponse

from app.models import AdminInfo

def update_admin_info(adminname, form_data, file_data):
    """ 修改个人信息 """
    admin = AdminInfo.objects.get(adminname=adminname)
    admin.sex = form_data['sex']

    if form_data['address']:
        admin.address = form_data['address']

    if form_data['intro']:
        admin.intro = form_data['intro']

    if form_data['contact_info']:
        admin.contact_info = form_data['contact_info']

    if file_data.get('avatar') != None:
        admin.avatar = file_data.get('avatar')
        print(admin.avatar)

    admin.save()

def update_admin_password(adminname, form_data):
    try:
        admin = AdminInfo.objects.get(adminname=adminname)
        old_password = form_data['oldPassword']
        new_password = form_data['newPassword']
        confirm_password = form_data['confirmPassword']

        # 原始密码是否正确
        if not bcrypt.checkpw(old_password.encode('utf-8'), admin.password.encode('utf-8')):
            return JsonResponse({'error': '原始密码错误'})
        # 原始密码与新密码是否相等
        if old_password == new_password:
            return JsonResponse({'error': '新密码与原始密码不能一致'})
        # 新密码与确认密码是否相等
        if new_password != confirm_password:
            return JsonResponse({'error': '新密码与确认密码不一致'})
        # 修改密码
        admin.password = bcrypt.hashpw(new_password.encode('utf-8'), bcrypt.gensalt()).decode('utf-8')
        admin.save()
        return JsonResponse({'success': '修改成功'})

    except:
        print(traceback.format_exc())
        return JsonResponse({'error': '修改失败'})






