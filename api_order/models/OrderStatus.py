from django.db import models
from django.db.models import Manager


class OrderStatus(models.Model):
    objects = Manager
    name = models.CharField(max_length=20)

    class Meta:
        db_table = "order_status"
        ordering = ('id',)
