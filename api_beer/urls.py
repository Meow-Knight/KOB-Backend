from rest_framework import routers

from api_beer.views import CreateProducerViewSet

app_name = 'api_beer'
router = routers.SimpleRouter(trailing_slash=True)
router.register(r'producer', CreateProducerViewSet, basename='producer')

urlpatterns = router.urls
