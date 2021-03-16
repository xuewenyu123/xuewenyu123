import json
import math

from django.views import View
from django.shortcuts import render, redirect, HttpResponse
from django.http import JsonResponse
from django.contrib.auth import login, logout
from django.db.models import F, Q

from ..models import User, BookingInformation, RoomInfo, CommodityInfo, OrderInformation


class Login(View):
    def get(self, request):
        return render(request, 'user/login.html')

    def post(self, request):
        args = json.loads(request.body)  # 获取前端页面提交的信息
        user_name = args.get("user_name")
        password = args.get("password")
        print('-----------', user_name)
        user = User.objects.filter(user_name=user_name, role="user").first()
        if user and user.check_password(password):  # check_password 返回一个boolean值 能够处理hash类型的密码
            try:
                login(request, user)
            except Exception:
                return JsonResponse({"error": "登陆失败请联系管理员"}, status=400)
            return redirect("user_index_page")

        return JsonResponse({"error": "用户名或密码错误,登陆失败"}, status=403)


class Register(View):
    def get(self, request):
        return render(request, 'user/register.html')

    def post(self, request):
        args = json.loads(request.body)  # 获取前端页面提交的信息
        user_name = args.get("user_name")
        user = User.objects.filter(user_name=user_name).first()
        if user:
            return JsonResponse({"error": "用户名重复，请重新输入"}, status=403)
        password = args.get("password")
        phone = args.get('phone')
        email = args.get('email')
        user = User.create_user(user_name=user_name, password=password, role="user", email=email, phone=phone)
        login(request, user)


class Logout(View):
    def delete(self, request):
        logout(request)  # django自带的登出方法，从request中将id移除
        return redirect("user_login_page")


class UserIndexPage(View):
    def get(self, request):
        return render(request, 'user/index.html')


class UserIndex(View):
    def post(self, request):
        pass


class UserInfoPage(View):
    def get(self, request):
        return render(request, 'user/user_info.html')


class ChangePasswordPage(View):
    def get(self, request):
        return render(request, "user/change_password.html")


class OrderRoom(View):
    def get(self, request):
        return render(request, 'user/order_room.html')


# class BookRoomViewMixin:
#     def __init__(self, request):
#         self.request = request
#
#     def get_list_by_page(self, request):
#         # print('-------------', request.body.startDate)
#         # args = json.loads(request.body)  # 获取前端页面提交的信息
#         # start_time = args.get("startDate")
#         # end_time = args.get("endDate")
#         # style = args.get("style")
#         # price = args.get("price")
#         # print("----------------start_time", start_time)
#         # page = int(request.GET.get("page") or 1)
#         # size = int(request.GET.get("size") or 10)
#         # # user_name = request.GET.get("user_name")
#         # rooms = BookingInformation.objects.filter(
#         #     Q(start_time__gt=F(end_time)) | Q(end_time__lt=F(start_time)),
#         #     is_delete=False,
#         # )  # 预订房间表中的开始时间大于想要预订的结束时间 或者 预订房间表中的结束时间小于想要预订的开始时间
#         # query_set = RoomInfo.objects.filter(style=style)
#
#         page = int(request.GET.get("page") or 1)
#         size = int(request.GET.get("size") or 10)
#         query_set = RoomInfo.objects.filter(is_active=True)
#         total = query_set.count()
#         infos = query_set.order_by("id")[(page - 1) * size: page * size]
#         return JsonResponse(
#             {
#                 "infos": [
#                     {
#                         "id": info.id,
#                         "rno": info.rno,
#                         "style": info.style,
#                         "dsc": info.dsc,
#                         "price": info.price,
#                     }
#                     for info in infos
#                 ],
#                 'page': {
#                     'total': math.ceil(total / size),
#                     'current': page,
#                     'size': size
#                 },
#             }
#         )
#
#     def get(self, request):
#         return self.get_list_by_page(request)
#
#
# class BookRoom(View, BookRoomViewMixin):
#     def post(self, request):
#         args = json.loads(request.body)
#         room_id = args.get("room_id")
#         user_id = args.get('user_id')
#         in_time = args.get('in_time')
#         out_time = args.get('out_time')
#         # book = BookingInformation.objects.filter(
#         #     Q(start_time__gt=F(out_time)) | Q(end_time__lt=F(in_time)),
#         #     bno=room_id,
#         #     uno=user_id,
#         # )  # 预订房间表中的开始时间大于想要预订的结束时间 或者 预订房间表中的结束时间小于想要预订的开始时间
#         book = BookingInformation.create_book(rno=room_id, uno=user_id, start_time=in_time, end_time=out_time)
#         return JsonResponse(
#             {
#                 "rno": book.rno,
#                 "uno": book.uno,
#                 "start_time": book.start_time,
#                 "end_time": book.end_time,
#                 "price": book.price,
#             }
#         )
#
#     def get(self, request):
#         args = json.loads(request.body)
#         in_time = args.get('in_time')
#         out_time = args.get('out_time')
#         style = args.get('style')
#         price = args.get('price')
#
#         min_price = price.split('-')[0]
#         max_price = price.split('-')[1]
#
#         room_info = RoomInfo.objects.filter(style=style, price__gt=min_price, price__lt=max_price)
#         print('-----=', {i[4] for i in room_info.all().values_list()})
#         book_info = BookingInformation.objects.filter(Q(start_time__gt=out_time) | Q(end_time__lt=in_time))
#         print('-----=', {j[7] for j in book_info.all().values_list()})
#         room_ids = {i[4] for i in room_info.all().values_list()} - {j[7] for j in book_info.all().values_list()}
#         rooms = RoomInfo.objects.filter(rno__in=room_ids)
#         return JsonResponse(
#             {
#                 "info": [
#                     {
#                         "id": room.id,
#                         "rno": room.rno,
#                         "style": room.style,
#                         "dsc": room.dsc,
#                         "price": room.price,
#                     }
#                     for room in rooms
#                 ]
#             }
#         )
class BookRoom(View):
    def get(self):
        pass


class Search(View):
    def get(self, request):
        # in_time = request.GET.get('in_time')
        # out_time = request.GET.get('out_time')
        # style = request.GET.get('style')
        # price = request.GET.get('price')
        # min_price = price.split('-')[0]
        # max_price = price.split('-')[1]
        #
        # room_info = RoomInfo.objects.filter(style=style, price__gt=min_price, price__lt=max_price)
        # print('-----=', {i[4] for i in room_info.all().values_list()})
        # book_info = BookingInformation.objects.filter(Q(start_time__gt=out_time) | Q(end_time__lt=in_time))
        # print('-----=', {j[7] for j in book_info.all().values_list()})
        # room_ids = {i[4] for i in room_info.all().values_list()} - {j[7] for j in book_info.all().values_list()}
        # rooms = RoomInfo.objects.filter(rno__in=room_ids, style=style)
        #
        # return JsonResponse(
        #     {
        #         "info": [
        #             {
        #                 "id": room.id,
        #                 "rno": room.rno,
        #                 "style": room.style,
        #                 "dsc": room.dsc,
        #                 "price": room.price,
        #             }
        #             for room in rooms
        #         ]
        #     }
        # )
        in_time = request.GET.get('in_time')
        out_time = request.GET.get('out_time')
        style = request.GET.get('style')
        price = request.GET.get('price')
        rooms = RoomInfo.objects.filter(is_active=True)
        rooms_map = {i[0]: i[4] for i in rooms.all().values_list()}

        min_price = price.split('-')[0]
        max_price = price.split('-')[1]
        if style == "所有类型":
            room_info = RoomInfo.objects.filter(price__gt=min_price, price__lt=max_price)
            print('============room_info', room_info.all())
        else:
            room_info = RoomInfo.objects.filter(style=style, price__gt=min_price, price__lt=max_price)
        book_info = BookingInformation.objects.filter(Q(start_time__gt=out_time) | Q(end_time__lt=in_time))
        for i in book_info:
            print('---------------i', i.rno_id)

        # print('-----=', {i[4] for i in room_info.all().values_list()})
        # print('-----=', {j[7] for j in book_info.all().values_list()})
        book_rnos = set()
        for j in book_info.all().values_list():
            book_rno = rooms_map.get(j[5])
            book_rnos.add(book_rno)
        print('============book_rnos', book_rnos)
        room_ids = {i[4] for i in room_info.all().values_list()} - book_rnos
        print('---------------room_ids', room_ids)
        print('-----------', type(room_ids))
        if style == "所有类型":
            rooms = RoomInfo.objects.filter(rno__in=room_ids)
        else:
            rooms = RoomInfo.objects.filter(rno__in=room_ids, style=style)
        print('--------', rooms.all())
        page = int(request.GET.get("page") or 1)
        size = int(request.GET.get("size") or 10)
        query_set = RoomInfo.objects.filter(is_active=True)
        total = query_set.count()
        # infos = query_set.order_by("id")[(page - 1) * size: page * size]
        return JsonResponse(
            {
                "infos": [
                    {
                        "id": room.id,
                        "rno": room.rno,
                        "style": room.style,
                        "dsc": room.dsc,
                        "price": room.price,
                    }
                    for room in rooms
                ],
                'page': {
                    'total': math.ceil(total / size),
                    'current': page,
                    'size': size
                },
            }
        )


class MyBookInfoViewMixin:
    def __init__(self, request):
        self.request = request

    def get_list_by_page(self, request):
        page = int(request.GET.get("page") or 1)
        size = int(request.GET.get("size") or 10)
        query_set = BookingInformation.objects.filter(is_delete=False, uno=request.user.id)
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
                        "uno": user_list[info.uno_id],
                        "rno": room_list[info.rno_id],
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


class MyBookInfoPage(View):
    def get(self, request):
        return render(request, "user/my_book_info.html")


class MyBookInfo(View, MyBookInfoViewMixin):
    def post(self, request):
        args = json.loads(request.body.decode())
        rno = args.get('rno')
        start_time = args.get('start_time')
        end_time = args.get('end_time')
        room = RoomInfo.objects.filter(is_active=True)
        room_list = {i[4]: i[0] for i in room.values_list()}
        book = BookingInformation.objects.get(
            uno=request.user.id, rno=room_list.get(int(rno)), start_time=start_time, end_time=end_time
        )
        book.is_cancel = True
        book.save()

        return JsonResponse(
            {
                "rno": book.rno_id,
                "uno": book.uno_id,
                "start_time": book.start_time,
                "end_time": book.end_time,
                "is_cancel": book.is_cancel,
            }
        )

    # def get(self, request):
    #     args = json.loads(request.body)
    #     in_time = args.get('in_time')
    #     out_time = args.get('out_time')
    #     style = args.get('style')
    #     price = args.get('price')
    #
    #     min_price = price.split('-')[0]
    #     max_price = price.split('-')[1]
    #
    #     room_info = RoomInfo.objects.filter(style=style, price__gt=min_price, price__lt=max_price)
    #     print('-----=', {i[4] for i in room_info.all().values_list()})
    #     book_info = BookingInformation.objects.filter(Q(start_time__gt=out_time) | Q(end_time__lt=in_time))
    #     print('-----=', {j[7] for j in book_info.all().values_list()})
    #     room_ids = {i[4] for i in room_info.all().values_list()} - {j[7] for j in book_info.all().values_list()}
    #     rooms = RoomInfo.objects.filter(rno__in=room_ids)
    #     return JsonResponse(
    #         {
    #             "info": [
    #                 {
    #                     "id": room.id,
    #                     "rno": room.rno,
    #                     "style": room.style,
    #                     "dsc": room.dsc,
    #                     "price": room.price,
    #                 }
    #                 for room in rooms
    #             ]
    #         }
    #     )


class MyOrderInfoViewMixin:
    def __init__(self, request):
        self.request = request

    def get_list_by_page(self, request):
        page = int(request.GET.get("page") or 1)
        size = int(request.GET.get("size") or 10)
        query_set = OrderInformation.objects.filter(is_delete=False, uno=request.user.id)
        total = query_set.count()
        infos = query_set.order_by("id")[(page - 1) * size: page * size]
        user = User.objects.filter(is_active=True)
        room = RoomInfo.objects.filter(is_active=True)
        user_list = {i[0]: i[5] for i in user.values_list()}
        room_list = {i[0]: i[4] for i in room.values_list()}
        return JsonResponse(
            {
                "infos": [
                    {
                        "id": info.id,
                        "ono": info.ono,
                        "uno": user_list[info.uno],
                        "rno": room_list[info.rno],
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


class MyOrderInfoPage(View):
    def get(self, request):
        return render(request, "user/my_order_info.html")


class MyOrderInfo(View, MyOrderInfoViewMixin):
    def post(self, request):
        pass
        # args = json.loads(request.body)
        # room_id = args.get("room_id")
        # user_id = args.get('user_id')
        # in_time = args.get('in_time')
        # out_time = args.get('out_time')
        # book = BookingInformation.create_book(rno=room_id, uno=user_id, start_time=in_time, end_time=out_time)
        # return JsonResponse(
        #     {
        #         "rno": book.rno,
        #         "uno": book.uno,
        #         "start_time": book.start_time,
        #         "end_time": book.end_time,
        #         "price": book.price,
        #     }
        # )

    # def get(self, request):
    #     args = json.loads(request.body)
    #     in_time = args.get('in_time')
    #     out_time = args.get('out_time')
    #     style = args.get('style')
    #     price = args.get('price')
    #
    #     min_price = price.split('-')[0]
    #     max_price = price.split('-')[1]
    #
    #     room_info = RoomInfo.objects.filter(style=style, price__gt=min_price, price__lt=max_price)
    #     print('-----=', {i[4] for i in room_info.all().values_list()})
    #     book_info = BookingInformation.objects.filter(Q(start_time__gt=out_time) | Q(end_time__lt=in_time))
    #     print('-----=', {j[7] for j in book_info.all().values_list()})
    #     room_ids = {i[4] for i in room_info.all().values_list()} - {j[7] for j in book_info.all().values_list()}
    #     rooms = RoomInfo.objects.filter(rno__in=room_ids)
    #     return JsonResponse(
    #         {
    #             "info": [
    #                 {
    #                     "id": room.id,
    #                     "rno": room.rno,
    #                     "style": room.style,
    #                     "dsc": room.dsc,
    #                     "price": room.price,
    #                 }
    #                 for room in rooms
    #             ]
    #         }
    #     )







