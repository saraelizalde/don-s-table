"""
URL configuration for the Menu app.

Defines the URL patterns for menu-related views:

- Display menu items
- Superuser menu management: list, add, edit, delete
"""

from django.urls import path
from . import views

urlpatterns = [
    path("", views.my_menu, name="menu"),
    path('manage/', views.superuser_menu, name='superuser_menu'),
    path('manage/add/', views.add_menu_item, name='add_menu_item'),
    path('manage/<int:item_id>/edit/',
         views.edit_menu_item, name='edit_menu_item'),
    path('manage/<int:item_id>/delete/',
         views.delete_menu_item, name='delete_menu_item'),
]
