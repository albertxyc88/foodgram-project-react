from rest_framework import serializers
from users.models import User


class UserSerializer(serializers.ModelSerializer):
    """User serializer."""

    class Meta:
        model = User
        fields = (
            'email',
            'id',
            'username',
            'first_name',
            'last_name',
            'password',
        )

    def create(self, validated_data):
        password = validated_data.pop('password')
        user = User.objects.create(**validated_data)
        user.set_password(password)
        user.save()
        return user


class DetailUserSerializer(UserSerializer):
    is_subscribed = serializers.SerializerMethodField()

    class Meta(UserSerializer.Meta):
        fields = (
            'email', 'id', 'username', 'first_name', 'last_name',
            'is_subscribed'
        )
