from rest_framework import status
from rest_framework.response import Response

from api_beer.serializers import BeerSerializer, ListBeerSerializer
from api_beer.models import Beer
from api_beer.services import BeerService
from api_base.views import BaseViewSet


class BeerViewSet(BaseViewSet):
    serializer_class = BeerSerializer
    queryset = Beer.objects.all()
    serializer_map = {
        "list": ListBeerSerializer
    }

    def create(self, request, *args, **kwargs):
        images = request.FILES.getlist("images")
        serializer = self.get_serializer(data=request.data)

        if serializer.is_valid(raise_exception=True):
            BeerService.create_beer_with_photos(serializer, images)
            return Response({"details": serializer.data}, status=status.HTTP_200_OK)
        return Response({"details": "Cannot create new beer record"}, status=status.HTTP_400_BAD_REQUEST)
