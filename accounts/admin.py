from django.contrib import admin
from .models import User


class UserAdmin(admin.ModelAdmin):
    list_display = ('username', 'nickname', 'role')
    list_filter = ('role',)
    search_fields = ('username', 'nickname')
    fieldsets = (
        (None, {
            'fields': ('nickname', 'role')
        }),
    )
    ordering = ('username',)

    def save_model(self, request, obj, form, change):
        if obj.role == 'A':
            obj.is_superuser = True
            obj.is_staff = True
        elif obj.role == 'S':
            obj.is_superuser = False
            obj.is_staff = True
        elif obj.role == 'U':
            obj.is_superuser = False
            obj.is_staff = False

        obj.save()

admin.site.register(User, UserAdmin)
