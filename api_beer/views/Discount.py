from rest_framework.permissions import IsAdminUser
from api_beer.serializers import DiscountSerializer, DateDiscountSerializer
from rest_framework import status
from django.db.models import Q

from api_base.views import BaseViewSet
from api_beer.models import Discount, BeerDiscount, Beer
from rest_framework.response import Response


class DiscountViewSet(BaseViewSet):
    permission_classes = [IsAdminUser]
    serializer_class = DiscountSerializer
    queryset = Discount.objects.all()

    def create(self, request, *args, **kwargs):
        serializer = DiscountSerializer(data=request.data)
        is_time_existed = Discount.objects.filter(start_date=request.data.get('start_date'),
                                                  end_date=request.data.get('end_date')).exists()
        if is_time_existed:
            return Response({"details": "Time is duplicated"}, status=status.HTTP_400_BAD_REQUEST)
        if serializer.is_valid(raise_exception=True):
            serializer.save()
            instance_discount = Discount.objects.get(name=request.data.get('name'))
            beer_ids = request.data.get("beer_ids")
            for id_beer in beer_ids:
                print(id_beer)
                instance_beer = Beer.objects.get(id=id_beer)
                b = BeerDiscount(discount_percent=request.data.get('discount_percent'), beer=instance_beer, discount=instance_discount)
                b.save()
            return Response({"details": serializer.data}, status=status.HTTP_200_OK)
        return Response({"details": "Cannot create new beer discount record"}, status=status.HTTP_400_BAD_REQUEST)

    def update(self, request, pk, *args, **kwargs):
        partial = kwargs.pop('partial', False)
        instance = self.get_object()
        is_time_existed = Discount.objects.filter(start_date=request.data.get('start_date'),
                                                  end_date=request.data.get('end_date'),
                                                  id__lt=pk).exists()
        if is_time_existed:
            return Response({"details": "Time is duplicate"})
        serializer = self.get_serializer(instance, data=request.data, partial=partial)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        instance_discount = Discount.objects.get(id=pk)
        BeerDiscount.objects.filter(discount_id=pk).delete()
        for id_beer in request.data.get('beer_ids'):
            print(id_beer)
            instance_beer = Beer.objects.get(id=id_beer)
            b = BeerDiscount(discount_percent=request.data.get('discount_percent'),
                             beer=instance_beer, discount=instance_discount)
            b.save()
        return Response({"details": serializer.data}, status=status.HTTP_200_OK)
