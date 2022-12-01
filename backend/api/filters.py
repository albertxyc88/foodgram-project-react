from django_filters import rest_framework as filters

from recipe.models import Recipes, Tags


class RecipesFilter(filters.FilterSet):
    """Фильтр  для рецептов."""

    is_favorited = filters.NumberFilter(
        field_name='favorite__user', method='filter_lists'
    )
    is_in_shopping_cart = filters.NumberFilter(
        field_name='cart__user', method='filter_lists'
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

    def filter_lists(self, queryset, name, value):
        user = self.request.user
        if user.is_anonymous or not int(value):
            return queryset
        return queryset.filter(**{name: user})
