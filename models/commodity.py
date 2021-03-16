from django.db import models
from .base import BaseModel


class CommodityInfo(BaseModel):
    """ 商品表 """
    cno = models.IntegerField(default=1, null=False)
    type = models.CharField(max_length=60, verbose_name='商品类型')
    price = models.FloatField(default=0, null=False, verbose_name='价格')

    @classmethod
    def create_commodity(cls, cno, type, price):
        commodity = cls(
            cno=cno, type=type, price=price
        )
        commodity.save()
        return commodity

    class Meta:
        db_table = "commodity_info"
        verbose_name = "商品信息"
        verbose_name_plural = verbose_name
