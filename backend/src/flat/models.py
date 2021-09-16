from django.db import models

class MacroRegion(models.Model):
    name = models.CharField(max_length=128)
    code = models.CharField(max_length=256)

class Region(models.Model):
    name = models.CharField(max_length=128)
    code = models.CharField(max_length=256)
    macro_region = models.ForeignKey(MacroRegion, on_delete=models.PROTECT)
