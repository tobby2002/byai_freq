from django import forms
from django.conf import settings
from django.urls import reverse_lazy
from django.utils.translation import pgettext_lazy
from django_countries import countries
from django_prices.forms import MoneyField
from mptt.forms import TreeNodeMultipleChoiceField

from ...core.taxes import zero_money
from ...core.utils.promo_code import generate_promo_code
from ...discount import DiscountValueType
from ...knowledge.models import Knowledge
from ...product.models import Category, Product
from ..forms import AjaxSelect2MultipleChoiceField

MinAmountSpent = MoneyField(
    min_value=zero_money(),
    required=False,
    currency=settings.DEFAULT_CURRENCY,
    label=pgettext_lazy(
        "Lowest value for order to be able to use the voucher",
        "Apply only if the purchase value is greater than or equal to",
    ),
)


# class KnowledgeForm(forms.ModelForm):
class KnowledgeForm(forms.Form):
    # products = AjaxSelect2MultipleChoiceField(
    #     queryset=Product.objects.all(),
    #     fetch_data_url=reverse_lazy("dashboard:ajax-products"),
    #     required=False,
    #     label=pgettext_lazy("Discounted products", "Discounted products"),
    # )
    tax_rate = forms.CharField(
        required=False, label=pgettext_lazy("Product type tax rate type", "Tax rate")
    )

    # class Meta:
    #
    #     model = Knowledge
    #     exclude = []
    #     # labels = {
    #     #     "name": pgettext_lazy("Sale name", "Name"),
    #     #     "type": pgettext_lazy("Discount type", "Fixed or percentage"),
    #     #     "start_date": pgettext_lazy("Sale date restrictions", "Start date"),
    #     #     "end_date": pgettext_lazy("Sale date restrictions", "End date"),
    #     #     "value": pgettext_lazy("Percentage or fixed amount value", "Value"),
    #     #     "categories": pgettext_lazy(
    #     #         "Discounted categories", "Discounted categories"
    #     #     ),
    #     #     "collections": pgettext_lazy(
    #     #         "Discounted collections", "Discounted collections"
    #     #     ),
    #     # }
    #
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # if self.instance.pk:
        #     self.fields["products"].set_initial(self.instance.products.all())


    def clean(self):
        cleaned_data = super().clean()
        self.tax_rate = cleaned_data.get("tax_rate")
        # self.description = cleaned_data.get("description")
        # self.slug = cleaned_data.get("slug")
        # if not any([self.tax_rate, self.description, self.slug]):
        if not any([self.tax_rate]):
            self.add_error(
                    "tax_rate--",
                    pgettext_lazy("Knowledge error", "Knowledge fill all..."),
                )
            raise forms.ValidationError(
                pgettext_lazy(
                    "Knowledge (discount) error",
                    "A single Knowledge must point to at least one name, description"
                    "and/or slug.",
                )
            )
        # if discount_type == DiscountValueType.PERCENTAGE and value > 100:
        #     self.add_error(
        #         "value",
        #         pgettext_lazy("Sale (discount) error", "Sale cannot exceed 100%"),
        #     )
        # products = cleaned_data.get("products")
        # categories = cleaned_data.get("categories")
        # collections = cleaned_data.get("collections")
        # if not any([products, categories, collections]):
        #     raise forms.ValidationError(
        #         pgettext_lazy(
        #             "Sale (discount) error",
        #             "A single sale must point to at least one product, collection"
        #             "and/or category.",
        #         )
        #     )
        return cleaned_data

class ExtendedForm(forms.Form):
    pass
