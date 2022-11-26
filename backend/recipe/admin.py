from django.contrib import admin

from .models import (Favorite, Ingredients, IngredientsRecipes, Recipes,
                     ShoppingCart, Tags, TagsRecipes)


class RecipesAdmin(admin.ModelAdmin):
    list_display = ('name', 'author')
    list_filter = ('name', 'author', 'tags')
    readonly_fields = ('favorite_added',)

    def favorite_added(self, instance):
        return instance.favorite.count()

    favorite_added.short_description = 'В избранном'


admin.site.register(Favorite)
admin.site.register(Ingredients)
admin.site.register(IngredientsRecipes)
admin.site.register(Recipes, RecipesAdmin)
admin.site.register(ShoppingCart)
admin.site.register(Tags)
admin.site.register(TagsRecipes)
