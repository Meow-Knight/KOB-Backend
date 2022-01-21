from rest_framework import serializers

from api_account.models import Account


class AccountInfoSerializer(serializers.ModelSerializer):
    first_name = serializers.CharField(read_only=True)
    last_name = serializers.CharField(read_only=True)
    is_staff = serializers.BooleanField(read_only=True)
    username = serializers.CharField(read_only=True)
    email = serializers.CharField(read_only=True)

    class Meta:
        model = Account
        fields = ('first_name', 'last_name', 'username', 'email', 'is_staff')


class GeneralInfoAccountSerializer(serializers.ModelSerializer):
    class Meta:
        model = Account
        exclude = ('password', 'role', 'is_active', 'is_staff', 'is_superuser')


class AccountCheckoutSerializer(serializers.ModelSerializer):

    class Meta:
        model = Account
        fields = ['id', 'address', 'phone', 'age', 'first_name', 'last_name', 'email']
