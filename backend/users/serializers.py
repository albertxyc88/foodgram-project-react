from djoser.serializers import UserCreateSerializer as DjoserUserCreate
from rest_framework import serializers
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
