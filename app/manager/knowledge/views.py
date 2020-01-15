from django.conf import settings
from django.contrib import messages
from django.contrib.auth.decorators import permission_required
from django.db.models import Q
from django.http import JsonResponse
from django.shortcuts import get_object_or_404, redirect
from django.template.response import TemplateResponse
from django.utils import timezone
from django.utils.translation import pgettext_lazy
from django import forms as fm

from ...core.utils import get_paginator_items
from ...knowledge.models import Knowledge, ModelSchema, FieldSchema
# from ...knowledge.models import ModelSchema, FieldSchema
from ..views import staff_member_required
from . import forms
from .forms import ExtendedForm
from .filters import SaleFilter
from .sparql import _class_prop_fetch, _class_label_comment_fetch


@staff_member_required
@permission_required("discount.manage_discounts")
def knowledge_list(request):
    knowledge_filter = []
    is_empty = False
    ctx = {
        # "knowledge": _class_prop_fetch(),
        "knowledge": _class_label_comment_fetch(),
        "filter_set": knowledge_filter,
        # "is_empty": not knowledge_filter.queryset.exists(),
        "is_empty": not is_empty,
    }
    return TemplateResponse(request, "manager/knowledge/list.html", ctx)


@staff_member_required
@permission_required("discount.manage_discounts")
def knowledge_add(request):
    print('add...')
    # knowledge_model_schema = ModelSchema.objects.create(name='knowledge')
    # knowledge = knowledge_model_schema.as_model()
    # knowledge = Knowledge()
    form = forms.KnowledgeForm(request.POST or None)
    if form.is_valid():
        # knowledge = form.save()
        msg = pgettext_lazy("Sale (discount) message", "Added knowledge")
        messages.success(request, msg)
        return redirect("manager:knowledge-update", pk=1)
    ctx = {"knowledge": None, "form": form}
    return TemplateResponse(request, "manager/knowledge/form.html", ctx)






@staff_member_required
@permission_required("discount.manage_discounts")
def knowledge_edit(request, slug):
    # knowledge = get_object_or_404(Knowledge, pk=1)
    # form = forms.KnowledgeForm(request.POST or None, instance=knowledge)

    # knowledge = Knowledge()


    # int_rate = knowledge.Meta.

    new_fields = {
        'cheese': fm.CharField(),
        'ketchup': fm.CharField()}

    DynamicExtendedForm = type('DynamicExtendedForm', (ExtendedForm,), new_fields)

    form = forms.KnowledgeForm(request.POST or None)

    if form.is_valid():
        # knowledge = form.save()
        msg = pgettext_lazy("Knowledge message", "Updated knowledge")
        messages.success(request, msg)

        kdata = {
            'name': form.name,
            'description': form.description,
            'slug': form.slug
        }
        ctx = {"knowledge": kdata, "form": form, "exform": DynamicExtendedForm}
        return TemplateResponse(request, "manager/knowledge/form.html", ctx)
        # return redirect("manager:knowledge-update", pk=knowledge.pk)
    # kdata = {
    #     'name': None,
    #     'description': None,
    #     'slug': None
    # }
    kdata = None
    print('slug:', slug)
    ctx = {"knowledge": kdata, "form": form, "exform": DynamicExtendedForm}
    return TemplateResponse(request, "manager/knowledge/form.html", ctx)


@staff_member_required
@permission_required("discount.manage_discounts")
def knowledge_delete(request, pk):
    instance = get_object_or_404(Sale, pk=pk)
    if request.method == "POST":
        instance.delete()
        msg = pgettext_lazy("Sale (discount) message", "Removed knowledge %s") % (
            instance.name,
        )
        messages.success(request, msg)
        return redirect("dashboard:knowledge-list")
    ctx = {"knowledge": instance}
    return TemplateResponse(
        request, "manager/knowledge/modal/confirm_delete.html", ctx
    )


@staff_member_required
@permission_required("discount.manage_discounts")
def ajax_voucher_list(request):
    queryset = Voucher.objects.active(date=timezone.now())

    search_query = request.GET.get("q", "")
    if search_query:
        queryset = queryset.filter(Q(name__icontains=search_query))

    vouchers = [{"id": voucher.pk, "text": str(voucher)} for voucher in queryset]
    return JsonResponse({"results": vouchers})
