from api_beer.serializers import BeerSerializer, ListBeerSerializer
from api_beer.models import Beer
from api_base.views import BaseViewSet


class BeerViewSet(BaseViewSet):
    serializer_class = BeerSerializer
    queryset = Beer.objects.all()
    serializer_map = {
        "list": ListBeerSerializer
    }

