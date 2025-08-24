"""
Admin configuration for the Menu app.

Registers the MenuItem model with custom admin options including:
- List display fields
- Filters
- Search fields
- Ordering
"""

from django.contrib import admin
from .models import MenuItem

@admin.register(MenuItem)
class MenuItemAdmin(admin.ModelAdmin):
    list_display = ('name', 'category', 'price', 'available')
    list_filter = ('category', 'available')
    search_fields = ('name', 'description')
    ordering = ('category', 'name')