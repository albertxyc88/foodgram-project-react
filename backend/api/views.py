from django.db.models import Sum
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import serializers, status, viewsets
from rest_framework.decorators import action
from rest_framework.filters import SearchFilter
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response

from recipe.models import (Favorite, Ingredients, IngredientsRecipes, Recipes,
                           ShoppingCart, Tags)

from .filters import RecipesFilter
from .paginators import CustomPaginator
from .permissions import IsAuthorOrAdminOnlyPermission
from .serializers import (FavoriteOrCartSerializer, FavoriteRecipeSerializer,
                          IngredientsSerializer, RecipeCreateSerializer,
                          RecipesSerializer, ShoppingCartSerializer,
                          TagsSerializer)
from .utils import generate_pdf


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


class RecipesViewSet(viewsets.ModelViewSet):
    """Вьюсет для рецептов, списка покупок, избранных рецептов."""

    queryset = Recipes.objects.all()
    serializer_class = RecipesSerializer
    pagination_class = CustomPaginator
    filter_backends = (DjangoFilterBackend,)
    filterset_class = RecipesFilter
    http_method_names = ['get', 'post', 'patch', 'delete']

    def get_serializer_class(self):
        if self.action in ('list', 'retrieve'):
            return RecipesSerializer
        if self.action == 'favorite':
            return FavoriteRecipeSerializer
        if self.action == 'shopping_cart':
            return ShoppingCartSerializer
        return RecipeCreateSerializer

    def get_permissions(self):
        if self.action in ('list', 'retrieve'):
            self.permission_classes = (AllowAny,)
        elif self.action in ('favorite', 'shopping_cart'):
            self.permission_classes = (IsAuthenticated,)
        elif self.request.method in (
            'PATCH', 'DELETE'
        ):
            self.permission_classes = (IsAuthorOrAdminOnlyPermission,)
        return super().get_permissions()

    def perform_create(self, serializer):
        serializer.save(author=self.request.user)

    @action(
        methods=['get'], detail=False,
    )
    def download_shopping_cart(self, request):
        cart = IngredientsRecipes.objects.filter(
            recipe__cart__user=request.user
        ).values(
            'ingredient__name',
            'ingredient__measurement_unit'
        ).annotate(
            Sum('amount')
        )
        cart_txt = []
        for item in cart:
            cart_txt.append(
                item['ingredient__name'] + ' - ' +
                str(item['amount__sum']) + ' ' +
                item['ingredient__measurement_unit']
            )
        return generate_pdf(cart_txt)

    @action(
        methods=['post', 'delete'], detail=True,
    )
    def favorite(self, request, pk):
        func_model = Favorite
        return custom_post_delete(self, request, pk, func_model)

    @action(
        methods=['post', 'delete'], detail=True,
    )
    def shopping_cart(self, request, pk):
        func_model = ShoppingCart
        return custom_post_delete(self, request, pk, func_model)


def custom_post_delete(self, request, pk, func_model):
    """Обработка delete, post запросов."""

    user = self.request.user
    recipe = self.get_object()
    if request.method == 'DELETE':
        instance = func_model.objects.filter(recipe=recipe, user=user)
        if not instance:
            raise serializers.ValidationError(
                {
                    'errors': [
                        'Этот рецепт в списке отсутствует.'
                    ]
                }
            )
        instance.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
    data = {
        'user': user.id,
        'recipe': pk
    }
    favorite = self.get_serializer(data=data)
    favorite.is_valid(raise_exception=True)
    favorite.save()
    serializer = FavoriteOrCartSerializer(recipe)
    return Response(serializer.data, status=status.HTTP_201_CREATED)
