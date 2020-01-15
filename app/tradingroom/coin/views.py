from django.conf import settings
from django.contrib import messages
from django.contrib.auth.decorators import permission_required
from django.db.models import Q
from django.http import JsonResponse
from django.shortcuts import get_object_or_404, redirect
from django.template.response import TemplateResponse
from django.utils import timezone
from django.utils.translation import pgettext_lazy

from ...core.utils import get_paginator_items
from ...coin.models import Coin

from . import forms
from .filters import CoinFilter


@permission_required("discount.manage_discounts")
def coin_list(request):
    coins = Coin.objects.prefetch_related("products").order_by("name")
    coin_filter = CoinFilter(request.GET, queryset=coins)
    coins = get_paginator_items(
        coin_filter.qs, settings.DASHBOARD_PAGINATE_BY, request.GET.get("page")
    )
    ctx = {
        "coins": coins,
        "filter_set": coin_filter,
        "is_empty": not coin_filter.queryset.exists(),
    }
    return TemplateResponse(request, "tradingroom/coin/list.html", ctx)



@permission_required("discount.manage_discounts")
def coin_add(request):
    coin = Coin()
    form = forms.CoinForm(request.POST or None, instance=coin)
    if form.is_valid():
        coin = form.save()
        msg = pgettext_lazy("Coin (discount) message", "Added coin")
        messages.success(request, msg)
        return redirect("tradingroom:coin-update", pk=coin.pk)
    ctx = {"coin": coin, "form": form}
    return TemplateResponse(request, "tradingroom/coin/form.html", ctx)



@permission_required("discount.manage_discounts")
def coin_edit(request, pk):
    coin = get_object_or_404(Coin, pk=pk)
    form = forms.CoinForm(request.POST or None, instance=coin)
    if form.is_valid():
        coin = form.save()
        msg = pgettext_lazy("Coin (discount) message", "Updated coin")
        messages.success(request, msg)
        return redirect("tradingroom:coin-update", pk=coin.pk)
    ctx = {"coin": coin, "form": form}
    return TemplateResponse(request, "tradingroom/coin/form.html", ctx)



@permission_required("discount.manage_discounts")
def coin_delete(request, pk):
    instance = get_object_or_404(Coin, pk=pk)
    if request.method == "POST":
        instance.delete()
        msg = pgettext_lazy("Coin (discount) message", "Removed coin %s") % (
            instance.name,
        )
        messages.success(request, msg)
        return redirect("tradingroom:coin-list")
    ctx = {"coin": instance}
    return TemplateResponse(
        request, "tradingroom/coin/modal/confirm_delete.html", ctx
    )
