
import datetime
from rest_framework import serializers

from api_beer.models import Cart, Beer, BeerPhoto, BeerDiscount
from api_order.models import Order
from api_beer.serializers import ItemBeerSerializer


class OrderCheckoutSerializer(serializers.ModelSerializer):

    def to_representation(self, instance):
        data = super(OrderCheckoutSerializer, self).to_representation(instance)
        beer = data['beer']
        beer = Beer.objects.filter(id=beer['id'])
        beer = ItemBeerSerializer(beer, many=True)
        data["beer"] = beer.data

        return data

    class Meta:
        model = Cart
        fields = ('id', 'amount', 'beer',)
        depth = 1


class OrderSerializer(serializers.ModelSerializer):
    class Meta:
        model = Order
        fields = '__all__'

