from rest_framework import status
from rest_framework.decorators import action
from rest_framework.response import Response

from api_base.views import BaseViewSet
from api_beer.models import Beer, BeerUnit, Producer
from api_beer.serializers import BeerSerializer, ListBeerSerializer, RetrieveBeerSerializer, BeerUnitSerializer, \
    ProducerSerializer
from api_beer.services import BeerService
from django.db.models import Q


class BeerViewSet(BaseViewSet):
    permission_classes = []
    serializer_class = BeerSerializer
    queryset = Beer.objects.all()
    serializer_map = {
        "list": ListBeerSerializer,
        "retrieve": RetrieveBeerSerializer,
    }
    permission_map = {
        "list": [],
        "retrieve": [],
        "homepage": []
    }

    @action(detail=False, methods=['get'])
    def info(self, request, *args, **kwargs):
        return Response("hehe", status=status.HTTP_200_OK)

    def create(self, request, *args, **kwargs):
        images = request.FILES.getlist("images")
        serializer = self.get_serializer(data=request.data)

        if serializer.is_valid(raise_exception=True):
            BeerService.create_beer_with_photos(serializer, images)
            return Response({"details": serializer.data}, status=status.HTTP_200_OK)
        return Response({"details": "Cannot create new beer record"}, status=status.HTTP_400_BAD_REQUEST)

    def list(self, request, *args, **kwargs):
        query_set = Beer.objects
        search_query = request.query_params.get("q", "")
        query_set = query_set.filter(name__icontains=search_query)
        sort_query = request.query_params.get("sort")
        if sort_query:
            try:
                if sort_query.startswith("-"):
                    Beer._meta.get_field(sort_query[1:])
                else:
                    Beer._meta.get_field(sort_query)
                query_set = query_set.order_by(sort_query)
            except:
                pass

        self.queryset = query_set
        return super().list(request, *args, **kwargs)

    @action(detail=False, methods=['get'])
    def homepage(self, request, *args, **kwargs):
        random_amount = int(request.query_params.get("random_amount", "4"))
        response_data = BeerService.get_homepage_data(random_amount)
        return Response(response_data, status=status.HTTP_200_OK)

    def get_queryset(self):
        bottle = self.request.query_params.get("bottle_amount")
        price = self.request.query_params.get("price")
        alcohol = self.request.query_params.get("alcohol")
        name = self.request.query_params.get("name")
        unit_name = self.request.query_params.get("unit")
        producer_name = self.request.query_params.get("producer")
        query_set = Beer.objects
        if name is not None:
            print(1)
            query_set = query_set.filter(Q(name__icontains=name))
        if bottle is not None:
            print(2)
            query_set = query_set.filter(Q(bottle_amount=bottle))
        if alcohol is not None:
            print(3)
            alcohol = alcohol.split(':')
            query_set = query_set.filter(Q(alcohol_concentration__range=(int(alcohol[0]), int(alcohol[1]))))
        if price is not None:
            print(4)
            price = price.split(':')
            query_set = query_set.filter(Q(price__range=(int(price[0]), int(price[1]))))
        if unit_name is not None:
            print(5)
            unit_id = BeerUnitSerializer(BeerUnit.objects.get(name=unit_name)).data.get('id')
            query_set = query_set.filter(Q(beer_unit_id=unit_id))
        if producer_name is not None:
            print(6)
            producer_id = ProducerSerializer(Producer.objects.get(name=producer_name)).data.get('id')
            query_set = query_set.filter(Q(producer_id=producer_id))
        return query_set
