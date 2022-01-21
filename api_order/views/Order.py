import datetime

from django.db.models import Q
from rest_framework import status
from rest_framework.decorators import action
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from api_account.serializers import AccountCheckoutSerializer
from api_base.views import BaseViewSet
from api_beer.models import Beer, Cart, BeerDiscount
from api_beer.serializers import ListBeerSerializer
from api_order.models import OrderDetail, OrderStatus, Order, Progress
from api_order.serializers import OrderCheckoutSerializer, OrderSerializer, OrderHistorySerializer, ProgressSerializer
from api_order.services import OrderService
from api_account.models import Account


class OrderViewSet(BaseViewSet):
    permission_classes = [IsAuthenticated]
    serializer_class = OrderSerializer
    queryset = Beer.objects.all()

    def create(self, request, *args, **kwargs):
        order_status = OrderStatus.objects.filter(name='PENDING').values('id').first()
        account = request.user
        dataProgress = {"order_status": order_status['id']}
        account = Account.objects.filter(username=account.username).values('id').first()
        request.data['account'] = account['id']
        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid(raise_exception=True):
            order = serializer.save()
            dataProgress["order"] = order.id
            progress = ProgressSerializer(data=dataProgress)
            if progress.is_valid(raise_exception=True):
                progress.save()
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
                        discount = {'discount_percent': 0}
                    order_detail.append(OrderDetail(amount=cart[0], price=price,
                                                    discount_percent=discount['discount_percent'], beer=beer, order=order))
                OrderDetail.objects.bulk_create(order_detail)
                Cart.objects.filter(account=account).delete()
                return Response({"details": serializer.data}, status=status.HTTP_200_OK)
        return Response({"details": "Cannot create new order record"}, status=status.HTTP_400_BAD_REQUEST)

    @action(detail=False, methods=['get'], permission_classes=[IsAuthenticated])
    def checkout(self, request, *args, **kwargs):
        account = request.user
        detail_user = AccountCheckoutSerializer(account)
        res_data = {"User": detail_user.data}
        carts = Cart.objects.filter(account=account)
        carts = OrderCheckoutSerializer(carts, many=True)
        res_data["cart"] = carts.data

        return Response(res_data, status=status.HTTP_200_OK)


