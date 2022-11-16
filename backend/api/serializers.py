from rest_framework import serializers
from users.models import Follow, User


class UserSerializer(serializers.ModelSerializer):
    """User serializer."""

    email = serializers.EmailField()
    username = serializers.CharField()
    first_name = serializers.CharField()
    last_name = serializers.CharField()
    is_subscribed = serializers.SerializerMethodField(read_only=True)

    def get_is_subscribed(self, username):
        user = self.context['request'].user
        return Follow.objects.filter(
            user=user,
            following=username
        ).exists()

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
