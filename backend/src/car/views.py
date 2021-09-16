from src.car.filters import GenerationFilterSet, ModelFilterSet, ModificationFilterSet
import pandas as pd
from src.car.converter import ValuesGetter
from rest_framework import viewsets
from rest_framework.response import Response
from rest_framework.decorators import action
from xgboost import XGBRegressor
from src.car.models import Brand, Model, Modification, Generation
from src.car.serializers import BrandSerializer, ModelSerializer, ModificationSerializer, GenerationSerializer, PriceSerializer


class BrandViewSet(viewsets.ReadOnlyModelViewSet):
    serializer_class = BrandSerializer
    queryset = Brand.objects.all()

class ModelViewSet(viewsets.ReadOnlyModelViewSet):
    serializer_class = ModelSerializer
    queryset = Model.objects.all()
    filterset_class = ModelFilterSet

class GenerationViewSet(viewsets.ReadOnlyModelViewSet):
    serializer_class = GenerationSerializer
    queryset = Generation.objects.all()
    filterset_class = GenerationFilterSet

class ModificationViewSet(viewsets.ReadOnlyModelViewSet):
    serializer_class = ModificationSerializer
    queryset = Modification.objects.all()
    filterset_class = ModificationFilterSet

    @action(detail=True, methods=['get'])
    def price(self, request, pk=None):
        modification = self.get_object()
        data = PriceSerializer(data=request.query_params)
        data.is_valid(raise_exception=True)
        data = data.validated_data
        rgs = XGBRegressor()
        rgs.load_model('cars.json')
        val_getter = ValuesGetter()
        gen = modification.generation
        model = gen.model
        brand = model.brand
        data_for_prediction = pd.DataFrame(columns=[
                'brand', 'year', 'engine_power', 'fuel_type', 'wheel', 'body_type',
                'pts', 'drive', 'transmission', 'engine_volume', 'owners_count',
                'mileage', 'height', 'length', 'doors_count', 'width', 'wheel_base',
                'cylinders_count'
            ], 
            data=[
                (
                    val_getter.get_brand(brand.name), 
                    data['year'], 
                    modification.engine_power, 
                    val_getter.get_fuel_type(modification.fuel_type), 
                    val_getter.get_wheel(modification.wheel), 
                    val_getter.get_body_type(model.body_type),
                    data['pts'],
                    val_getter.get_drive(modification.drive),
                    val_getter.get_transmission(modification.transmission),
                    modification.engine_volume,
                    data['owners_count'],
                    data['mileage'],
                    modification.height,
                    modification.length,
                    model.doors_count,
                    modification.width,
                    modification.wheel_base,
                    modification.cylinders_count,
                )
            ]
        )
        return Response(
            {
                'price': round(rgs.predict(data_for_prediction)[0]),
                'eco_class': modification.eco,
            }
        )
