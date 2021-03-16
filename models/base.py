from django.db import models


class BaseManager(models.Manager):
    def get_queryset(self):
        return super().get_queryset().filter(is_active=True)


class BaseModel(models.Model):
    is_active = models.BooleanField(db_index=True, default=True)
    create_time = models.DateTimeField(auto_now_add=True)
    update_time = models.DateTimeField(auto_now=True)

    objects = BaseManager()

    def __str__(self, ):
        return f"User: <id: {self.id}>"

    def __repr__(self, ):
        return self.__str__()

    class Meta:
        abstract = True  # abstract 代表一个抽象类，用它来归纳一些公共属性字段，可以被继承
