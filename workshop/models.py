from django.db import models
from django.conf import settings


class Link(models.Model):
    name = models.CharField()
    href = models.CharField()


class Category(models.Model):
    name = models.CharField(max_length=128)


class Image(models.Model):
    content = models.ImageField()


class Workshop(models.Model):
    scheduled_at = models.DateField()
    created_at = models.DateField(auto_now=True)

    title = models.CharField(max_length=128)
    description = models.TextField()

    categories = models.ManyToManyField(Category)
    links = models.ManyToManyField(Link)
    images = models.ManyToManyField(Image)

    price = models.DecimalField(max_digits=16, decimal_places=2)
    capacity = models.IntegerField()

    location = models.ForeignKey(
        "location_app.Location",
        on_delete=models.CASCADE,
    )

    def get_average_rating(self) -> int:
        reviews = Review.objects.filter(workshop=self)

        length = len(reviews)

        if not length:
            return 0

        return round(
            sum(r.rating for r in reviews) / length
        )

    def rating_prerendered(self) -> str:
        rating = self.get_average_rating()

        out = ""

        for _ in range(rating):
            out += '<i class="fas fa-star text-warning"></i>'
        
        for _ in range(5 - rating):
            out += '<i class="far fa-star text-warning"></i>'

        return out


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
