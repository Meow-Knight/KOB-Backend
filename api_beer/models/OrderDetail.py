from django.db import models

from api_base.models import TimeStampedModel
from api_beer.models import Order, Beer


class OrderDetail(TimeStampedModel):
    amount = models.IntegerField()
    price = models.FloatField(null=True, blank=True)
    discount = models.IntegerField(null=True, blank=True)
    beer = models.ForeignKey(Beer, on_delete=models.CASCADE, related_name="order_detail")
    order = models.ForeignKey(Order, null=True, blank=True, on_delete=models.SET_NULL, related_name="order_detail")

    class Meta:
        db_table = "order_detail"
