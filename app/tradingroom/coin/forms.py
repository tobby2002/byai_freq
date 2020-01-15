from django import forms
from django.conf import settings
from django.urls import reverse_lazy
from django.utils.translation import pgettext_lazy
from ...core.utils.promo_code import generate_promo_code
from ...coin.models import Coin


class CoinForm(forms.ModelForm):
    class Meta:
        model = Coin
        exclude = [
            "min_amount_spent",
            "countries",
            "products",
            "collections",
            "categories",
            "used",
        ]
        labels = {
            "type": pgettext_lazy("Discount type", "Discount type"),
            "name": pgettext_lazy("Item name", "Name"),
            "code": pgettext_lazy("Coupon code", "Code"),
            "usage_limit": pgettext_lazy("Usage limit", "Usage limit"),
            "min_checkout_items_quantity": pgettext_lazy(
                "Voucher: discount with", "Minimal quantity of products"
            ),
            "start_date": pgettext_lazy("Voucher date restrictions", "Start date"),
            "end_date": pgettext_lazy("Voucher date restrictions", "End date"),
            "discount_value_type": pgettext_lazy(
                "Discount type of the voucher", "Discount type"
            ),
            "discount_value": pgettext_lazy(
                "Discount value of the voucher", "Discount value"
            ),
        }

    def __init__(self, *args, **kwargs):
        initial = kwargs.get("initial", {})
        instance = kwargs.get("instance")
        if instance and instance.id is None and not initial.get("code"):
            initial["code"] = generate_promo_code()
        kwargs["initial"] = initial
        super().__init__(*args, **kwargs)
