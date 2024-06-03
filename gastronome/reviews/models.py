import uuid

from django.db import models
from restaurants.models import Restaurant
from users.models import AppUser


class Review(models.Model):
    id = models.UUIDField(
        primary_key=True,
        default=uuid.uuid4,
        editable=False,
    )
    restaurant = models.ForeignKey(
        Restaurant,
        on_delete=models.CASCADE,
        null=False,
    )
    score = models.IntegerField(default=3, null=False)
    comment = models.TextField(default="", null=False, max_length=300)
    created_by = models.ForeignKey(
        AppUser,
        on_delete=models.CASCADE,
        null=False,
    )
    created_at = models.DateTimeField(auto_now_add=True, editable=False)
    updated_at = models.DateTimeField(auto_now=True, editable=False)

    class Meta:
        unique_together = ('restaurant', 'created_by')

    def __str__(self):
        return f"{self.restaurant.name} - {self.created_by.username}"
