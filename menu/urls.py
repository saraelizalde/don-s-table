"""
URL configuration for the Menu app.

Defines the URL patterns for menu-related views.
"""

from django.urls import path
from . import views

urlpatterns = [
    path("", views.my_menu, name="menu"),
]