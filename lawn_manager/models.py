from django.contrib.gis.db import models
from django.db import models

class Place(models.Model):
    name = models.CharField(max_length=100)
    location = models.PointField()