from rest_framework import viewsets
from rest_framework.permissions import AllowAny

from .models import Tags
from .serializers import TagsSerializer


class TagsViewSet(viewsets.ReadOnlyModelViewSet):
    """Вьюсет для тегов в режиме только чтение."""

    queryset = Tags.objects.all()
    serializer_class = TagsSerializer
    permission_classes = (AllowAny,)
