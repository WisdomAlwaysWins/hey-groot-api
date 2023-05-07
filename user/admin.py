from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from django.db import models
from .models import User
from django.forms import Textarea

class UserAdminConfig(UserAdmin):
    ordering = ('-created_at',)
    list_display = ('id', 'email', 'last_login')

    fieldsets = (
        (None, {'fields': ('email', 'password', 'created_at', 'last_login')}),
        ('Permissions', {'fields': ('is_staff', 'is_active',)}),
    )
    formfield_overrides = {
        models.TextField: {'widget': Textarea(attrs={'rows': 20, 'cols': 60})},
    }
    add_fieldsets = (
        (None, {
            # 'classes': ('wide',),
            'fields' : ('email', 'password', 'is_active', 'is_staff')}
        ),
    )



admin.site.register(User, UserAdminConfig)