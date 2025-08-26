"""
URL configuration for dons_table project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.2/topics/http/urls/

This module defines the URL patterns for the project, routing
requests to the appropriate apps and views:

- Home page
- Account management via allauth
- Admin interface
- Menu app
- Reservations app
"""

from django.contrib import admin
from django.urls import path, include
from menu.views import my_menu
from reservations.views import make_reservation, reservation_dashboard
from .views import home, contact

urlpatterns = [
    path('', home, name='home'),
    path("accounts/", include("allauth.urls")),
    path('admin/', admin.site.urls),
    path("contact/", contact, name="contact"),
    path('menu/', include("menu.urls")),
    path('reservation/', include('reservations.urls')),
]
