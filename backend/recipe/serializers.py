from rest_framework import serializers

from .models import Tags


class TagsSerializer(serializers.ModelSerializer):
    """Сериализатор для тегов."""

    class Meta:
        model = Tags
        fields = '__all__'
