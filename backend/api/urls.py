from django.urls import include, path
from rest_framework import routers

from .views import IngredientsViewSet, TagsViewSet

app_name = 'recipe'

router = routers.DefaultRouter()

router.register(r'tags', TagsViewSet, basename='tags')
router.register(r'ingredients', IngredientsViewSet, basename='ingredients')

urlpatterns = [
    path('', include(router.urls)),
]
