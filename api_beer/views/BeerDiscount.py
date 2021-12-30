from rest_framework.permissions import IsAdminUser
from api_beer.serializers import BeerDiscountSerializer

from api_base.views import BaseViewSet
from api_beer.models import BeerDiscount


class BeerDiscountViewSet(BaseViewSet):
    permission_classes = [IsAdminUser]
    serializer_class = BeerDiscountSerializer
    queryset = BeerDiscount.objects.all()
