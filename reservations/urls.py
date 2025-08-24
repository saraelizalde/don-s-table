"""
URL configuration for the Reservations app.

Defines URL patterns for managing reservations:
- Dashboard view
- Make a new reservation
- Edit an existing reservation
- Cancel a reservation
"""

from django.urls import path
from . import views

urlpatterns = [
    path('dashboard/', views.reservation_dashboard, name='reservation_dashboard'),
    path('form/', views.make_reservation, name='make_reservation'),
    path("<int:reservation_id>/edit/", views.edit_reservation, name="edit_reservation"),
    path("<int:reservation_id>/cancel/", views.cancel_reservation, name="cancel_reservation"),
]