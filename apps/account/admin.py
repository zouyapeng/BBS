
from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from apps.account import models
from django.utils.translation import ugettext, ugettext_lazy as _



class MyUserAdmin(UserAdmin):
    fieldsets = (
        (None, {'fields': ('username', 'password')}),
        (_('Personal info'), {'fields': ('avatar', 'first_name', 'last_name', 'email')}),
        (_('Permissions'), {'fields': ('is_active', 'is_staff', 'is_superuser',
                                       'groups', 'user_permissions')}),
        (_('Important dates'), {'fields': ('last_login', 'date_joined')}),
    )


admin.site.register(models.User, MyUserAdmin)

