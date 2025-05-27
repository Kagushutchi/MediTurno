from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import CustomUser  # Import your custom user model


class CustomUserAdmin(UserAdmin):
    model = CustomUser
    list_display = ('email', 'is_staff', 'is_superuser', 'role')# Customize fields shown in admin
    fieldsets = UserAdmin.fieldsets + (
        ('Custom Fields', {'fields': ('role',)}),
    )
    
    @admin.display(description="User Role")
    def get_role(self, obj):
        return obj.role.capitalize() 

admin.site.register(CustomUser, CustomUserAdmin)