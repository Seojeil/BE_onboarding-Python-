from django.db import models
from django.contrib.auth.models import AbstractUser


# class Role(models.Model):
#     ROLE_CHOICES = [
#         ("A", "ADMIN"),
#         ("S", "STAFF"),
#         ("U", "USER"),
#     ]

#     name = models.CharField(
#         max_length=50, choices=ROLE_CHOICES, default="U", unique=True
#     )

#     def __str__(self):
#         return self.name


class User(AbstractUser):
    pass
    # nickname = models.CharField(max_length=20, unique=True)
    # roles = models.ManyToManyField(Role, related_name="users", blank=True)

    # # 기본 fields에 대한 related_name 지정
    # groups = models.ManyToManyField(
    #     'auth.Group', related_name='custom_user_groups', blank=True
    # )
    # user_permissions = models.ManyToManyField(
    #     'auth.Permission', related_name='custom_user_permissions', blank=True
    # )

    # def __str__(self):
    #     return self.username
