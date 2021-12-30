from django.db import models

from api_base.models import TimeStampedModel
from api_account.models import Account


class User(TimeStampedModel):
    address = models.TextField()
    phone = models.CharField(max_length=20)
    age = models.IntegerField()
    account = models.ForeignKey(Account, on_delete=models.CASCADE, related_name="account_user")

    class Meta:
        db_table = "user"
