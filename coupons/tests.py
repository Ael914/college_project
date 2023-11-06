import datetime

from django.test import TestCase
from django.utils import timezone

from .forms import CouponApplyForm
from .models import Coupon


# Create your tests here.
class CouponTestCase(TestCase):
    def setUp(self):
        kwargs = {
            "code": "TEST",
            "valid_from": timezone.now(),
            "valid_to": timezone.now() + datetime.timedelta(weeks=4),
            "discount": 50,
            "active": True,
        }
        Coupon.objects.create(**kwargs)

    def test_check_valid_28_days(self):
        coupon = Coupon.objects.get(id=1)
        self.assertEqual((coupon.valid_to - coupon.valid_from).days, 28)

    def test_valid_to_label(self):
        coupon = Coupon.objects.get(id=1)
        field_label = coupon._meta.get_field("valid_to").verbose_name
        self.assertEqual(field_label, "valid to")

    def test_valid_from_label(self):
        coupon = Coupon.objects.get(id=1)
        field_label = coupon._meta.get_field("valid_from").verbose_name
        self.assertEqual(field_label, "valid from")


class CouponApplyFormTestCase(TestCase):
    def test_form_code_label(self):
        form = CouponApplyForm()
        self.assertTrue(
            form.fields["code"].label == None or form.fields["code"].label == "Coupon"
        )
