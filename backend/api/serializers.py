from django.conf import settings
from django.shortcuts import get_object_or_404
from drf_extra_fields.fields import Base64ImageField
from rest_framework import serializers
from rest_framework.validators import UniqueTogetherValidator

from recipe.models import (Favorite, Ingredients, IngredientsRecipes, Recipes,
                           ShoppingCart, Tags, TagsRecipes)
from users.serializers import UserSerializer


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


class IngredientsRecipesSerializer(serializers.ModelSerializer):
    """Для показа ингредиентов в рецепте."""

    id = serializers.IntegerField(source='ingredient.id')
    name = serializers.CharField(source='ingredient.name')
    measurement_unit = serializers.CharField(
        source='ingredient.measurement_unit'
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
        read_only_fields = ('user', 'ingredients',)

    def to_representation(self, value):
        return RecipesSerializer(value, context=self.context).data

    def create(self, validated_data):
        tags = validated_data.pop('tags')
        ingredients = validated_data.pop('ingredients')
        recipe = Recipes.objects.create(**validated_data)
        for item in tags:
            TagsRecipes.objects.create(
                tag=item,
                recipe=recipe
            )
        for item in ingredients:
            ingredient = get_object_or_404(Ingredients, id=item.get('id'))
            IngredientsRecipes.objects.create(
                ingredient=ingredient,
                recipe=recipe,
                amount=item.get('amount')
            )
        return recipe

    def update(self, instance, validated_data):
        if validated_data.get('image') is not None:
            instance.image = validated_data.pop('image')
        instance.name = validated_data.get('name')
        instance.text = validated_data.get('text')
        instance.cooking_time = validated_data.get('cooking_time')

        tags = validated_data.pop('tags')
        instance.tags.set(tags)

        ingredients = validated_data.pop('ingredients')
        instance.ingredients.clear()
        for item in ingredients:
            ingredient = get_object_or_404(Ingredients, id=item.get('id'))
            instance.ingredients.add(
                ingredient,
                through_defaults={'amount': item.get('amount')}
            )
        instance.save()
        return instance


class RecipesSerializer(serializers.ModelSerializer):
    """Вывод списка рецептов."""

    tags = TagsSerializer(many=True)
    ingredients = IngredientsRecipesSerializer(
        many=True, source='ingredientsrecipes_set'
    )
    author = UserSerializer(
        many=False,
        read_only=True
    )
    image = Base64ImageField()
    is_favorite = serializers.SerializerMethodField(
        read_only=True,
        method_name='get_is_favorite'
    )
    is_in_shopping_cart = serializers.SerializerMethodField(
        read_only=True,
        method_name='get_is_in_shopping_cart'
    )

    def get_is_favorite(self, recipe):
        user = self.context['request'].user
        return (
            user.is_authenticated and
            recipe.favorite.filter(user=user).exists()
        )

    def get_is_in_shopping_cart(self, recipe):
        user = self.context['request'].user
        return (
            user.is_authenticated and
            recipe.cart.filter(user=user).exists()
        )

    class Meta:
        model = Recipes
        fields = (
            'id',
            'tags',
            'author',
            'ingredients',
            'is_favorite',
            'is_in_shopping_cart',
            'name',
            'image',
            'text',
            'cooking_time'
        )


class FavoriteRecipeSerializer(serializers.ModelSerializer):
    """Добавление рецепта в избранное."""

    class Meta:
        model = Favorite
        fields = '__all__'

        validators = [
            UniqueTogetherValidator(
                queryset=Favorite.objects.all(),
                fields=('user', 'recipe'),
                message='Этот рецепт уже добавлен в избранное.'
            )
        ]


class ShoppingCartSerializer(serializers.ModelSerializer):
    """Добавление рецепта в список покупок."""

    class Meta:
        model = ShoppingCart
        fields = '__all__'

        validators = [
            UniqueTogetherValidator(
                queryset=ShoppingCart.objects.all(),
                fields=('user', 'recipe'),
                message='Этот рецепт уже добавлен в список покупок.'
            )
        ]


class FavoriteOrCartSerializer(serializers.ModelSerializer):
    """Отображение рецептов в избранном, списке покупок."""

    class Meta:
        model = Recipes
        fields = (
            'id',
            'name',
            'image',
            'cooking_time'
        )
        read_only_fields = (
            'name',
            'image',
            'cooking_time'
        )
