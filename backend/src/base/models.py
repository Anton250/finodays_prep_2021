from django.db import models
import json

ECO_CLASSES = {
    'euro1': 1.0,
    'euro2': 1.0,
    'euro3': 1.0,
    'euro4': 1.0,
    'euro5': 1.0,
    'euro6': 1.0,
    'electro': 1.0,
    'hybrid': 1.0,
}


class Setting(models.Model):
    eco_class_coeffs = models.TextField(default=json.dumps(ECO_CLASSES))
    car_discount = models.FloatField(default=0)
    flat_discount = models.FloatField(default=0)
