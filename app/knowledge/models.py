from decimal import Decimal
from functools import partial

from django.conf import settings
from django.urls import reverse
from django.utils.text import slugify
from django.db import models
from django.db.models import F, Q
from django.utils import timezone
from django.utils.translation import pgettext, pgettext_lazy
from prices import Money, fixed_discount, percentage_discount

from ..core.utils.translations import TranslationProxy
from dynamic_models.models import AbstractModelSchema, AbstractFieldSchema

class ModelSchema(AbstractModelSchema):
    pass

class FieldSchema(AbstractFieldSchema):
    pass

class KnowledgeQueryset(models.QuerySet):
    def active(self, date):
        return self.filter(
            Q(end_date__isnull=True) | Q(end_date__gte=date), start_date__lte=date
        )

    def expired(self, date):
        return self.filter(end_date__lt=date, start_date__lt=date)


class Knowledge(models.Model):
    name = models.CharField(max_length=255)
    description = models.TextField(max_length=1000)
    slug = models.SlugField(max_length=1000)

    translated = TranslationProxy()

    class Meta:
        app_label = "knowledge"
        permissions = (
            (
                "manage_discounts",
                pgettext_lazy("Permission description", "Manage sales and vouchers."),
            ),
        )

    def __repr__(self):
        return "Knowledge(name=%r, value=%r, type=%s)" % (
            str(self.name),
            self.value,
            self.get_type_display(),
        )

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse("manager:knowledge-update", kwargs={"slug": self.slug})

class KnowledgeTranslation(models.Model):
    language_code = models.CharField(max_length=10)
    name = models.CharField(max_length=255, null=True, blank=True)
    knowledge = models.ForeignKey(
        Knowledge, related_name="translations", on_delete=models.CASCADE
    )

    class Meta:
        unique_together = (("language_code", "knowledge"),)
