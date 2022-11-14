from django.contrib.auth.models import AbstractUser
from django.core.validators import RegexValidator
from django.db import models


class User(AbstractUser):
    email = models.EmailField(max_length=254, unique=True, blank=False)
    username = models.CharField(
        max_length=150,
        unique=True,
        blank=False,
        # validators=[
        #     RegexValidator(
        #         regex=r'^[\w.@+-]+\z',
        #         message='Username is not valid.',
        #     ),
        # ]
    )
    first_name = models.CharField(max_length=150, unique=False, blank=False)
    last_name = models.CharField(max_length=150, unique=False, blank=False)
    password = models.CharField(max_length=150, blank=False)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username', 'first_name', 'last_name']

    class Meta:
        ordering = ['username']
        verbose_name = 'Пользователь'
        verbose_name_plural = 'Пользователи'

    def __str__(self):
        return self.username
