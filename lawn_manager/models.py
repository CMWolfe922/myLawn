from django.db import models
from django.contrib.gis.db import models as gis_models

class Place(gis_models.Model):
    name = models.CharField(max_length=100)
    location = models.PointField()