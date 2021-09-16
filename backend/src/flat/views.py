import pandas as pd
from rest_framework.response import Response
from xgboost import XGBRegressor
from src.flat.reestr import AddressWrapper, RosreestrAPIClient
from rest_framework import viewsets
from rest_framework.decorators import action
from src.flat.serializers import AddressSerializer, FlatPriceSerializer

class FlatViewSet(viewsets.ViewSet):
    @action(detail=False, methods=['get'])
    def byaddress(self, request):
        data = AddressSerializer(data=request.query_params)
        data.is_valid(raise_exception=True)
        data = data.validated_data
        address = AddressWrapper(**data)
        client = RosreestrAPIClient()
        flat = client.get_flat_by_address(address)
        floor = flat.get('premisesData', {}).get('premisesFloor') if flat.get('premisesData') else flat.get('parcelData', {}).get('oksFloors') if flat.get('parcelData', {}) else None

        return Response (
            {
                'actualDate': flat['firActualDate'],
                'objectName': flat['objectData']['objectName'],
                'cadNum': flat['objectData']['objectCn'],
                'address': flat['objectData']['objectAddress']['mergedAddress'],
                'region': flat['objectData']['objectAddress']['region'],
                'areaValue': flat.get('parcelData', {}).get('areaValue') or flat.get('premisesData', {}).get('areaValue'),
                'cadCost': {
                    'cost': flat.get('parcelData', {}).get('cadCost'),
                    'date': flat.get('parcelData', {}).get('dateCost'),
                },
                'floor': floor,
            }
        )

    @action(detail=False, methods=['get'])
    def price(self, request):
        data = FlatPriceSerializer(data=request.query_params)
        data.is_valid(raise_exception=True)
        data = data.validated_data
        rgs = XGBRegressor()
        rgs.load_model('flat_without_kitchen_area.json')
        data_for_prediction = pd.DataFrame(
            columns=["geo_lon", "area", "geo_lat", "level", "building_type", "rooms", "levels"],
            data=[
                (data['geo_lon'], data['area'], data['geo_lat'], data['level'], data['building_type'], data['rooms'], data['levels']),
            ]
        )

        return Response(
            {
                'price': round(rgs.predict(data_for_prediction)[0]),
            }
        )
