import json
import math

from django.views import View
from django.http import HttpResponse, JsonResponse
from django.shortcuts import render

from ..models.room import RoomInfo
from ..models.commodity import CommodityInfo
from ..models.book import BookingInformation, Register, OrderInformation
from ..models.user import User


class RoomInfoViewMixin:

    def __init__(self, request):
        self.request = request

    # 获取页数和Room表中的内容
    def get_list_by_page(self, request):
        print("request.user: ", request.user)
        page = int(request.GET.get("page") or 1)
        size = int(request.GET.get("size") or 10)
        query_set = RoomInfo.objects.filter(is_active=True)
        total = query_set.count()
        infos = query_set.order_by("id")[(page - 1) * size: page * size]
        return JsonResponse(
            {
                "infos": [
                    {
                        "id": info.id,
                        "rno": info.rno,
                        "style": info.style,
                        "dsc": info.dsc,
                        "price": info.price,
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

    def delete(self, request):
        # id = json.loads(request.body or "{}").get('id')
        id = request.GET.get("id")
        if not id:
            return JsonResponse(
                {
                    "error": "请求参数错误"
                },
                status=400
            )
        info = RoomInfo.objects.get(id=id)
        info.is_active = False
        info.save()
        return HttpResponse(status=204)


class RoomPage(View):
    # 获取列表内容

    def get(self, request):
        print('--------------request.user3', request.user)
        return render(request, "admin/room.html")


class Room(View, RoomInfoViewMixin):
    # 增加内容
    def post(self, request):
        args = json.loads(request.body)
        rno = args.get("rno")
        style = args.get("style")
        dsc = args.get("dsc")
        price = args.get("price")
        if RoomInfo.objects.filter(rno=rno, is_active=True).exists():
            return JsonResponse(
                {
                    "error": "该房间号已存在，请重新输入"
                },
                status=400,
            )
        room = RoomInfo.create_room(rno=rno, style=style, dsc=dsc, price=price)
        return JsonResponse(
            {
                "id": room.id,
                "rno": room.rno,
                "style": room.style,
                "dsc": room.dsc,
                "price": room.price,
            }
        )

    # 修改内容
    def patch(self, request):
        args = json.loads(request.body)
        rno = args["rno"]
        style = args["style"]
        dsc = args["dsc"]
        price = args["price"]
        room = RoomInfo.objects.filter(rno=rno).first()  # 可能有重复值，获取第一个
        room.rno = rno
        room.style = style
        room.dsc = dsc
        room.price = price
        room.save()
        return JsonResponse(
            {
                'id': room.id,
                "rno": room.rno,
                'style': room.style,
                'dsc': room.dsc,
                'price': room.price,
            }
        )


class CommodityInfoViewMixin:

    def __init__(self, request):
        self.request = request

    def get_list_by_page(self, request):
        page = int(request.GET.get("page") or 1)
        size = int(request.GET.get("size") or 10)
        query_set = CommodityInfo.objects.filter(is_active=True)
        total = query_set.count()
        infos = query_set.order_by("id")[(page - 1) * size: page * size]
        return JsonResponse(
            {
                "infos": [
                    {
                        "id": info.id,
                        "cno": info.cno,
                        "type": info.type,
                        "price": info.price,
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

    def delete(self, request):
        # id = json.loads(request.body or "{}").get('id')
        id = request.GET.get("id")
        if not id:
            return JsonResponse(
                {
                    "error": "请求参数错误"
                },
                status=400
            )
        info = RoomInfo.objects.get(id=id)
        info.is_active = False
        info.save()
        return HttpResponse(status=204)


class CommodityPage(View):
    # 获取列表内容
    def get(self, request):
        # print('-----------', request.user.user_name)
        return render(request, "admin/commodity.html")


class Commodity(View, CommodityInfoViewMixin):
    # 增加内容
    def post(self, request):
        args = json.loads(request.body)
        cno = args.get("cno")
        type = args.get("type")
        price = args.get("price")
        if CommodityInfo.objects.filter(cno=cno, is_active=True).exists():
            return JsonResponse(
                {
                    "error": "该房间号已存在，请重新输入"
                },
                status=400,
            )
        commodity = CommodityInfo.create_commodity(cno=cno, type=type, price=price)
        return JsonResponse(
            {
                "id": commodity.id,
                "cno": commodity.cno,
                "type": commodity.type,
                "price": commodity.price,
            }
        )

    # 修改内容
    def patch(self, request):
        args = json.loads(request.body)
        cno = args["cno"]
        type = args["type"]
        price = args["price"]
        commodity = CommodityInfo.objects.filter(cno=cno).first()  # 可能有重复值，获取第一个
        commodity.cno = cno
        commodity.type = type
        commodity.price = price
        commodity.save()
        return JsonResponse(
            {
                'id': commodity.id,
                "cno": commodity.cno,
                'type': commodity.type,
                'price': commodity.price,
            }
        )


class BookInfoViewMixin:
    def __init__(self, request):
        self.request = request

    def get_list_by_page(self, request):
        page = int(request.GET.get("page") or 1)
        size = int(request.GET.get("size") or 10)
        query_set = BookingInformation.objects.filter(is_delete=False)
        total = query_set.count()
        infos = query_set.order_by("id")[(page - 1) * size: page * size]
        user = User.objects.filter(is_active=True)
        room = RoomInfo.objects.filter(is_active=True)
        user_list = {i[0]: i[5] for i in user.values_list()}
        room_list = {i[0]: i[4] for i in room.values_list()}
        is_cancel_map = {False: "否", True: '是'}
        return JsonResponse(
            {
                "infos": [
                    {
                        "id": info.id,
                        "start_time": info.start_time,
                        "end_time": info.end_time,
                        "is_cancel": is_cancel_map[info.is_cancel],
                        "uno": info.uno_id,
                        "rno": info.rno_id,
                        "status": info.get_status_display(),
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

    def delete(self, request):
        # id = json.loads(request.body or "{}").get('id')
        id = request.GET.get("id")
        if not id:
            return JsonResponse(
                {
                    "error": "请求参数错误"
                },
                status=400
            )
        info = BookingInformation.objects.get(id=id)
        info.is_delete = True
        info.save()
        return HttpResponse(status=204)


class BookPage(View):
    def get(self, request):
        return render(request, "admin/book_room.html")


class Book(View, BookInfoViewMixin):
    def post(self, request):
        args = json.loads(request.body)


class CheckInInfoViewMixin:
    def __init__(self, request):
        self.request = request

    def get_list_by_page(self, request):
        page = int(request.GET.get("page") or 1)
        size = int(request.GET.get("size") or 10)
        query_set = Register.objects.filter(is_delete=False)
        total = query_set.count()
        infos = query_set.order_by("id")[(page - 1) * size: page * size]
        return JsonResponse(
            {
                "infos": [
                    {
                        "id": info.id,
                        "start_time": info.start_time,
                        "rno": info.rno,
                        "uno": info.uno,
                        "id_card": info.id_card,
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

    def delete(self, request):
        # id = json.loads(request.body or "{}").get('id')
        id = request.GET.get("id")
        if not id:
            return JsonResponse(
                {
                    "error": "请求参数错误"
                },
                status=400
            )
        info = Register.objects.get(id=id)
        info.is_delete = True
        info.save()
        return HttpResponse(status=204)


class CheckInInfoPage(View):
    def get(self, request):
        return render(request, "admin/check_in.html")


class CheckInInfo(View, CheckInInfoViewMixin):
    def post(self, request):
        pass

    def patch(self, request):
        args = json.loads(request.body)
        start_time = args["start_time"]
        uno = args["uno"]
        rno = args["rno"]
        id_card = args["id_card"]
        check_in = Register.objects.filter(uno=uno, rno=rno).first()  # 可能有重复值，获取第一个
        check_in.start_time = start_time
        check_in.uno = uno
        check_in.rno = rno
        check_in.id_card = id_card
        check_in.save()
        return JsonResponse(
            {
                'id': check_in.id,
                "start_time": check_in.start_time,
                'uno': check_in.uno,
                'rno': check_in.rno,
                'id_card': check_in.id_card,
            }
        )


class OrderInfoViewMixin:
    def __init__(self, request):
        self.request = request

    def get_list_by_page(self, request):
        page = int(request.GET.get("page") or 1)
        size = int(request.GET.get("size") or 10)
        query_set = OrderInformation.objects.filter(is_delete=False)
        total = query_set.count()
        infos = query_set.order_by("id")[(page - 1) * size: page * size]
        return JsonResponse(
            {
                "infos": [
                    {
                        "id": info.id,
                        "ono": info.ono,
                        "uno": info.uno,
                        "rno": info.rno,
                        "num": info.num,
                        "start_time": info.start_time,
                        "end_time": info.end_time,
                        "price": info.price,
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

    def delete(self, request):
        # id = json.loads(request.body or "{}").get('id')
        id = request.GET.get("id")
        if not id:
            return JsonResponse(
                {
                    "error": "请求参数错误"
                },
                status=400
            )
        info = Register.objects.get(id=id)
        info.is_delete = True
        info.save()
        return HttpResponse(status=204)


class OrderInfoPage(View):
    def get(self, request):
        return render(request, "admin/order_info.html")


class OrderInfo(View, OrderInfoViewMixin):
    def post(self, request):
        pass

    def patch(self, request):
        args = json.loads(request.body)
        ono = args["ono"]
        uno = args["uno"]
        rno = args["rno"]
        start_time = args["start_time"]
        end_time = args["end_time"]
        order_info = Register.objects.filter(uno=uno, rno=rno).first()  # 可能有重复值，获取第一个
        check_in.start_time = start_time
        check_in.uno = uno
        check_in.rno = rno
        check_in.id_card = id_card
        check_in.save()
        return JsonResponse(
            {
                'id': check_in.id,
                "start_time": check_in.start_time,
                'uno': check_in.uno,
                'rno': check_in.rno,
                'id_card': check_in.id_card,
            }
        )


class UserInfoViewMixin:

    def __init__(self, request):
        self.request = request

    def get_list_by_page(self, request):
        page = int(request.GET.get("page") or 1)
        size = int(request.GET.get("size") or 10)
        query_set = User.objects.filter(is_active=True, role='user')
        total = query_set.count()
        infos = query_set.order_by("id")[(page - 1) * size: page * size]
        return JsonResponse(
            {
                "infos": [
                    {
                        "id": info.id,
                        "user_name": info.user_name,
                        "password": info.password,
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

    def delete(self, request):
        # id = json.loads(request.body or "{}").get('id')
        id = request.GET.get("id")
        if not id:
            return JsonResponse(
                {
                    "error": "请求参数错误"
                },
                status=400
            )
        info = User.objects.get(id=id)
        info.is_active = False
        info.save()
        return HttpResponse(status=204)


class UserPage(View):
    # 获取列表内容

    def get(self, request):
        print('9999999999')
        return render(request, "admin/user.html")


class Users(View, UserInfoViewMixin):
    # 增加内容
    def post(self, request):
        args = json.loads(request.body)
        user_name = args.get("user_name")
        password = args.get("password")
        phone = args.get("phone")
        email = args.get("email")
        if User.objects.filter(user_name=user_name, is_active=True).exists():
            return JsonResponse(
                {
                    "error": "该用户名已存在，请重新输入"
                },
                status=400,
            )
        user = User.create_user(user_name=user_name, password=password, phone=phone, email=email, role="user")
        return JsonResponse(
            {
                "id": user.id,
                "user_name": user.user_name,
                "password": user.password,
                "phone": user.phone,
                "email": user.email,
            }
        )

    # 修改内容
    def patch(self, request):
        args = json.loads(request.body)
        user_name = args["user_name"]
        password = args["password"]
        phone = args["phone"]
        email = args["email"]
        user = User.objects.filter(user_name=user_name).first()  # 可能有重复值，获取第一个
        user.user_name = user_name
        user.password = password
        user.phone = phone
        user.email = email
        user.save()
        return JsonResponse(
            {
                'id': user.id,
                "user_name": user.user_name,
                'phone': user.phone,
                'password': user.password,
                'email': user.email,
            }
        )



