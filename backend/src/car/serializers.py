from rest_framework import serializers
from src.car.models import Brand, Model, Modification, Generation

class BrandSerializer(serializers.ModelSerializer):
    class Meta:
        fields = ['id', 'name']
        model = Brand

class ModelSerializer(serializers.ModelSerializer):
    class Meta:
        fields = ['id', 'name']
        model = Model

class GenerationSerializer(serializers.ModelSerializer):
    class Meta:
        fields = ['id', 'name']
        model = Generation

class ModificationSerializer(serializers.ModelSerializer):
    class Meta:
        fields = ['id', 'name']
        model = Modification

class PriceSerializer(serializers.Serializer):
    year = serializers.IntegerField()
    pts = serializers.ChoiceField(choices=[0, 1])
    owners_count = serializers.IntegerField()
    mileage = serializers.FloatField()
