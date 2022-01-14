from rest_framework import serializers

from api_account.models import User, Account
from api_account.serializers import AccountInfoSerializer


class UserSerializer(serializers.ModelSerializer):

    class Meta:
        model = User
        fields = ['address', 'phone', 'age']


class EditUserSerializer(serializers.ModelSerializer):
    first_name = serializers.CharField(source='user.account.first_name')
    last_name = serializers.CharField(source='user.account.last_name')
    address = serializers.CharField(source='user.address')
    phone = serializers.CharField(source='user.phone')
    age = serializers.IntegerField(source='user.age')

    class Meta:
        model = User
        fields = ['first_name', 'last_name', 'address', 'phone', 'age']


class ListUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = '__all__'
        depth = 1


class UserViewCheckoutSerializer(serializers.ModelSerializer):
    first_name = serializers.CharField(source='account.first_name')
    last_name = serializers.CharField(source='account.last_name')
    email = serializers.CharField(source='account.email')

    class Meta:
        model = User
        fields = ['address', 'phone', 'age', 'first_name', 'last_name', 'email']
