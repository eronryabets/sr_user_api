from django.contrib import admin
from .models import User


@admin.register(User)
class CustomUserAdmin(admin.ModelAdmin):
    list_display = ['id', 'first_name', 'last_name', 'created_at', 'updated_at']
    search_fields = ['id', 'first_name', 'last_name']
