from api.serializers import FavoriteOrCartSerializer
from django.conf import settings
from djoser.serializers import UserCreateSerializer as DjoserUserCreate
from rest_framework import serializers
from rest_framework.validators import UniqueTogetherValidator
from users.models import Follow, User


class UserSerializer(serializers.ModelSerializer):
    """User profile serializer."""

    email = serializers.EmailField(required=True)
    username = serializers.CharField(max_length=150, required=True)
    first_name = serializers.CharField(max_length=150, required=True)
    last_name = serializers.CharField(max_length=150, required=True)
    is_subscribed = serializers.SerializerMethodField(read_only=True)

    def get_is_subscribed(self, username):
        user = self.context['request'].user
        return (
            user.is_authenticated
            and Follow.objects.filter(
                user=user,
                following=username
            ).exists()
        )

    class Meta:
        model = User
        fields = (
            'email',
            'id',
            'username',
            'first_name',
            'last_name',
            'is_subscribed'
        )


class UserCreateSerializer(DjoserUserCreate):
    """User create serializer."""

    class Meta:
        model = User
        fields = (
            'email',
            'username',
            'first_name',
            'last_name',
            'password',
            'role'
        )

    def validate_username(self, data):
        if User.objects.filter(username=data).exists():
            raise serializers.ValidationError(
                "Username is already registered."
            )
        return data

    def validate_email(self, data):
        if User.objects.filter(email=data).exists():
            raise serializers.ValidationError(
                "Email is already registered."
            )
        return data


class FollowCreateSerializer(serializers.ModelSerializer):
    """Подписаться на пользователя."""

    class Meta:
        model = Follow
        fields = '__all__'

        validators = [
            UniqueTogetherValidator(
                queryset=Follow.objects.all(),
                fields=('user', 'following'),
                message='Вы уже подписаны на этого пользователя.'
            )
        ]

    def validate(self, data):
        if data['user'] == data['following']:
            raise serializers.ValidationError(
                'Вы не можете подписаться на самого себя.')
        return data


class FollowSerializer(serializers.ModelSerializer):
    """Вывод подписок."""

    is_subscribed = serializers.SerializerMethodField()
    recipes = serializers.SerializerMethodField()
    recipes_count = serializers.SerializerMethodField()

    class Meta:
        model = User
        fields = (
            'email',
            'id',
            'username',
            'first_name',
            'last_name',
            'is_subscribed',
            'recipes',
            'recipes_count'
        )

    def get_recipes(self, obj):
        limit = self.context['request'].query_params.get(
            'recipes_limit', settings.RECIPES_DEFAULT
        )
        recipes = obj.recipes.all()[:int(limit)]
        return FavoriteOrCartSerializer(recipes, many=True).data

    def get_is_subscribed(self, obj):
        user = self.context['request'].user
        return bool(obj.subscriber.filter(user=user))

    def get_recipes_count(self, obj):
        return obj.recipes.count()
