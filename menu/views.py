"""
Views for the Menu app.

Contains view functions for displaying the restaurant menu.
"""

from django.shortcuts import render
from django.http import HttpResponse
from .models import MenuItem

def my_menu(request):
    """
    Display the menu page with available items grouped by category.

    Categories considered: Starter, Main Course, Dessert, Drink.

    Template:
        menu.html
    """
    categories = ["starter", "main", "dessert", "drink"]
    menu_items = {cat: MenuItem.objects.filter(category=cat, available=True) for cat in categories}
    return render(request, "menu.html", {"menu_items": menu_items})