import uuid

from django.db import models
from users.models import AppUser


class Restaurant(models.Model):
    id = models.UUIDField(
        primary_key=True,
        default=uuid.uuid4,
        editable=False,
    )
    name = models.CharField(null=False)
    description = models.TextField(default="", null=False)
    address = models.TextField(default="", null=False)
    created_by = models.ForeignKey(
        AppUser,
        on_delete=models.CASCADE,
        null=False,
    )
    created_at = models.DateTimeField(auto_now_add=True, editable=False)
    updated_at = models.DateTimeField(auto_now=True, editable=False)

    def __str__(self):
        return f"{self.name}({self.address})"
