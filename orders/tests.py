from django.test import TestCase

from .forms import OrderCreateForm
from .models import Order


# Create your tests here.
class OrderLabelsTestCase(TestCase):
    def setUp(self):
        kwargs = {
            "first_name": "John",
            "last_name": "Eirikson",
            "email": "email123@gmail.com",
            "address": "Street №1",
            "postal_code": "12345",
            "city": "Moscow",
        }
        Order.objects.create(**kwargs)

    def test_check_first_name_label(self):
        order = Order.objects.get(id=1)
        field_label = order._meta.get_field("first_name").verbose_name
        self.assertEqual(field_label, "first name")

    def test_check_last_name_label(self):
        order = Order.objects.get(id=1)
        field_label = order._meta.get_field("last_name").verbose_name
        self.assertEqual(field_label, "last name")

    def test_check_postal_code_label(self):
        order = Order.objects.get(id=1)
        field_label = order._meta.get_field("postal_code").verbose_name
        self.assertEqual(field_label, "postal code")

    def test_check_object_name(self):
        order = Order.objects.last()
        self.assertEqual(str(order), f"Order {order.id}")


class OrderCreateFormTestCase(TestCase):
    def test_form_first_name_label(self):
        form = OrderCreateForm()
        self.assertTrue(
            form.fields["first_name"].label == None
            or form.fields["first_name"].label == "First name"
        )

    def test_form_last_name_label(self):
        form = OrderCreateForm()
        self.assertTrue(
            form.fields["last_name"].label == None
            or form.fields["last_name"].label == "Last name"
        )

    def test_form_postal_code_label(self):
        form = OrderCreateForm()
        self.assertTrue(
            form.fields["postal_code"].label == None
            or form.fields["postal_code"].label == "Postal code"
        )
