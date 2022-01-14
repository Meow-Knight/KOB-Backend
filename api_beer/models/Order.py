from django.db import models

from api_base.models import TimeStampedModel
from api_account.models import User
from api_beer.models import OrderStatus


class Order(TimeStampedModel):
    total_price = models.FloatField()
    total_discount = models.FloatField()
    sum_price = models.FloatField()
    shipping_address = models.TextField()
    shipping_phone = models.CharField(max_length=20)
    done_at = models.DateField()
    order_status = models.ForeignKey(OrderStatus, on_delete=models.CASCADE, related_name="order")
    user = models.ForeignKey(User, null=True, blank=True, on_delete=models.SET_NULL, related_name="order")

    class Meta:
        db_table = "order"
        ordering = ('-done_at',)
