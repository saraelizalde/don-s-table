from django import forms
from .models import MenuItem

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
    class Meta:
        model = MenuItem
        fields = ['name', 'description', 'price', 'category', 'available']
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control'}),
            'description': forms.Textarea(attrs={'class': 'form-control', 'rows': 3}),
            'price': forms.NumberInput(attrs={'class': 'form-control'}),
            'category': forms.Select(attrs={'class': 'form-control'}),
            'available': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
        }
