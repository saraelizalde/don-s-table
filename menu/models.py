"""
Models for the Menu app.

Defines the MenuItem model representing individual menu items in the restaurant.
"""

from django.db import models

class MenuItem(models.Model):
    """
    Represents a single item on the restaurant menu.

    Meta:
        ordering: Items are ordered by category, then by name.
    """
    CATEGORY_CHOICES = [
        ('starter', 'Starter'),
        ('main', 'Main Course'),
        ('dessert', 'Dessert'),
        ('drink', 'Drink'),
    ]

    name = models.CharField(max_length=100)
    description = models.TextField(blank=True, null=True)
    price = models.DecimalField(max_digits=6, decimal_places=2)
    category = models.CharField(max_length=20, choices=CATEGORY_CHOICES)
    available = models.BooleanField(default=True)

    def __str__(self):
        """Return a string representation including name and price."""
        return f"{self.name} - {self.price}€"

    class Meta:
        ordering = ['category', 'name']