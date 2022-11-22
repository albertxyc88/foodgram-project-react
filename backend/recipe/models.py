from django.core.validators import RegexValidator
from django.db import models


class Tags(models.Model):
    """Модель для тегов."""

    name = models.CharField(
        max_length=200,
        unique=True,
        verbose_name='Имя'
    )
    color = models.CharField(
        max_length=7,
        unique=True,
        validators=[RegexValidator(regex=r'^#(A-Fa-f0-9]{6})$')],
        verbose_name='Цвет'
    )
    slug = models.SlugField(
        max_length=200,
        unique=True
    )

    class Meta:
        verbose_name = 'Тег'
        verbose_name_plural = 'Теги'

    def __str__(self):
        return self.name