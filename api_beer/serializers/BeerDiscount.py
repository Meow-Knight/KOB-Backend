from rest_framework import serializers

from api_beer.models import BeerDiscount
from api_beer.serializers import DropdownBeerSerializer


class BeerDiscountSerializer(serializers.ModelSerializer):
    class Meta:
        model = BeerDiscount
        fields = '__all__'


class SimplestBeerDiscountSerializer(serializers.ModelSerializer):
    beer = DropdownBeerSerializer()

    class Meta:
        model = BeerDiscount
        fields = ('id', 'discount_percent', 'beer')
