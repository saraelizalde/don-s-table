from django import forms
from .models import MenuItem
from django.core.validators import MinValueValidator


class MenuItemForm(forms.ModelForm):
    """
    Form for creating or editing a MenuItem.

    Fields:
        - name: Name of the menu item
        - description: Optional description
        - price: Decimal price
        - category: One of the predefined category choices
        - available: Boolean to mark if item is available
    """

    # Add a minimum value validator to ensure price is positive
    price = forms.DecimalField(
        max_digits=6,
        decimal_places=2,
        validators=[MinValueValidator(0.01)],
        widget=forms.NumberInput(attrs={'class': 'form-control'})
    )

    class Meta:
        model = MenuItem
        fields = ['name', 'description', 'price', 'category', 'available']
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control'}),
            'description':
            forms.Textarea(attrs={'class': 'form-control', 'rows': 3}),
            'category': forms.Select(attrs={'class': 'form-control'}),
            'available':
            forms.CheckboxInput(attrs={'class': 'form-check-input'}),
        }
