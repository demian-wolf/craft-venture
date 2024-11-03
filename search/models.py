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
    created_at = models.DateTimeField(auto_now_add=True)

    starts_at = models.DateTimeField()
    ends_at = models.DateTimeField()

    radius = models.IntegerField(
        default=500,
        validators=[MinValueValidator(500), MaxValueValidator(500_000)],
    )

    lat = models.FloatField()
    lng = models.FloatField()


class UserSearchStage(models.Model):
    search = models.ForeignKey(
        UserSearch, on_delete=models.CASCADE,
    )
    workshop = models.OneToOneField(
        "workshop.Workshop", on_delete=models.CASCADE,
    )

    is_completed = models.BooleanField(default=False)
    is_accepted = models.BooleanField(default=False)
