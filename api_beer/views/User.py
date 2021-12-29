from rest_framework import status
from rest_framework.permissions import IsAdminUser, IsAuthenticated
from rest_framework.response import Response

from api_beer.serializers import UserSerializer, ListUserSerializer
from api_beer.models import User
from api_base.views import BaseViewSet


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
        user = User(first_name=data['first_name'], last_name=data['last_name'], address=data['address'],
                    delivery_address=data['delivery_address'], phone=data['phone'], age=data['age'], account=account)
        user.save()

        return Response({"details": "add success"}, status=status.HTTP_200_OK)

    def list(self, request, *args, **kwargs):
        query_set = User.objects
        search_query = request.query_params.get("q", "")
        query_set = query_set.filter(first_name__icontains=search_query)
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
