from django.core.validators import MinValueValidator, MaxValueValidator
from django.db import models

from api_base.models import TimeStampedModel
from api_beer.models import Beer, Discount


class BeerDiscount(TimeStampedModel):
    discount_percent = models.IntegerField(validators=[MinValueValidator(1), MaxValueValidator(100)])
    beer = models.ForeignKey(Beer, on_delete=models.CASCADE, related_name="beer_discount")
    discount = models.ForeignKey(Discount, on_delete=models.CASCADE, related_name="beer_discount")

    class Meta:
        db_table = "beer_discount"
        ordering = ('created_at',)
        unique_together = ('beer', 'discount',)
