from django.db.models import Q
from rest_framework import status
from rest_framework.decorators import action
from rest_framework.permissions import AllowAny
from rest_framework.response import Response

from api_base.views import BaseViewSet
from api_beer.models import Beer
from api_beer.serializers import BeerDetailSerializer, ItemBeerSerializer


class BeerDetailViewSet(BaseViewSet):
    permission_classes = [AllowAny]
    serializer_class = BeerDetailSerializer
    queryset = Beer.objects.all()

    @action(detail=True, methods=['get'], permission_classes=[AllowAny])
    def info(self, request, pk, *args, **kwargs):
        beer = self.get_object()
        beer = BeerDetailSerializer(beer)
        res_data = {"details": beer.data}
        query_set = Beer.objects.filter(Q(producer__name__icontains=beer.data["producer"]["name"]) |
                                        Q(price__range=(beer.data["price"]-50000, beer.data["price"]+50000)) |
                                        Q(name__startswith=beer.data["name"][:5])
                                        ).exclude(id=beer.data["id"]).distinct()[:5]
        query_set = BeerDetailSerializer(query_set, many=True)
        res_data["BeerRelated"] = query_set.data
        return Response(res_data, status=status.HTTP_200_OK)

    @action(detail=False, methods=['get'], permission_classes=[AllowAny])
    def list_beer(self, request, *args, **kwargs):
        queryset = self.filter_queryset(self.get_queryset())
        beer = ItemBeerSerializer(queryset, many=True)
        res_data = {"list_beer": beer.data}
        return Response(res_data, status=status.HTTP_200_OK)



