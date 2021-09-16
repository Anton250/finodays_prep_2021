import json
from src.base.models import Setting
from rest_framework import serializers

class EcoClassCoeffsSerializer(serializers.Serializer):
    euro1 = serializers.FloatField(default=1.0)
    euro2 = serializers.FloatField(default=1.0)
    euro3 = serializers.FloatField(default=1.0)
    euro4 = serializers.FloatField(default=1.0)
    euro5 = serializers.FloatField(default=1.0)
    euro6 = serializers.FloatField(default=1.0)
    electro = serializers.FloatField(default=1.0)
    hybrid = serializers.FloatField(default=1.0)

class SettingSerializer(serializers.ModelSerializer):
    eco_class_coeffs = serializers.JSONField()
    class Meta:
        fields = '__all__'
        model = Setting

    def to_representation(self, obj):
        data = super().to_representation(obj)
        if isinstance(data['eco_class_coeffs'], str):
            data['eco_class_coeffs'] = json.loads(data['eco_class_coeffs'])
        return data

    def validate(self, attrs):
        eco_data = EcoClassCoeffsSerializer(data=attrs['eco_class_coeffs'])
        eco_data.is_valid(raise_exception=True)
        attrs['eco_class_coeffs'] = json.dumps(eco_data.validated_data)
        return attrs
