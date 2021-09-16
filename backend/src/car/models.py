from src.car.utils import get_eco_class
from django.db import models

ECO_CLASSES = {
    'электро': 'electro',
    'гибрид': 'hybrid',
}

class Brand(models.Model):
    name = models.CharField(max_length=256) # brand

class Model(models.Model):
    name = models.CharField(max_length=256) # model
    brand = models.ForeignKey(Brand, on_delete=models.PROTECT, related_name='models')
    body_type = models.CharField(max_length=32) # body_type
    doors_count = models.IntegerField()

class Generation(models.Model):
    name = models.CharField(max_length=128) # generation_to_show
    model = models.ForeignKey(Model, on_delete=models.PROTECT, related_name='generations')

class Modification(models.Model):
    name = models.CharField(max_length=128) # (engine_volume (engine_power л.с.) transmission fuel_type drive)
    engine_power = models.FloatField() # engine_power
    engine_volume = models.FloatField() # engine_volume
    fuel_type =  models.CharField(max_length=32) # fuel_type
    transmission = models.CharField(max_length=32) # transmission
    drive = models.CharField(max_length=32) # drive
    cylinders_count = models.IntegerField() # cylinders_count
    wheel = models.CharField(max_length=32) # wheel
    generation = models.ForeignKey(Generation, on_delete=models.PROTECT, related_name='modifications')
    height = models.FloatField() # height
    length = models.FloatField() # length
    width = models.FloatField() # width
    wheel_base = models.FloatField() # wheel_base
    catalog_link = models.URLField()
    eco_class = models.CharField(max_length=16, null=True, blank=True)

    @property
    def eco(self):
        if self.eco_class is None:
            if self.fuel_type in ECO_CLASSES:
                self.eco_class = ECO_CLASSES[self.fuel_type]
            else:
                self.eco_class = get_eco_class(self.catalog_link).lower().replace(' ', '')
            self.save()   
        return self.eco_class
