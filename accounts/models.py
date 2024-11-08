from django.db import models
from django.contrib.auth.models import AbstractUser


class Role(models.Model):
    ROLE_CHOICES = [
        ("A", "ADMIN"),
        ("S", "STAFF"),
        ("U", "USER"),
    ]

    name = models.CharField(
        max_length=50, choices=ROLE_CHOICES, default="U", unique=True
    )

    def __str__(self):
        return self.name


class User(AbstractUser):
    nickname = models.CharField(max_length=20, unique=True)
    roles = models.ManyToManyField(Role, related_name="users", blank=True)

    def __str__(self):
        return self.username
