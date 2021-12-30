from rest_framework import status
from rest_framework.permissions import IsAdminUser, IsAuthenticated, AllowAny
from rest_framework.response import Response

from api_account.serializers import UserSerializer, ListUserSerializer, AccountInfoSerializer, EditUserSerializer
from api_account.models import User, Account
from api_base.views import BaseViewSet
from rest_framework.decorators import action


class UserViewSet(BaseViewSet):
    permission_classes = [IsAdminUser]
    serializer_class = UserSerializer
    queryset = User.objects.all()
    serializer_map = {
        "list": ListUserSerializer,
        "retrieve": ListUserSerializer
    }
    permission_map = {
        "create": [IsAuthenticated],
        "update": [IsAuthenticated],
        "retrieve": [IsAuthenticated]
    }

    def create(self, request, *args, **kwargs):
        account = request.user
        data = request.data
        user = User(address=data['address'], phone=data['phone'], age=data['age'], account=account)
        user.save()

        return Response({"details": "add success"}, status=status.HTTP_200_OK)

    def list(self, request, *args, **kwargs):
        query_set = User.objects
        search_query = request.query_params.get("q", "")
        query_set = query_set.filter(account__first_name__icontains=search_query)
        sort_query = request.query_params.get("sort")
        if sort_query:
            try:
                if sort_query.startswith("-"):
                    User._meta.get_field(sort_query[1:])
                else:
                    User._meta.get_field(sort_query)
                query_set = query_set.order_by(sort_query)

            except:
                pass

        self.queryset = query_set
        return super().list(request, *args, **kwargs)

    @action(detail=False, methods=['post'], permission_classes=[IsAuthenticated])
    def edit(self, request, *args, **kwargs):
        account = request.user
        instance = self.queryset.get(account=account)
        self.serializer_class = EditUserSerializer
        serializer = self.serializer_class(instance, data=request.data, partial=True)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        Account.objects.filter(id=account.id)\
            .update(first_name=request.data["first_name"], last_name=request.data["last_name"])
        return Response(serializer.data)

    @action(detail=False, methods=['get'], permission_classes=[IsAuthenticated])
    def detail_user(self, request, *args, **kwargs):
        account = request.user
        instance = self.queryset.get(account=account)
        detail_user = UserSerializer(instance)
        res_data = {"user": detail_user.data}
        account = instance.account
        detail_account = AccountInfoSerializer(account)
        res_data["account"] = detail_account.data
        return Response(res_data, status=status.HTTP_200_OK)



