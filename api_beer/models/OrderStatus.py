from django.db import models

from api_base.models import TimeStampedModel


class OrderStatus(TimeStampedModel):
    name = models.CharField(max_length=50, unique=True)

    class Meta:
        db_table = "order_status"
        ordering = ('name',)
