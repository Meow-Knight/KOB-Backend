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

    def to_representation(self, instance):
        data = super(AccountInfoSerializer, self).to_representation(instance)
        data['role'] = instance.role.name

        return data


class GeneralInfoAccountSerializer(serializers.ModelSerializer):
    class Meta:
        model = Account
        exclude = ('password', 'role', 'is_active', 'is_staff', 'is_superuser')


class AccountCheckoutSerializer(serializers.ModelSerializer):

    class Meta:
        model = Account
        fields = ['id', 'address', 'phone', 'age', 'first_name', 'last_name', 'email', 'is_staff']
