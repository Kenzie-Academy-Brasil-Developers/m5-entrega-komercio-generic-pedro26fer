from django.db import models
from django.contrib.auth.models import AbstractUser
import uuid


class User(AbstractUser):

    id = models.UUIDField(default=uuid.uuid4, primary_key=True, editable=False)
    username = models.CharField(max_length=50, unique=True)
    # password = models.CharField(max_length=20)
    first_name = models.CharField(max_length=50)
    last_name = models.CharField(max_length=50)
    is_seller = models.BooleanField(blank=True, null=True, default=False)

    REQUIRED_FIELDS = ["first_name", "last_name"]
