from django.contrib import admin

from .models import Follow, User


class UserAdmin(admin.ModelAdmin):
    list_display = ('pk', 'first_name', 'last_name', 'username', 'email')
    list_filter = ('email', 'username')
    search_fields = ('email', 'username')


admin.site.register(User, UserAdmin)
admin.site.register(Follow)
