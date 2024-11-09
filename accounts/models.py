from django.db import models
from django.contrib.auth.models import AbstractUser, UserManager


class CustomUserManager(UserManager):
    def create_superuser(self, username, password=None, **extra_fields):
        extra_fields.setdefault('role', 'A')

        return self._create_user(username, None, password, **extra_fields)


class User(AbstractUser):
    ROLE_CHOICES = [
        ("A", "ADMIN"),
        ("S", "STAFF"),
        ("U", "USER"),
    ]

    nickname = models.CharField(max_length=20, unique=True)
    role = models.CharField(choices=ROLE_CHOICES, max_length=1, default="U")

    REQUIRED_FIELDS = ["nickname"]

    objects = CustomUserManager()

    def __str__(self):
        return self.username
