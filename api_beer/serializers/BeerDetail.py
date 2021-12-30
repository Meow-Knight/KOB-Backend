from rest_framework import serializers

from api_beer.models import Beer, BeerPhoto
import json


class BeerDetailSerializer(serializers.ModelSerializer):
    # name = serializers.CharField(source='beer.name')
    # alcohol_concentration = serializers.FloatField(source='beer.alcohol_concentration')
    # capacity = serializers.CharField(source='beer.capacity')
    # origin_nation = serializers.CharField(source='beer.origin_nation.name')
    # price = serializers.FloatField(source='beer.price')
    # bottle_amount = serializers.IntegerField(source='beer.bottle_amount')
    # describe = serializers.CharField(source='beer.describe')
    # producer = serializers.CharField(source='beer.producer.name')
    # beer_unit = serializers.CharField(source='beer.beer_unit.name')
    # beer_id = serializers.CharField(source="beer.id")

    class Meta:
        model = Beer
        # fields = ['beer_id', 'link', 'name', 'alcohol_concentration', 'capacity', 'origin_nation',
        #           'price', 'bottle_amount', 'describe', 'producer', 'beer_unit']
        fields = '__all__'
        depth = 1

    def to_representation(self, instance):
        data = super(BeerDetailSerializer, self).to_representation(instance)
        beer_id = data['id']
        photos = BeerPhoto.objects.filter(beer_id=beer_id).values('link')
        if photos:
            data["photos"] = list(photos)
        return data


# class BeerRelatedSerializer(serializers.ModelSerializer):
#
#     class Meta:
#         model = Beer
#         # fields = ['beer_id', 'link', 'name', 'alcohol_concentration', 'capacity', 'origin_nation',
#         #           'price', 'bottle_amount', 'describe', 'producer', 'beer_unit']
#         fields = '__all__'
#         depth = 1
#
#     def to_representation(self, instance):
#         data = super(BeerRelatedSerializer, self).to_representation(instance)
#         beer_id = data['id']
#         photos = BeerPhoto.objects.filter(beer_id=beer_id).values('link')
#         if photos:
#             data["photos"] = list(photos)
#         beer = Beer.objects.filter(name__startswith=data['name'][:5])[:5]
#         data["beer_related"] = list(beer)
#         return data


