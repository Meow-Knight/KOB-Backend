from api_beer.serializers import OrderCheckoutSerializer, OrderSerializer, OrderDetailSerializer, OrderHistorySerializer
from api_account.serializers import UserViewCheckoutSerializer
from rest_framework.permissions import AllowAny, IsAuthenticated
from api_base.views import BaseViewSet
from api_beer.models import Beer, Cart, OrderDetail, OrderStatus, Order
from api_account.models import User
from rest_framework.response import Response
from rest_framework.decorators import action
from rest_framework import status
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
        # serializer.data['order_status'] = order_status
        if serializer.is_valid(raise_exception=True):
            order = serializer.save()
            order_detail = []
            account = request.user
            carts = Cart.objects.filter(account=account).values_list('amount', 'beer')
            if carts:
                for cart in carts:
                    beer = Beer.objects.filter(id=cart[1]).first()
                    order_detail.append(OrderDetail(amount=cart[0], beer=beer, order=order))
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
        instance = User.objects.get(account=account)
        detail_user = UserViewCheckoutSerializer(instance)
        res_data = {"User": detail_user.data}
        print(status_query)
        order = Order.objects.filter(Q(user=instance) & Q(order_status__name__icontains=status_query))
        order = OrderSerializer(order, many=True)
        order = list(order.data)
        # print(order[0]['id'])
        res_data["beers"] = []
        # res_data["beers"]["orders"] = []
        for i in range(len(order)):
            order_detail = OrderDetail.objects.filter(order__id=order[i]['id'])
            order_detail = OrderHistorySerializer(order_detail, many=True)
            res_data["beers"].append(order[i])
            res_data["beers"].append(order_detail.data)

        return Response(res_data, status=status.HTTP_200_OK)






