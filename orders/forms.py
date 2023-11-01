from django import forms
from django.utils.translation import gettext_lazy as _
from localflavor.us.forms import USZipCodeField

from .models import Order


class OrderCreateForm(forms.ModelForm):
    postal_code = USZipCodeField(label=_("Postal code"))

    class Meta:
        model = Order
        fields = ["first_name", "last_name", "email", "address", "postal_code", "city"]
