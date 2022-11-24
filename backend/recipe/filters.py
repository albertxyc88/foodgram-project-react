from django_filters import rest_framework as filters
from recipe.models import Recipes, Tags


class RecipesFilter(filters.FilterSet):
    """Фильтр  для рецептов."""

    is_favorited = filters.NumberFilter(
        field_name='favorite__user', method='favorite_filter'
    )
    is_in_shopping_cart = filters.NumberFilter(
        field_name='cart__user', method='cart_filter'
    )
    tags = filters.ModelMultipleChoiceFilter(
        field_name='tags__slug',
        queryset=Tags.objects.all(),
        to_field_name='slug'
    )

    class Meta:
        model = Recipes
        fields = (
            'author',
        )

    def cart_filter(self, queryset, name, value):
        if value:
            return queryset.filter(favorite__user=self.request.user)
        return queryset

    def favorite_filter(self, queryset, name, value):
        if value:
            return queryset.filter(cart__user=self.request.user)
        return queryset
    