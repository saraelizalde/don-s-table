from django.contrib.auth.models import User
from django.urls import reverse
from django.test import TestCase
from .models import MenuItem
from .forms import MenuItemForm

class TestMenuCRUDViews(TestCase):

    def setUp(self):
        self.superuser = User.objects.create_superuser(
            username='admin', password='adminpass', email='admin@test.com'
        )
        self.item = MenuItem.objects.create(
            name='Bruschetta',
            description='Tasty bread with tomato',
            price=6.50,
            category='starter',
            available=True
        )

    def test_add_menu_item_view_get(self):
        """GET request renders the add menu item form."""
        self.client.login(username='admin', password='adminpass')
        response = self.client.get(reverse('add_menu_item'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'menu_item_form.html')
        self.assertIsInstance(response.context['form'], MenuItemForm)

    def test_add_menu_item_view_post(self):
        """POST request successfully adds a new menu item."""
        self.client.login(username='admin', password='adminpass')
        post_data = {
            'name': 'Garlic Knots',
            'description': 'Soft dough with garlic',
            'price': 5.50,
            'category': 'starter',
            'available': True
        }
        response = self.client.post(reverse('add_menu_item'), post_data)
        self.assertEqual(response.status_code, 302)
        self.assertTrue(MenuItem.objects.filter(name='Garlic Knots').exists())

    def test_edit_menu_item_view_get(self):
        """GET request renders the edit form prefilled."""
        self.client.login(username='admin', password='adminpass')
        response = self.client.get(reverse('edit_menu_item', args=[self.item.id]))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'menu_item_form.html')
        self.assertIsInstance(response.context['form'], MenuItemForm)
        self.assertEqual(response.context['form'].instance, self.item)

    def test_edit_menu_item_view_post(self):
        """POST request updates the menu item."""
        self.client.login(username='admin', password='adminpass')
        response = self.client.post(
            reverse('edit_menu_item', args=[self.item.id]),
            {'name': 'Updated Bruschetta',
             'description': 'Updated description',
             'price': 7.00,
             'category': 'starter',
             'available': True}
        )
        self.assertEqual(response.status_code, 302)
        self.item.refresh_from_db()
        self.assertEqual(self.item.name, 'Updated Bruschetta')

    def test_delete_menu_item_view(self):
        """POST request deletes a menu item."""
        self.client.login(username='admin', password='adminpass')
        response = self.client.post(reverse('delete_menu_item', args=[self.item.id]))
        self.assertEqual(response.status_code, 302)
        self.assertFalse(MenuItem.objects.filter(id=self.item.id).exists())
