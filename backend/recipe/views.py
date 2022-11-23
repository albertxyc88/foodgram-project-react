from rest_framework import viewsets
from rest_framework.filters import SearchFilter
from rest_framework.permissions import AllowAny

from .models import Ingredients, Tags
from .serializers import IngredientsSerializer, TagsSerializer


class TagsViewSet(viewsets.ReadOnlyModelViewSet):
    """Вьюсет для тегов в режиме только чтение."""

    queryset = Tags.objects.all()
    serializer_class = TagsSerializer
    permission_classes = (AllowAny,)
    pagination_class = None

class IngredientsViewSet(viewsets.ReadOnlyModelViewSet):
    """Вьюсет для ингредиентов в режиме только чтение."""

    queryset = Ingredients.objects.all()
    serializer_class = IngredientsSerializer
    permission_classes = (AllowAny,)
    filter_backends = (SearchFilter,)
    search_fields = ('^name', 'name')
    pagination_class = None