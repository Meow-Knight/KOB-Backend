from rest_framework import serializers

from api_account.serializers import UserWithNameSerializer
from api_beer.models import Order, Cart, Beer, OrderStatus
from api_beer.serializers import ItemBeerSerializer


class OrderSerializer(serializers.ModelSerializer):
    class Meta:
        model = Order
        fields = '__all__'


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


class ListOrderWithUserSerializer(serializers.ModelSerializer):
    user = UserWithNameSerializer()

    def to_representation(self, instance):
        data = super(ListOrderWithUserSerializer, self).to_representation(instance)
        order_status = OrderStatus.objects.get(pk=data.get('order_status'))
        data['order_status'] = order_status.name
        return data

    class Meta:
        model = Order
        fields = ['id', 'total_price', 'total_discount', 'shipping_address', 'shipping_phone', 'done_at', 'order_status', 'user']
