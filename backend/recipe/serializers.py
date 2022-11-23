from django.conf import settings
from drf_extra_fields.fields import Base64ImageField
from rest_framework import serializers
from users.models import User
from users.serializers import UserSerializer

from .models import Ingredients, IngredientsRecipes, Recipes, Tags, TagsRecipes


class TagsSerializer(serializers.ModelSerializer):
    """Сериализатор для тегов."""

    class Meta:
        model = Tags
        fields = '__all__'


class IngredientsSerializer(serializers.ModelSerializer):
    """Сериализатор для ингредиентов."""

    class Meta:
        model = Ingredients
        fields = '__all__'


class IngredientsRecipesSaveSerializator(serializers.Serializer):
    """Для сохранения ингридентов рецепта."""

    id = serializers.IntegerField()
    amount = serializers.IntegerField(min_value=settings.MIN_VALUE)


class IngreientsRecipesSerializer(serializers.ModelSerializer):
    """Для показа ингредиентов в рецепте."""

    id = serializers.IntegerField(source='ingredients.id')
    name = serializers.CharField(source='ingredients.name')
    measurement_unit = serializers.CharField(
        source='ingredients.measurement_unit'
    )

    class Meta:
        model = IngredientsRecipes
        fields = ('id', 'name', 'measurement_unit', 'amount')


class RecipeCreateSerializer(serializers.ModelSerializer):
    """Создание рецепта."""

    author = UserSerializer(
        default=serializers.CurrentUserDefault(),
        read_only=True
    )
    image = Base64ImageField()
    ingredients = IngredientsRecipesSaveSerializator(many=True)
    tags = serializers.PrimaryKeyRelatedField(
        many=True,
        queryset=Tags.objects.all()
    )

    class Meta:
        model = Recipes
        fields = '__all__'
        read_only_fields = ('author', 'ingredients')
    
    def to_representation(self, instance):
        return Recipe