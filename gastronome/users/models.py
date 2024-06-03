import uuid

from django.contrib.auth.models import AbstractUser
from django.db import models


class AppUser(AbstractUser):
    id = models.UUIDField(
        primary_key=True,
        default=uuid.uuid4,
        editable=False,
    )
    is_business = models.BooleanField(
        default=False,
        null=False,
        help_text="Business user can create restaurant. Regular user can create review.",
    )
