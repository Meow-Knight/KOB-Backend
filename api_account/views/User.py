from rest_framework import status
from rest_framework.permissions import IsAdminUser, IsAuthenticated, AllowAny
from rest_framework.response import Response

from api_account.serializers import UserSerializer, ListUserSerializer, EditUserSerializer
from api_account.models import Account
from api_base.views import BaseViewSet
from rest_framework.decorators import action


class UserViewSet(BaseViewSet):
    permission_classes = [IsAdminUser]
    serializer_class = UserSerializer
    queryset = Account.objects.all()
    serializer_map = {
        "list": ListUserSerializer,
        "retrieve": ListUserSerializer
    }
    permission_map = {
        "retrieve": [IsAuthenticated]
    }

    def create(self, request, *args, **kwargs):
        response = {'message': 'Create function is not offered in this path.'}
        return Response(response, status=status.HTTP_403_FORBIDDEN)

    def update(self, request, *args, **kwargs):
        response = {'message': 'Update function is not offered in this path.'}
        return Response(response, status=status.HTTP_403_FORBIDDEN)

    def list(self, request, *args, **kwargs):
        query_set = Account.objects
        search_query = request.query_params.get("q", "")
        query_set = query_set.filter(first_name__icontains=search_query)
        sort_query = request.query_params.get("sort")
        if sort_query:
            try:
                if sort_query.startswith("-"):
                    Account._meta.get_field(sort_query[1:])
                else:
                    Account._meta.get_field(sort_query)
                query_set = query_set.order_by(sort_query)

            except:
                pass

        self.queryset = query_set
        return super().list(request, *args, **kwargs)

    @action(detail=False, methods=['put'], permission_classes=[IsAuthenticated])
    def edit(self, request, *args, **kwargs):
        account = request.user
        instance = self.queryset.get(username=account)
        serializer = self.serializer_class(instance, data=request.data, partial=True)
        serializer.is_valid(raise_exception=True)
        self.perform_update(serializer)
        return Response(serializer.data)

    @action(detail=False, methods=['get'], permission_classes=[IsAuthenticated])
    def detail_user(self, request, *args, **kwargs):
        account = request.user
        user = self.queryset.get(username=account)
        detail_user = ListUserSerializer(user)
        res_data = {"user": detail_user.data}
        return Response(res_data, status=status.HTTP_200_OK)



