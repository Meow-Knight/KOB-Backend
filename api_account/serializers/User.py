from rest_framework import serializers

from api_account.models import User, Account


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

    # def to_internal_value(self, data):
    #     default_return_value = super(EditUserSerializer, self).to_internal_value(data)
    #     Account.objects.filter(id = 223).update(field1 = 2)
    #     return default_return_value


class ListUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = '__all__'
        depth = 1