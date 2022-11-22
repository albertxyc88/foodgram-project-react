from django.contrib.auth import get_user_model
from djoser.views import UserViewSet
from rest_framework import serializers, status
from rest_framework.decorators import action
from rest_framework.response import Response

User = get_user_model()


class UserCustomViewSet(UserViewSet):
    """Кастомизированный вьюсет библиотеки 'djoser'."""
