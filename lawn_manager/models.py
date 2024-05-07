from django.db import models
from django.contrib.gis.db import models as gis_models

class Place(gis_models.Model):
    name = models.CharField(max_length=100)
    location = models.PointField()


class Lawn(models.Model):
    lawn = models.ForeignKey(Place, on_delete=models.CASCADE)
    size = models.IntegerField()
    price = models.FloatField()
    description = models.TextField()
    image = models.ImageField(upload_to="lawn_images")

    def __str__(self):
        return self.lawn.name + " - " + str(self.size) + " sqft" + " - $" + str(self.price)

class Booking(models.Model):
    lawn = models.ForeignKey(Lawn, on_delete=models.CASCADE)
    date = models.DateField()
    start_time = models.TimeField()
    end_time = models.TimeField()
    customer_name = models.CharField(max_length=100)
    customer_phone = models.CharField(max_length=15)
    customer_email = models.EmailField()

    def __str__(self):
        return self.lawn.name + " - " + str(self.date) + " - " + str(self.start_time) + " to " + str(self.end_time)

class Review(models.Model):
    lawn = models.ForeignKey(Lawn, on_delete=models.CASCADE)
    rating = models.IntegerField()
    comment = models.TextField()

    def __str__(self):
        return self.lawn.name + " - " + str(self.rating) + " stars"

# Path: lawn_manager/admin.py
from django.contrib import admin
from .models import Place, Lawn, Booking, Review

