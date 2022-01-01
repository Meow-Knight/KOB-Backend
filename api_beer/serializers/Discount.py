from rest_framework import serializers
from api_beer.models import Discount, Beer
from api_beer.serializers import ItemBeerSerializer
from django.db import models


class DiscountSerializer(serializers.ModelSerializer):
    class Meta:
        model = Discount
        fields = ('name', 'start_date', 'end_date')

    # def update(self, instance):
    #     print(instance.name)



class DateDiscountSerializer(serializers.ModelSerializer):
    class Meta:
        model = Discount
        fields = ('start_date', 'end_date')


class DiscountWithItemBeerSerializer(serializers.ModelSerializer):
    def to_representation(self, instance):
        data = super(DiscountWithItemBeerSerializer, self).to_representation(instance)
        discount_id = data['id']
        beers = Beer.objects.filter(beer_discount__discount_id=discount_id)
        if beers.exists():
            item_beer_serializer = ItemBeerSerializer(beers, many=True)
            data['beers'] = item_beer_serializer.data
        return data

    class Meta:
        model = Discount
        fields = ('id', 'name', 'start_date', 'end_date')
