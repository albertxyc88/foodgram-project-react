from rest_framework.pagination import PageNumberPagination


class RecipePaginator(PageNumberPagination):
    """Пагинатор для списка рецептов."""

    page_size = 10
    page_size_query_param = 'limit'
    max_page_size = 100
