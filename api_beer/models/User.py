from django.db import models

from api_base.models import TimeStampedModel
from api_account.models import Account


class User(TimeStampedModel):
    first_name = models.CharField(max_length=20)
    last_name = models.CharField(max_length=20)
    address = models.TextField()
    delivery_address = models.TextField()
    phone = models.CharField(max_length=20)
    age = models.IntegerField()
    account = models.ForeignKey(Account, on_delete=models.CASCADE, related_name="account_user")

    class Meta:
        db_table = "user"
        ordering = ['last_name', 'first_name']
