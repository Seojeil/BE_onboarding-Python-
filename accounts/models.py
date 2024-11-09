from django.db import models
from django.contrib.auth.models import AbstractUser, UserManager


class CustomUserManager(UserManager):
    def create_superuser(self, nickname, password=None, **extra_fields):
        extra_fields.setdefault("is_staff", True)
        extra_fields.setdefault("is_superuser", True)

        if extra_fields.get("is_staff") is not True:
            raise ValueError("Superuser must have is_staff=True.")
        if extra_fields.get("is_superuser") is not True:
            raise ValueError("Superuser must have is_superuser=True.")

        extra_fields.setdefault('roles', 'A')

        return self._create_user(nickname, None, password, **extra_fields)


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

    REQUIRED_FIELDS = ["nickname"]

    def __str__(self):
        return self.username
