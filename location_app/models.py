from django.db import models


class Location(models.Model):
    city = models.CharField(max_length=128)
    address = models.CharField(max_length=128)
    postcode = models.CharField(max_length=16)

    lat = models.FloatField()
    lng = models.FloatField()
