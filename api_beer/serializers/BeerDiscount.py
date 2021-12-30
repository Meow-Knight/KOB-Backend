from rest_framework import serializers

from api_beer.models import BeerDiscount


class BeerDiscountSerializer(serializers.ModelSerializer):
    class Meta:
        model = BeerDiscount
        fields = '__all__'


class ListBeerDiscountSerializer(serializers.ModelSerializer):
    class Meta:
        model = BeerDiscount
        fields = '__all__'
