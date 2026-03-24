from django.utils.deprecation import MiddlewareMixin
from django.shortcuts import redirect

class UserMiddleWare(MiddlewareMixin):
    def process_request(self, request):
        path = request.path_info
        if path in ['/app/login/', '/app/register/', '/app/adminLogin/']:
            return None
        else:
            if request.session.get('adminname') or request.session.get('username'):
                return None
            else:
                return redirect('/app/login/')