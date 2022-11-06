from rest_framework import mixins, viewsets
from rest_framework.permissions import AllowAny
from users.models import User

from .serializers import DetailUserSerializer, UserSerializer


class UserViewSet(
    mixins.CreateModelMixin,
    mixins.ListModelMixin,
    mixins.RetrieveModelMixin,
    viewsets.GenericViewSet
):
    queryset = User.objects.all()
    permission_classes = (AllowAny,)

    def get_serializer_class(self):
        if self.action == 'retrieve':
            return DetailUserSerializer
        return UserSerializer
