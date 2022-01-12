from django.db import models

from api_base.models import TimeStampedModel
from api_account.models import User
from api_beer.models import Beer


class Cart(TimeStampedModel):
    cart_time = models.DateField()
    amount = models.IntegerField()
    beer = models.ForeignKey(Beer, on_delete=models.CASCADE, related_name="cart")
    user = models.ForeignKey(User, null=True, blank=True, on_delete=models.SET_NULL, related_name="cart")

    class Meta:
        db_table = "cart"
        ordering = ('cart_time',)
