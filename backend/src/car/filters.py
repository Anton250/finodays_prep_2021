from django_filters.rest_framework import (
    FilterSet,
)
from src.car.models import Model, Generation, Modification

class ModelFilterSet(FilterSet):
    class Meta:
        fields = ['brand_id']
        model = Model

class GenerationFilterSet(FilterSet):
    class Meta:
        fields = ['model_id']
        model = Generation

class ModificationFilterSet(FilterSet):
    class Meta:
        fields = ['generation_id']
        model = Modification      
