from django.test import TestCase
from menu.forms import MenuItemForm


class TestMenuItemForm(TestCase):

    def test_form_is_valid(self):
        """Form should be valid with all required fields filled."""
        form_data = {
            'name': 'Margherita Pizza',
            'description': 'Classic pizza with tomato and mozzarella',
            'price': '12.50',
            'category': 'main',
            'available': True
        }
        form = MenuItemForm(data=form_data)
        self.assertTrue(form.is_valid(), msg='Form should be valid')

    def test_form_is_invalid_without_name(self):
        """Form should be invalid if the name is missing."""
        form_data = {
            'name': '',
            'description': 'Classic pizza with tomato and mozzarella',
            'price': '12.50',
            'category': 'main',
            'available': True
        }
        form = MenuItemForm(data=form_data)
        self.assertFalse(form.is_valid(), msg='Form is valid without a name')

    def test_form_is_invalid_without_price(self):
        """Form should be invalid if the price is missing."""
        form_data = {
            'name': 'Margherita Pizza',
            'description': 'Classic pizza with tomato and mozzarella',
            'price': '',
            'category': 'main',
            'available': True
        }
        form = MenuItemForm(data=form_data)
        self.assertFalse(form.is_valid(), msg='Form is valid without a price')

    def test_form_is_invalid_with_negative_price(self):
        """Form should be invalid if the price is negative."""
        form_data = {
            'name': 'Margherita Pizza',
            'description': 'Classic pizza with tomato and mozzarella',
            'price': '-5.00',
            'category': 'main',
            'available': True
        }
        form = MenuItemForm(data=form_data)
        self.assertFalse(form.is_valid(),
                         msg='Form is valid with negative price')
