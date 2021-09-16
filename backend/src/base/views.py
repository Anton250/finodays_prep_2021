from src.base.models import Setting
from src.base.serializers import SettingSerializer
from rest_framework import viewsets, mixins

class SettingViewSet(mixins.RetrieveModelMixin, mixins.UpdateModelMixin, viewsets.GenericViewSet):
    serializer_class = SettingSerializer
    queryset = Setting.objects.all()
