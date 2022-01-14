from api_beer.serializers import OrderCheckoutSerializer, OrderSerializer, ListBeerSerializer, OrderHistorySerializer
from api_account.serializers import UserViewCheckoutSerializer
from rest_framework.permissions import AllowAny, IsAuthenticated
from api_base.views import BaseViewSet
from api_beer.models import Beer, Cart, OrderDetail, OrderStatus, Order, BeerDiscount
from api_account.models import User
from rest_framework.response import Response
from rest_framework.decorators import action
from rest_framework import status
import datetime
from django.db.models import Q
import string


class OrderViewSet(BaseViewSet):
    permission_classes = [IsAuthenticated]
    serializer_class = OrderSerializer
    queryset = Beer.objects.all()

    def create(self, request, *args, **kwargs):
        order_status = OrderStatus.objects.filter(name='PENDING').values('id').first()
        account = request.user
        user = User.objects.filter(account=account).values('id').first()
        request.data['order_status'] = order_status['id']
        request.data['user'] = user['id']
        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid(raise_exception=True):
            order = serializer.save()
            order_detail = []
            account = request.user
            carts = Cart.objects.filter(account=account).values_list('amount', 'beer')
            if carts:
                for cart in carts:
                    beer = Beer.objects.filter(id=cart[1]).first()
                    beer_price = ListBeerSerializer(beer)
                    price = cart[0] * beer_price['price'].value
                    discount = BeerDiscount.objects.filter(beer=beer,
                                                           discount__start_date__lte=datetime.date.today(),
                                                           discount__end_date__gte=datetime.date.today(),
                                                           discount__is_activate=True).values("discount_percent")
                    if discount.exists():
                        discount = discount.first()
                    else:
                        discount = 0
                    order_detail.append(OrderDetail(amount=cart[0], price=price,
                                                    discount=discount['discount_percent'], beer=beer, order=order))
                OrderDetail.objects.bulk_create(order_detail)
                Cart.objects.filter(account=account).delete()
                return Response({"details": serializer.data}, status=status.HTTP_200_OK)
        return Response({"details": "Cannot create new order record"}, status=status.HTTP_400_BAD_REQUEST)

    @action(detail=False, methods=['get'], permission_classes=[IsAuthenticated])
    def info(self, request, *args, **kwargs):
        account = request.user
        instance = User.objects.get(account=account)
        detail_user = UserViewCheckoutSerializer(instance)
        res_data = {"User": detail_user.data}
        # carts = Cart.objects.filter(account=account).values_list('beer', 'amount')
        carts = Cart.objects.filter(account=account)
        carts = OrderCheckoutSerializer(carts, many=True)
        # if carts:
        res_data["cart"] = carts.data

        return Response(res_data, status=status.HTTP_200_OK)

    @action(detail=False, methods=['get'], permission_classes=[IsAuthenticated])
    def order_history(self, request, *args, **kwargs):
        account = request.user
        status_query = request.query_params.get("status", "")
        user = User.objects.get(account=account)
        order = Order.objects.filter(Q(user=user) & Q(order_status__name__icontains=status_query))
        order = OrderHistorySerializer(order, many=True)
        res_data = {"orders": order.data}

        return Response(res_data, status=status.HTTP_200_OK)






