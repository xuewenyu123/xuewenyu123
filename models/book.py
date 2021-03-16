from datetime import datetime
import time
from django.db import models
# from .base import BaseModel


# class OrderNo:
#
#     def __init__(self):
#         self.i = 0
#         self.l = []
#
#     def test(self):
#         if self.i == 100:
#             self.i = 0
#         self.i += 1
#         return self.i
#
#     def no(self):
#         self.l.append(str(int(time.time() * 1000)) + str(self.test()))


class BookingInformation(models.Model):
    """ 预订房间信息表 """
    STATUS_CHOICES = [
        (1, '已预订'),
        (2, '已入住'),
        (3, '已退房'),
    ]
    # bno = models.CharField(default=0, max_length=20)
    is_delete = models.IntegerField(default=0)
    create_time = models.DateTimeField(auto_now_add=True)
    update_time = models.DateTimeField(auto_now=True)
    uno = models.ForeignKey('User', verbose_name='用户编号', on_delete=models.CASCADE)
    rno = models.ForeignKey('RoomInfo', verbose_name='房间编号', on_delete=models.CASCADE)
    start_time = models.DateField(default=datetime.now, null=False, verbose_name='入住时间')
    end_time = models.DateField(default=datetime.now, null=False, verbose_name='退订时间')
    status = models.IntegerField(choices=STATUS_CHOICES, default=1, verbose_name='1.已预订，2.已入住，3.已退房')
    deposit = models.FloatField(default=0, null=False, verbose_name='押金')
    is_cancel = models.BooleanField(default=0, null=False, verbose_name="是否取消预订")
    # is_return = models.BooleanField(default=0, verbose_name='押金是否退回')

    @classmethod
    def create_book(cls, uno, rno, start_time, end_time):  # 学院 -- 地址
        book = cls(uno=uno, rno=rno, start_time=start_time, end_time=end_time)
        book.save()
        return book

    class Meta:
        db_table = "book_info"
        verbose_name = "预订房间信息"
        verbose_name_plural = verbose_name


class Register(models.Model):
    """ 入住房间登记 """
    is_delete = models.IntegerField(default=0)
    create_time = models.DateTimeField(auto_now_add=True)
    update_time = models.DateTimeField(auto_now=True)
    start_time = models.DateField(default=datetime.now, null=False, verbose_name='入住时间')
    uno = models.IntegerField(null=False, default=0, verbose_name='用户号')
    rno = models.IntegerField(null=False, default=0, verbose_name='用户号')
    id_card = models.CharField(null=False, default='', max_length=18, verbose_name='身份证号')

    @classmethod
    def create_register(cls, start_time, uno, rno, id_card):
        register = cls(start_time=start_time, uno=uno, rno=rno, id_card=id_card)
        register.save()
        return register

    class Meta:
        db_table = "register"
        verbose_name = "入住房间登记"
        verbose_name_plural = verbose_name


count = 1


def set_flow():
    global count
    base_code = datetime.now().strftime('%Y%m%d%H%M%S')
    # order_ = ''
    if count > 100:
        count = 1
        # id = int(id) % 100
    count += 1
    count_str = str(count).zfill(2)
    order_ = base_code+count_str
    return order_


class OrderInformation(models.Model):
    """ 订单表信息 """
    ono = models.CharField(default=set_flow(), max_length=128)
    is_delete = models.IntegerField(default=0)
    create_time = models.DateTimeField(auto_now_add=True)
    update_time = models.DateTimeField(auto_now=True)
    uno = models.IntegerField(null=False, default=0, verbose_name='用户号')
    rno = models.IntegerField(null=False, default=0, verbose_name='房间号')
    num = models.IntegerField(default=1, verbose_name='商品数量')
    start_time = models.DateField(default=datetime.now, null=False, verbose_name='入住时间')
    end_time = models.DateField(default=datetime.now, null=False, verbose_name='退房时间')
    price = models.FloatField(default=0, verbose_name='消费金额')

    class Meta:
        db_table = "order_info"
        verbose_name = "订单信息表"
        verbose_name_plural = verbose_name


class COrder(models.Model):
    """ 订单中商品信息 """
    is_delete = models.IntegerField(default=0)
    create_time = models.DateTimeField(auto_now_add=True)
    update_time = models.DateTimeField(auto_now=True)
    order_info_no = models.ForeignKey('OrderInformation', verbose_name='订单信息表', on_delete=models.CASCADE)
    commodity = models.ForeignKey('CommodityInfo', verbose_name='用户购买的商品', on_delete=models.CASCADE)
    c_good_num = models.IntegerField(default=1)

    class Meta:
        db_table = "commodity_order"
        verbose_name = "订单中商品信息"
        verbose_name_plural = verbose_name


class ROrder(models.Model):
    """ 订单中房间信息 """
    is_delete = models.IntegerField(default=0)
    create_time = models.DateTimeField(auto_now_add=True)
    update_time = models.DateTimeField(auto_now=True)
    order_info_no = models.ForeignKey('OrderInformation', verbose_name='订单信息表', on_delete=models.CASCADE)
    room = models.ForeignKey('RoomInfo', verbose_name='用户订购房间', on_delete=models.CASCADE)

    class Meta:
        db_table = "room_order"
        verbose_name = "订单中房间信息"
        verbose_name_plural = verbose_name
