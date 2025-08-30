"""
Views for the Menu app.

Contains view functions for displaying the restaurant menu.
"""

from django.shortcuts import render, get_object_or_404, redirect
from django.http import HttpResponse
from .models import MenuItem
from .forms import MenuItemForm
from django.contrib import messages
from django.contrib.auth.decorators import user_passes_test


def my_menu(request):
    """
    Display the menu page with available items grouped by category.

    Categories considered: Starter, Main Course, Dessert, Drink.

    Template:
        menu.html
    """
    categories = ["starter", "main", "dessert", "drink"]
    menu_items = {cat: MenuItem.objects.filter(category=cat, available=True)
                  for cat in categories}
    return render(request, "menu.html", {"menu_items": menu_items})


def superuser_required(view_func):
    """
    Decorator to restrict access to superusers only.
    """
    return user_passes_test(lambda u: u.is_superuser)(view_func)


@superuser_required
def superuser_menu(request):
    """
    Display a table of all menu items for superusers.

    Shows:
        - Name, description, price, category, availability
        - Actions: edit and delete

    Template:
        superuser_menu.html
    """
    items = MenuItem.objects.all().order_by('category', 'name')
    return render(request, 'superuser_menu.html', {'items': items})


@superuser_required
def add_menu_item(request):
    """
    Allow a superuser to add a new menu item.

    Handles:
        - GET: show empty form
        - POST: validate and save form

    Template:
        menu_item_form.html
    """
    if request.method == 'POST':
        form = MenuItemForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, "Menu item added successfully.")
            return redirect('superuser_menu')
    else:
        form = MenuItemForm()
    return render(request, 'menu_item_form.html',
                  {'form': form, 'title': 'Add Menu Item'})


@superuser_required
def edit_menu_item(request, item_id):
    """
    Allow a superuser to edit an existing menu item.

    Parameters:
        item_id (int): ID of the MenuItem to edit

    Handles:
        - GET: show form prefilled with current item data
        - POST: validate and save updates

    Template:
       menu_item_form.html
    """
    item = get_object_or_404(MenuItem, id=item_id)
    if request.method == 'POST':
        form = MenuItemForm(request.POST, instance=item)
        if form.is_valid():
            form.save()
            messages.success(request, "Menu item updated successfully.")
            return redirect('superuser_menu')
    else:
        form = MenuItemForm(instance=item)
    return render(request, 'menu_item_form.html',
                  {'form': form, 'title': 'Edit Menu Item'})


@superuser_required
def delete_menu_item(request, item_id):
    """
    Allow a superuser to delete a menu item.

    Parameters:
        item_id (int): ID of the MenuItem to delete

    Handles:
        - GET: show confirmation page
        - POST: delete item and redirect to menu management

    Template:
        menu_item_confirm_delete.html
    """
    item = get_object_or_404(MenuItem, id=item_id)
    if request.method == 'POST':
        item.delete()
        messages.success(request, "Menu item deleted successfully.")
        return redirect('superuser_menu')
    return render(request, 'menu_item_confirm_delete.html', {'item': item})
