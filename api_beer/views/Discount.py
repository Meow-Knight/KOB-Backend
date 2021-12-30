from rest_framework.permissions import IsAdminUser
from api_beer.serializers import DiscountSerializer

from api_base.views import BaseViewSet
from api_beer.models import Discount


class DiscountViewSet(BaseViewSet):
    permission_classes = [IsAdminUser]
    serializer_class = DiscountSerializer
    queryset = Discount.objects.all()
