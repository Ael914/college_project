from django.test import TestCase
from .forms import CartAddProductForm


# Create your tests here.
class CartFormTestCase(TestCase):
    def test_quantity_label(self):
        form = CartAddProductForm()
        self.assertTrue(
            form.fields["quantity"].label == None
            or form.fields["quantity"].label == "Quantity"
        )

    def test_override_label(self):
        form = CartAddProductForm()
        self.assertTrue(form.fields["override"].label == None)
