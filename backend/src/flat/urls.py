from django.conf.urls import url, include
from rest_framework import routers
from src.flat.views import FlatViewSet


router = routers.DefaultRouter()
router.register(r'flat', FlatViewSet, basename='Flat')


urlpatterns = [
    url(r'^', include(router.urls)),
]
