from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):

    USER = 'user'
    ADMIN = 'admin'
    ROLES = [
        (USER, USER),
        (ADMIN, ADMIN),
    ]

    email = models.EmailField(max_length=254, unique=True, blank=False)
    username = models.CharField(max_length=150, unique=True, blank=False,)
    first_name = models.CharField(max_length=150, unique=False, blank=False)
    last_name = models.CharField(max_length=150, unique=False, blank=False)
    password = models.CharField(max_length=150, blank=False)
    role = models.CharField(max_length=20, choices=ROLES, default=USER)

    @property
    def is_admin(self):
        return self.role == self.ADMIN or self.is_superuser

    @property
    def is_user(self):
        return self.role == self.USER

    class Meta:
        ordering = ['username']
        verbose_name = 'Пользователь'
        verbose_name_plural = 'Пользователи'

    def __str__(self):
        return self.username
