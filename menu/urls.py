from django.urls import path
from . import views

urlpatterns = [
    path("", views.my_menu, name="menu"),
]