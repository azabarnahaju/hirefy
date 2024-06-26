"""
Dajngo admin customization.
"""
from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.utils.translation import gettext_lazy as _
from django.contrib.auth.forms import UserChangeForm
from django import forms

from core import models


class CustomUserChangeForm(UserChangeForm):
    """Form for updating users."""

    class Meta:
        model = models.User
        fields = ['email', 'first_name', 'last_name', 'is_active',
                  'is_staff', 'is_superuser', 'role']
        widgets = {
            'role': forms.TextInput(attrs={'readonly': 'readonly'})
        }


class UserAdmin(BaseUserAdmin):
    """Define the admin pages for users."""
    ordering = ['id']
    list_display = ['email', 'first_name', 'last_name', 'role']
    form = CustomUserChangeForm

    fieldsets = (
        (None, {'fields': ('email', 'password')}),
        (
            _('Basic data'),
            {
                'fields': (
                    'first_name',
                    'last_name',
                    'role'
                )
            }
        ),
        (
            _('Permissions'),
            {
                'fields': (
                    'is_active',
                    'is_staff',
                    'is_superuser'
                )
            }
        ),
        (
            _('Important dates'),
            {
                'fields': (
                    'last_login',
                    'date_joined'
                )
            }
        )
    )
    readonly_fields = ['last_login', 'date_joined']
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': (
                'email',
                'password1',
                'password2',
                'role',
                'first_name',
                'last_name',
                'is_active',
                'is_superuser',
                'is_staff',
            )
        }),
    )


admin.site.register(models.User, UserAdmin)
admin.site.register(models.CompanyProfile)
admin.site.register(models.TalentProfile)
admin.site.register(models.Job)
