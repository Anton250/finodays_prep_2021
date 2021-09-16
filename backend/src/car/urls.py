from django.conf.urls import url, include
from rest_framework import routers
from src.car.views import BrandViewSet, ModelViewSet, GenerationViewSet, ModificationViewSet


router = routers.DefaultRouter()
router.register(r'brand', BrandViewSet, basename='Brand')
router.register(r'model', ModelViewSet, basename='Model')
router.register(r'generation', GenerationViewSet, basename='Generation')
router.register(r'modification', ModificationViewSet, basename='Modification')


urlpatterns = [
    url(r'^', include(router.urls)),
]
