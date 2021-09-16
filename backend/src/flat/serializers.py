from rest_framework import serializers

class AddressSerializer(serializers.Serializer):
    macro_region_name = serializers.CharField()
    street = serializers.CharField()
    street_type =serializers.CharField()
    house = serializers.CharField()
    apartment = serializers.CharField()
    building = serializers.CharField(required=False)
    structure = serializers.CharField(required=False)
    region_name = serializers.CharField(required=False)


class FlatPriceSerializer(serializers.Serializer):
    geo_lat = serializers.DecimalField(decimal_places=8, max_digits=12)
    geo_lon = serializers.DecimalField(decimal_places=8, max_digits=12)
    area = serializers.FloatField()
    rooms = serializers.IntegerField()
    level = serializers.IntegerField()
    levels = serializers.IntegerField()
    building_type = serializers.IntegerField()
