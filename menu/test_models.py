from django.test import TestCase
from .models import MenuItem

class TestMenuItemModel(TestCase):

    def setUp(self):
        self.item1 = MenuItem.objects.create(
            name="Bruschetta",
            description="Tasty bread with tomato",
            price=6.50,
            category="starter"
        )
        self.item2 = MenuItem.objects.create(
            name="Garlic Knots",
            description="Soft dough with garlic",
            price=5.50,
            category="starter"
        )

    def test_str_method(self):
        self.assertEqual(str(self.item1), "Bruschetta - 6.50€")

    def test_default_available(self):
        self.assertTrue(self.item1.available)

    def test_ordering(self):
        items = MenuItem.objects.all()
        self.assertEqual(items[0], self.item1)
        self.assertEqual(items[1], self.item2)
