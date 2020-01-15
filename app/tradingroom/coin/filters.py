from django import forms
from django.db.models import Q
from django.utils.translation import npgettext, pgettext_lazy
from django_filters import (
    CharFilter,
    ChoiceFilter,
    DateFromToRangeFilter,
    ModelMultipleChoiceFilter,
    OrderingFilter,
    RangeFilter,
)

from ...core.filters import SortedFilterSet
from ...coin.models import Coin
from ...product.models import Category
from ..widgets import DateRangeWidget

SORT_BY_FIELDS_COIN = {
    "name": pgettext_lazy("Coin list sorting option", "name"),
    "value": pgettext_lazy("Coin list sorting option", "value"),
    "start_date": pgettext_lazy("Coin list sorting option", "start_date"),
    "end_date": pgettext_lazy("Coin list sorting option", "end_date"),
}


def filter_by_date_range(queryset, name, value):
    q = Q()
    if value.start:
        q = Q(start_date__gte=value.start)
    if value.stop:
        if value.start:
            q |= Q(end_date__lte=value.stop)
        else:
            q = Q(end_date__lte=value.stop)
    return queryset.filter(q)


class CoinFilter(SortedFilterSet):
    name = CharFilter(
        label=pgettext_lazy("Coin list filter label", "Name"), lookup_expr="icontains"
    )
    categories = ModelMultipleChoiceFilter(
        label=pgettext_lazy("Coin list filter label", "Categories"),
        field_name="categories",
        queryset=Category.objects.all(),
    )
    type = ChoiceFilter(
        label=pgettext_lazy("Coin list filter label", "Discount type"),
        empty_label=pgettext_lazy("Filter empty choice label", "All"),
        widget=forms.Select,
    )
    value = RangeFilter(label=pgettext_lazy("Coin list filter label", "Value"))
    date = DateFromToRangeFilter(
        label=pgettext_lazy("Coin list sorting filter label", "Period of validity"),
        field_name="created",
        widget=DateRangeWidget,
        method=filter_by_date_range,
    )
    sort_by = OrderingFilter(
        label=pgettext_lazy("Coin list filter label", "Sort by"),
        fields=SORT_BY_FIELDS_COIN.keys(),
        field_labels=SORT_BY_FIELDS_COIN,
    )

    class Meta:
        model = Coin
        fields = []

    def get_summary_message(self):
        counter = self.qs.count()
        return npgettext(
            "Number of matching records in the tradingroom coins list",
            "Found %(counter)d matching coin",
            "Found %(counter)d matching coins",
            number=counter,
        ) % {"counter": counter}
