import datetime
from typing import Dict, Union, Any

from django.db.models import Q
from rest_framework import status
from rest_framework.decorators import action
from rest_framework.utils.serializer_helpers import ReturnDict

from api_order.models import OrderDetail, OrderStatus, Order
from api_order.serializers import OrderCheckoutSerializer, OrderSerializer, OrderHistorySerializer
from rest_framework.response import Response
from api_order.serializers import ProgressSerializer, ListProgressSerializer, RetrieveProgressSerializer
from api_base.views import BaseViewSet
from api_order.models import Progress
from api_order.services import OrderService
from rest_framework.permissions import IsAdminUser, IsAuthenticated


class ProgressViewSet(BaseViewSet):
    permission_classes = [IsAuthenticated]
    serializer_class = ProgressSerializer
    queryset = Progress.objects.all()
    permission_map = {
        "create": []
    }

    def create(self, request, *args, **kwargs):
        progress = {"order_status": request.data['order_status'], "order": request.data['order']}
        progress = ProgressSerializer(data=progress)
        filter = Progress.objects.filter(order_id=request.data['order']).values('order_status').order_by('order_status')\
            .last()

        if filter:
            if ((filter['order_status'] == 1) & (request.data['order_status'] == 2)) or \
                    ((filter['order_status'] == 1) & (request.data['order_status'] == 5)):
                if progress.is_valid(raise_exception=True):
                    progress.save()
                    return Response(progress.data, status=status.HTTP_200_OK)
            if ((filter['order_status'] == 2) & (request.data['order_status'] == 3)) or \
                    ((filter['order_status'] == 3) & (request.data['order_status'] == 4)):
                if progress.is_valid(raise_exception=True):
                    progress.save()
                    return Response(progress.data, status=status.HTTP_200_OK)
            if filter['order_status'] == 5:
                return Response({"detail": 'This order is canceled'}, status=status.HTTP_400_BAD_REQUEST)

        return Response({"detail": 'invalid status order'}, status=status.HTTP_400_BAD_REQUEST)

    @action(detail=False, methods=['post'], permission_classes=[])
    def user_create(self, request, *args, **kwargs):
        progress = {"order_status": request.data['order_status'], "order": request.data['order']}
        progress = ProgressSerializer(data=progress)
        filter = Progress.objects.filter(order_id=request.data['order']).values('order_status').order_by('order_status')\
            .last()
        if filter:
            if (filter['order_status'] == 1) & (request.data['order_status'] == 5):
                if progress.is_valid(raise_exception=True):
                    progress.save()
                    return Response(progress.data, status=status.HTTP_200_OK)
            if ((filter['order_status'] == 4) & (request.data['order_status'] == 7)) or \
                    ((filter['order_status'] == 4) & (request.data['order_status'] == 6)):
                if progress.is_valid(raise_exception=True):
                    progress.save()
                    return Response(progress.data, status=status.HTTP_200_OK)
            if filter['order_status'] == 5:
                return Response({"detail": 'This order is canceled'}, status=status.HTTP_400_BAD_REQUEST)

        return Response({"detail": 'invalid status order'}, status=status.HTTP_400_BAD_REQUEST)

    @action(detail=False, methods=['get'], permission_classes=[])
    def user_progress(self, request, *args, **kwargs):
        order = request.query_params.get("order", "")
        progress = Progress.objects.filter(order__id=order)
        progress = RetrieveProgressSerializer(progress, many=True)
        res_data = {'progress': progress.data}
        order = Order.objects.filter(id=order)
        order = OrderHistorySerializer(order, many=True)
        res_data['order'] = order.data
        return Response(res_data, status=status.HTTP_200_OK)

    @action(detail=False, methods=['get'], permission_classes=[IsAuthenticated])
    def order_history(self, request, *args, **kwargs):
        account = request.user
        status_query = request.query_params.get("status", "")
        res_data = {'order_status': status_query}
        orders = Progress.objects.filter(Q(order__account=account.id) & Q(order_status__name__icontains=status_query)) \
            .values('order')
        order = Order.objects.filter(id__in=orders)
        order = OrderHistorySerializer(order, many=True)
        res_data["orders"] = order.data
        return Response(res_data, status=status.HTTP_200_OK)

    # @action(detail=False, methods=['get'], permission_classes=[IsAuthenticated])
    # def status(self, request, *args, **kwargs):
    #     account = request.user
    #     status_query = request.query_params.get("status", "")
    #     res_data = {'order_status': status_query}
    #     orders = Progress.objects.filter(Q(order__account=account.id) & Q(order_status__name__icontains=status_query))\
    #         .values('order')
    #     order = Order.objects.filter(id__in=orders)
    #     order = OrderHistorySerializer(order, many=True)
    #     res_data["orders"] = order.data
    #
    #     return Response(res_data, status=status.HTTP_200_OK)

    @action(methods=['put'], detail=False, url_path="admin_change_order_status")
    def ad_change_order_status(self, request):
        user = request.user
        pk = request.data["id"]
        order = Order.objects.filter(pk=pk)
        key_change = request.data.get("key_change")
        if order.exists():
            res = OrderService.change_order_status(order.first(), key_change, user.role.name)
            if res is not None:
                return Response({"detail": res}, status=status.HTTP_200_OK)
        return Response({"detail": "Order is not exists"}, status=status.HTTP_404_NOT_FOUND)

    @action(methods=['put'], detail=False, url_path='admin_cancel_order')
    def admin_cancel_order(self, request):
        pk = request.data.get("id")
        order = Order.objects.filter(pk=pk)
        res = OrderService.cancel_order(order)
        if res is not None:
            return Response({"detail": res}, status=status.HTTP_200_OK)
        return Response({"detail": 'Order is not exists'}, status=status.HTTP_404_NOT_FOUND)