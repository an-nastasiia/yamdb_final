from django.contrib.admin import ModelAdmin, register

from .models import User


@register(User)
class UserAdmin(ModelAdmin):
    list_display = ('pk', 'username', 'email', 'first_name',
                    'last_name', 'is_superuser', 'role',)
    list_editable = ('is_superuser', 'role',)
    search_fields = ('username', 'first_name', 'last_name', 'email',)
    list_filter = ('is_superuser', 'role',)
    empty_value_display = '-пусто-'
