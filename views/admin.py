import json
import math

from django.shortcuts import render, redirect
from django.http import JsonResponse, HttpResponse
from django.views import View
from django.contrib.auth import login, logout
from django.contrib.auth.hashers import make_password

from ..models.user import User
from ..models.room import RoomInfo
from ..models.book import Register, OrderInformation, COrder, ROrder


def admin_auth(func):
    def f(*args, **kwargs):
        request = args[1]
        # path = request.META.get("PATH_INFO")
        if request.user.role != "admin": # and path.startswith("/admin"):
            return JsonResponse(
                {
                    "error": "权限错误",
                },
                status=403,
            )
        return func(*args, **kwargs)
    return f


class AuthMixin:
    def __init__(self, request):
        pass


class Admin(View):
    def get(self, request):
        print('-------', request.user)
        return redirect("admin_room_page")


class AdminLogin(View):
    """ 管理员登录，默认是只有一个管理员 """
    def get(self, request):
        return render(request, 'admin/login.html')

    def post(self, request):
        args = json.loads(request.body)  # 获取前端页面提交的信息
        user_name = args.get("user_name")
        password = args.get("password")
        admin = User.objects.filter(user_name=user_name, role="admin")

        if admin.count() == 0:
            if user_name == "admin" and password == "admin":
                return redirect("admin_regist_page")
            else:
                return JsonResponse({"error": "用户名或密码错误,登陆失败"}, status=403)

        admin = admin.first()
        if admin and admin.check_password(password):  # check_password 返回一个boolean值 能够处理hash类型的密码
            try:
                print('11111111111111111')
                login(request, admin)
            except Exception:
                return JsonResponse({"error": "登陆失败请联系管理员"}, status=400)
            return redirect("admin_page")

        return JsonResponse({"error": "用户名或密码错误,登陆失败"}, status=403)


class AdminRegist(View):
    def get(self, request):
        return render(request, "admin/register.html")

    def patch(self, request):
        admin = User.objects.filter(user_name="admin").first()
        if admin:
            return JsonResponse({"error": "权限错误"}, status=403)

        args = json.loads(request.body)
        user_name = args.get("user_name") or "admin"
        password = args.get("password")
        admin = User.create_user(user_name, password, "admin")
        login(request, admin)  # 内置方法 在请求中保留用户ID和后端 用户不会必须对每个请求重新进行身份验证
        return redirect("admin_page")


class AdminLogout(View):
    def delete(self, request):
        logout(request)  # django自带的登出方法，从request中将id移除
        return redirect("admin_login_page")


class AdminViewMixin:
    def __init__(self, request):
        self.request = request

    def get_list_by_page(self, request):
        user_name = request.user.user_name
        print('-----------user_name', user_name)
        page = int(request.GET.get("page") or 1)
        size = int(request.GET.get("size") or 10)
        # user_name = request.GET.get("user_name")
        query_set = User.objects.filter(is_active=True, user_name=user_name)
        total = query_set.count()
        infos = query_set.order_by("id")[(page - 1) * size: page * size]
        return JsonResponse(
            {
                "infos": [
                    {
                        "id": info.id,
                        "user_name": info.user_name,
                        "role": info.role,
                        "phone": info.phone,
                        "email": info.email,
                    }
                    for info in infos
                ],
                'page': {
                    'total': math.ceil(total / size),
                    'current': page,
                    'size': size
                },
            }
        )

    def get(self, request):
        return self.get_list_by_page(request)


class AdminInfoPage(View):
    def get(self, request):
        return render(request, 'admin/admin_info.html')


class AdminInfo(View, AdminViewMixin):
    def post(self, request):
        pass


class ChangePasswordPage(View):
    def get(self, request):
        return render(request, "admin/change_password.html")


class ChangePassword(View):

    def patch(self, request):
        """首次登陆强制修改密码 ｜ 默认密码同学号or工号"""
        args = json.loads(request.body)
        user_name = args.get("user_name")
        password = args.get("password")
        old_password = args.get("old_password")
        print('------------old_password', old_password)
        print('------------password', password)
        if not password:
            return JsonResponse(
                {
                    "error": "请输入密码",
                },
                status=400,
            )
        try:
            user = User.objects.get(user_name=request.user.user_name)
            print('------------user_name', user_name)
        except:
            return JsonResponse(
                {
                    "error": "用户名或密码错误",
                }
            )
        if not user.check_password(old_password):
            return JsonResponse(
                {
                    "error": "用户名或密码错误",
                }
            )
        user.password = make_password(password)
        user.save()
        # User.create_user(user_name, password, request.user.role)
        return redirect("admin_login_page")


class CheckInPage(View):
    def get(self, request):
        return render(request, "admin/check_in.html")


class CheckIn(View):
    def post(self, request):
        args = json.loads(request.body)
        start_time = args.get("start_time")
        rno = args.get("rno")
        uno = args.get("uno")
        id_card = args.get("id_card1")
        register = Register.create_register(start_time=start_time, rno=rno, uno=uno, id_card=id_card)
        return JsonResponse(
            {
                "id": register.id,
                "start_time": register.start_time,
                "rno": register.rno,
                "uno": register.uno,
                "id_card": register.id_card,
            }
        )


class CreateRoomOrder(View):
    def post(self, request):
        args = json.loads(request.body)
        uno = args.get("uno")
        rno = args.get("rno")
        start_time = args.get("start_time")
        end_time = args.get("end_time")
        id_card = args.get("id_card2")
        # print('-----------id_card', id_card)
        rooms = RoomInfo.objects.filter(is_active=True)
        price_map = {i[0]: i[7] for i in rooms.values_list()}
        price = price_map.get(int(rno))
        print('-------------price', price)
        user_register_info = Register.objects.filter(id_card=id_card).first()
        print('----------------user_register_info', user_register_info)
        if user_register_info:
            order = OrderInformation(start_time=start_time, end_time=end_time, uno=uno, rno=rno, num=1, price=price)
            order.save()
            return JsonResponse(
                {
                    "id": order.id,
                    "ono": order.ono,
                    "start_time": order.start_time,
                    "end_time": order.end_time,
                    "uno": order.uno,
                    "rno": order.rno,
                    "num": order.num,
                    "price": order.price,

                }
            )
        return HttpResponse('身份证输入错误！！！')


class UserInfos(View):
    def get(self, request):
        response = HttpResponse()
        # response.set_cookie(key="user_id", value=str(request.user.user_id))
        response.set_cookie(key="user_name", value=json.dumps(request.user.user_name))
        response.set_cookie(key="role", value=json.dumps(request.user.role))
        response.status_code = 204
        return response
