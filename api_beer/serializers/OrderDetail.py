from rest_framework import serializers

from api_beer.models import OrderDetail
from api_beer.models import Order, Cart, Beer, BeerPhoto, BeerDiscount
from api_beer.serializers import ItemBeerSerializer, OrderSerializer


class OrderDetailSerializer(serializers.ModelSerializer):
    class Meta:
        model = OrderDetail
        fields = '__all__'
        depth = 1


class ListOrderDetailSerializer(serializers.ModelSerializer):
    class Meta:
        model = OrderDetail
        fields = '__all__'
        depth = 1


class OrderHistorySerializer(serializers.ModelSerializer):

    def to_representation(self, instance):
        data = super(OrderHistorySerializer, self).to_representation(instance)
        print(data)
        beer = data['beer']
        beer = Beer.objects.filter(id=beer['id'])
        beer = ItemBeerSerializer(beer, many=True)
        data["beer"] = beer.data
        return data

    class Meta:
        model = OrderDetail
        fields = ('id', 'amount', 'beer',)
        depth = 1
