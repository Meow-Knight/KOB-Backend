from rest_framework import serializers

from api_beer.models import BeerDiscount


class BeerDiscountSerializer(serializers.ModelSerializer):
    class Meta:
        model = BeerDiscount
        fields = ('discount_percent', 'beer', 'discount')


