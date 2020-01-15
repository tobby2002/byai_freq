from dataclasses import dataclass
from typing import Any, List

from django.conf import settings
from django.utils.translation import pgettext_lazy


class KnowledgeValueType:
    FIXED = "fixed"
    PERCENTAGE = "percentage"

    CHOICES = [
        (FIXED, pgettext_lazy("Knowledge type", settings.DEFAULT_CURRENCY)),
        (PERCENTAGE, pgettext_lazy("Knowledge type", "%")),
    ]
