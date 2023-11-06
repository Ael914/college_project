from django.test import TestCase
from .models import Category, Product


# Create your tests here.
class ShopTestCase(TestCase):
    def setUp(self):
        category_kwargs = {"name": "Cars", "slug": "cars"}
        Category.objects.create(**category_kwargs)
        product_kwargs = {
            "name": "Car",
            "slug": "car",
            "description": "SuperMegaCar",
            "category": Category.objects.get(id=1),
            "price": 123.45,
            "available": True,
        }
        Product.objects.create(**product_kwargs)

    def test_product_category(self):
        category = Category.objects.get(id=1)
        product = Product.objects.get(id=1)
        self.assertEqual(product.category, category)
