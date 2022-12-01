from django.urls import include, path
from rest_framework import routers

from .views import IngredientsViewSet, RecipesViewSet, TagsViewSet

app_name = 'recipe'

router = routers.DefaultRouter()

router.register('tags', TagsViewSet, basename='tags')
router.register('ingredients', IngredientsViewSet, basename='ingredients')
router.register('recipes', RecipesViewSet, basename='recipes')


urlpatterns = [
    path('', include(router.urls)),
]
