# Generated by Django 2.0.8 on 2018-09-11 06:09

import django.utils.timezone
from django.conf import settings
from django.contrib.postgres import fields
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ("order", "0052_auto_20180822_0720"),
    ]

    operations = [
        migrations.CreateModel(
            name="OrderEvent",
            fields=[
                (
                    "id",
                    models.AutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                (
                    "date",
                    models.DateTimeField(
                        default=django.utils.timezone.now, editable=False
                    ),
                ),
                (
                    "type",
                    models.CharField(
                        choices=[
                            ("PLACED", "placed"),
                            ("PLACED_FROM_DRAFT", "draft_placed"),
                            ("ORDER_MARKED_AS_PAID", "marked_as_paid"),
                            ("CANCELED", "canceled"),
                            ("ORDER_FULLY_PAID", "order_paid"),
                            ("UPDATED", "updated"),
                            ("EMAIL_SENT", "email_sent"),
                            ("PAYMENT_CAPTURED", "captured"),
                            ("PAYMENT_REFUNDED", "refunded"),
                            ("PAYMENT_RELEASED", "released"),
                            ("FULFILLMENT_CANCELED", "fulfillment_canceled"),
                            ("FULFILLMENT_RESTOCKED_ITEMS", "restocked_items"),
                            ("FULFILLMENT_FULFILLED_ITEMS", "fulfilled_items"),
                            ("NOTE_ADDED", "note_added"),
                            ("OTHER", "other"),
                        ],
                        max_length=255,
                    ),
                ),
                ("parameters", fields.JSONField(blank=True, default=dict)),
                (
                    "order",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="events",
                        to="order.Order",
                    ),
                ),
                (
                    "user",
                    models.ForeignKey(
                        blank=True,
                        null=True,
                        on_delete=django.db.models.deletion.SET_NULL,
                        related_name="+",
                        to=settings.AUTH_USER_MODEL,
                    ),
                ),
            ],
            options={"ordering": ("date",)},
        )
    ]
