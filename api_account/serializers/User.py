from rest_framework import serializers

from api_account.models import Account
from api_account.serializers import AccountInfoSerializer


class UserSerializer(serializers.ModelSerializer):

    class Meta:
        model = Account
        fields = ['address', 'phone', 'age']


class EditUserSerializer(serializers.ModelSerializer):

    class Meta:
        model = Account
        fields = ['first_name', 'last_name', 'address', 'phone', 'age']


class ListUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = Account
        fields = ['first_name', 'last_name', 'address', 'phone', 'age', 'is_staff', ]
        depth = 1


# class UserViewCheckoutSerializer(serializers.ModelSerializer):
#     first_name = serializers.CharField(source='account.first_name')
#     last_name = serializers.CharField(source='account.last_name')
#     email = serializers.CharField(source='account.email')
#
#     class Meta:
#         model = User
#         fields = ['address', 'phone', 'age', 'first_name', 'last_name', 'email']


class UserWithNameSerializer(serializers.ModelSerializer):
    full_name = serializers.SerializerMethodField()

    class Meta:
        model = Account
        fields = ['id', 'full_name']

    def get_full_name(self, obj):
        return '{} {}'.format(obj.account.first_name, obj.account.last_name)

