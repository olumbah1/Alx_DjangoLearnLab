from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import CustomUser
# Register your models here.

class CustomUserAdmin(UserAdmin):
    list_display = ('username', 'email', 'date_of_birth', 'is_staff')
    model = CustomUser
    fieldsets = UserAdmin.fieldsets + (
        ('Etra Info', {'fields': ('date_of_birth','profile_photo')})
    )
    add_fieldsets = UserAdmin.add_fieldsets + (
        ('Extra Info', {'fields': ('date_of_birth', 'profile_photo')})
    )
admin.site.register(CustomUser,CustomUserAdmin)