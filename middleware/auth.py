from django.conf import settings
from django.shortcuts import redirect
from django.http import JsonResponse, HttpResponse


# pylint: disable=C0111,R1710,W0613


class LoginRequired:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        path = request.META.get("PATH_INFO")
        # print("path: ", path, request.user.is_authenticated, request.user.role, request.method)
        if request.user.is_authenticated:
            if request.user.role != "admin" and path.startswith("/api/admin"):
                print('admin-------')
                if path not in settings.TEACGER_ADMIN_API or request.method != "GET":
                    if request.is_ajax():
                        return JsonResponse(
                            {
                                "error": "权限错误",
                            },
                            status=403,
                        )
                    else:
                        html_text = '''<html><body><h1><a href="/">返回首页</a></h1><h1>权限错误</h1></body></html>'''
                        return HttpResponse(html_text, status=403)
        elif path not in settings.NOT_LOGIN_LIST:
            print('user----------')
            if path.startswith("/api/admin"):
                return redirect(settings.ADMIN_LOGIN_PATH)
            else:
                return redirect(settings.LOGIN_PATH)
        response = self.get_response(request)
        return response
