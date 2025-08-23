from django.urls import path
from . import views

urlpatterns = [
    path('dashboard/', views.reservation_dashboard, name='reservation_dashboard'),
    path('form/', views.make_reservation, name='make_reservation'),
    path("<int:reservation_id>/edit/", views.edit_reservation, name="edit_reservation"),
    path("<int:reservation_id>/cancel/", views.cancel_reservation, name="cancel_reservation"),
]