from django.shortcuts import render
from django.http import HttpResponse
from .models import MenuItem

# Create your views here.
def my_menu(request):
    categories = ["starter", "main", "dessert", "drink"]
    menu_items = {cat: MenuItem.objects.filter(category=cat, available=True) for cat in categories}
    return render(request, "menu.html", {"menu_items": menu_items})