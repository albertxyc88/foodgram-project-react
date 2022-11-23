from django.contrib import admin

from .models import Ingredients, Tags

admin.site.register(Tags)
admin.site.register(Ingredients)
