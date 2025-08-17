from django.urls import path
from . import views

urlpatterns = [
    path('dashboard/', views.reservation_dashboard, name='reservation_dashboard'),
    path('form/', views.make_reservation, name='make_reservation'),
]