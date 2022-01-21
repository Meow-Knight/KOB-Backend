from rest_framework import serializers

from api_order.models import OrderDetail, Order
from api_beer.models import Cart, Beer, BeerPhoto, BeerDiscount
from api_beer.serializers import ItemBeerSerializer
from api_order.serializers import OrderSerializer


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


class OrderDetailBeerSerializer(serializers.ModelSerializer):

    def to_representation(self, instance):
        data = super(OrderDetailBeerSerializer, self).to_representation(instance)
        beers = data['beer']
        beer = Beer.objects.filter(id=beers['id'])
        beer = ItemBeerSerializer(beer, many=True)
        data["beer"] = beer.data
        return data

    class Meta:
        model = OrderDetail
        fields = ('id', 'amount', 'beer',)
        depth = 1


class OrderHistorySerializer(serializers.ModelSerializer):

    def to_representation(self, instance):
        data = super(OrderHistorySerializer, self).to_representation(instance)
        order_detail = data['order_detail']
        data['order_detail'] = []
        for i in order_detail:
            order_details = OrderDetail.objects.filter(id=i['id'])
            order = OrderDetailBeerSerializer(order_details, many=True)
            if not data['order_detail']:
                data["order_detail"] = order.data
            else:
                data["order_detail"].append(order.data)
        return data

    class Meta:
        model = Order
        fields = ('id', 'total_price', 'total_discount',
                  'shipping_address', 'shipping_phone', 'done_at',
                  'order_detail')
        depth = 1

