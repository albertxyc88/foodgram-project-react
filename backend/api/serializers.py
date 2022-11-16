from django.contrib.auth import get_user_model
from rest_framework import serializers

User = get_user_model()


class UserSerializer(serializers.ModelSerializer):
    """User serializer."""

    # is_subscribed = serializers.SerializerMethodField()

    class Meta:
        model = User
        fields = (
            'email',
            'id',
            'username',
            'first_name',
            'last_name',
            'password',
            # 'is_subscribed'
        )
        extra_kwargs = {
            "password": {
                'write_only': True
            }
        }

    # def get_is_subscribed(self, obj):
    #     request = self.context.get('request')
    #     if request is None or request.user.is_anonymous:
    #         return False
    #     user = request.user
    #     return Follow.objects.filter(following=obj, user=user).exists()

class ChangePasswordSerializer(serializers.Serializer):
    model = User
    current_password = serializers.CharField(required=True)
    new_password = serializers.CharField(required=True)