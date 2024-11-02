from django.db import models
from django.conf import settings


class Workshop(models.Model):
    scheduled_at = models.DateField()
    created_at = models.DateField(auto_now=True)

    title = models.CharField(max_length=128)
    description = models.TextField()

    price = models.DecimalField(max_digits=16, decimal_places=2)
    capacity = models.IntegerField()

    location = models.ForeignKey(
        "location_app.Location",
        on_delete=models.CASCADE,
    )


class Review(models.Model):
    class Rating(models.IntegerChoices):
        TERRIBLE = 1
        BAD = 2
        AVERAGE = 3
        GOOD = 4
        EXCELLENT = 5
    
    rating = models.IntegerField(choices=Rating)
    description = models.TextField()

    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
    )
    workshop = models.ForeignKey(
        Workshop,
        on_delete=models.CASCADE,
    )


class Link(models.Model):
    name = models.CharField()
    href = models.CharField()


class Category(models.Model):
    name = models.CharField(max_length=128)


class Image(models.Model):
    content = models.ImageField()

    workshop = models.ForeignKey(
        Workshop,
        on_delete=models.CASCADE,
    )

class WorkshopImageMapping(models.Model):
    workshop = models.ForeignKey(
        Workshop,
        on_delete=models.CASCADE,
    )

    image = models.ForeignKey(
        Image,
        on_delete=models.CASCADE,
    )
