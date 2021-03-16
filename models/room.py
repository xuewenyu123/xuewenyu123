from django.db import models
from .base import BaseModel


class RoomInfo(BaseModel):
    """ 房间信息 """
    rno = models.IntegerField(default=101, null=False)
    style = models.CharField(max_length=60, verbose_name='房间类型')
    dsc = models.CharField(max_length=255, default='', verbose_name='简介')
    price = models.DecimalField(default=0, max_digits=6, decimal_places=2, null=False, verbose_name='价格')

    @classmethod
    def create_room(cls, rno, style, dsc, price):  # 学院 -- 地址
        info = cls(rno=rno, style=style, dsc=dsc, price=price)
        info.save()
        return info

    class Meta:
        db_table = "room_info"
        verbose_name = "房间信息"
        verbose_name_plural = verbose_name
