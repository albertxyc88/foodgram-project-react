from django.contrib.auth import get_user_model
from djoser.views import UserViewSet
from rest_framework import serializers, status
from rest_framework.decorators import action
from rest_framework.response import Response

from api.paginators import CustomPaginator

from .serializers import FollowCreateSerializer, FollowSerializer

User = get_user_model()


class UserCustomViewSet(UserViewSet):
    """Кастомный юзер вьюсет."""

    pagination_class = CustomPaginator

    @action(
        methods=['get'], detail=False,
        serializer_class=FollowSerializer
    )
    def subscriptions(self, request):
        user = self.request.user

        def queryset():
            return User.objects.filter(following__user=user)

        self.get_queryset = queryset
        return self.list(request)

    @action(
        methods=['post', 'delete'], detail=True,
        serializer_class=FollowSerializer
    )
    def subscribe(self, request, id):
        user = self.request.user
        following = self.get_object()
        if request.method == 'DELETE':
            instance = user.follower.filter(following=following)
            if not instance:
                raise serializers.ValidationError(
                    {
                        'errors': [
                            'Вы не подписаны на этого автора.'
                        ]
                    }
                )
            instance.delete()
            return Response(status=status.HTTP_204_NO_CONTENT)
        data = {
            'user': user.id,
            'following': id
        }
        subscription = FollowCreateSerializer(data=data)
        subscription.is_valid(raise_exception=True)
        subscription.save()
        serializer = self.get_serializer(following)
        return Response(serializer.data, status=status.HTTP_201_CREATED)
