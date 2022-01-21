from rest_framework import routers
from api_order.views import OrderViewSet, ProgressViewSet

app_name = 'api_order'
router = routers.SimpleRouter(trailing_slash=True)
router.register(r'progress', ProgressViewSet, basename='progress')
router.register(r'', OrderViewSet, basename='order')
urlpatterns = router.urls
