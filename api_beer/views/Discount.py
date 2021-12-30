from rest_framework import status
from rest_framework.response import Response

from api_account.permissions import AdminPermission
from api_base.views import BaseViewSet
from api_beer.models import Discount
from api_beer.serializers import DiscountSerializer, DetailDiscountSerializer
from api_beer.services import DiscountService


class DiscountViewSet(BaseViewSet):
    permission_classes = [AdminPermission]
    serializer_class = DiscountSerializer
    queryset = Discount.objects.all()
    serializer_map = {
        "retrieve": DetailDiscountSerializer
    }

    def create(self, request, *args, **kwargs):
        validated_data = DiscountService.create(request.data)
        return Response(validated_data, status=status.HTTP_201_CREATED)
