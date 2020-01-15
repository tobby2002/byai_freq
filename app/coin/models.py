from decimal import Decimal
from functools import partial

from django.conf import settings
from django.db import models
from django.db.models import F, Q
from django.utils import timezone
from django.utils.translation import pgettext, pgettext_lazy
from prices import Money, fixed_discount, percentage_discount

from ..core.utils.translations import TranslationProxy
from . import CoinValueType

class CoinQueryset(models.QuerySet):
    def active(self, date):
        return self.filter(
            Q(end_date__isnull=True) | Q(end_date__gte=date), start_date__lte=date
        )

    def expired(self, date):
        return self.filter(end_date__lt=date, start_date__lt=date)


class Coin(models.Model):
    name = models.CharField(max_length=255)
    type = models.CharField(
        max_length=10,
        choices=CoinValueType.CHOICES,
        default=CoinValueType.FIXED,
    )
    value = models.DecimalField(
        max_digits=settings.DEFAULT_MAX_DIGITS,
        decimal_places=settings.DEFAULT_DECIMAL_PLACES,
        default=0,
    )
    products = models.ManyToManyField("product.Product", blank=True)
    categories = models.ManyToManyField("product.Category", blank=True)
    collections = models.ManyToManyField("product.Collection", blank=True)
    start_date = models.DateTimeField(default=timezone.now)
    end_date = models.DateTimeField(null=True, blank=True)

    objects = CoinQueryset.as_manager()
    translated = TranslationProxy()

    class Meta:
        app_label = "coin"
        permissions = (
            (
                "manage_discounts",
                pgettext_lazy("Permission description", "Manage sales and vouchers."),
            ),
        )

    def __repr__(self):
        return "Coin(name=%r, value=%r, type=%s)" % (
            str(self.name),
            self.value,
            self.get_type_display(),
        )

    def __str__(self):
        return self.name

    def get_discount(self):
        if self.type == CoinValueType.FIXED:
            discount_amount = Money(self.value, settings.DEFAULT_CURRENCY)
            return partial(fixed_discount, discount=discount_amount)
        if self.type == CoinValueType.PERCENTAGE:
            return partial(percentage_discount, percentage=self.value)
        raise NotImplementedError("Unknown discount type")


class CoinTranslation(models.Model):
    language_code = models.CharField(max_length=10)
    name = models.CharField(max_length=255, null=True, blank=True)
    coin = models.ForeignKey(
        Coin, related_name="translations", on_delete=models.CASCADE
    )

    class Meta:
        unique_together = (("language_code", "coin"),)
