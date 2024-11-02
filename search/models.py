from uuid import uuid4

from django.db import models
from django.conf import settings
from django.core.validators import MinValueValidator, MaxValueValidator


class TemporaryUser(models.Model):
    id = models.UUIDField(
        primary_key=True, default=uuid4, editable=False,
    )

    created_at = models.DateTimeField(auto_now_add=True)


class UserSearch(models.Model):
    user = models.OneToOneField(
        settings.AUTH_USER_MODEL, null=True, blank=True, on_delete=models.CASCADE,
    )

    temporary_user = models.OneToOneField(
        TemporaryUser, null=True, blank=True, on_delete=models.CASCADE,
    )

    start_date = models.DateField()
    end_date = models.DateField()

    radius = models.IntegerField(
        default=500,
        validators=[MinValueValidator(500), MaxValueValidator(500_000)],
    )

    favorites = models.ManyToManyField(
        "workshop.Workshop", blank=True, related_name="favorites",
    )
    declined = models.ManyToManyField(
        "workshop.Workshop", blank=True, related_name="declined",
    )


class SearchFeedback(models.Model):
    search = models.OneToOneField(
        UserSearch, on_delete=models.CASCADE,
    )

    workshop = models.OneToOneField(
        "workshop.Workshop", on_delete=models.CASCADE,
    )

    is_accepted = models.BooleanField()
