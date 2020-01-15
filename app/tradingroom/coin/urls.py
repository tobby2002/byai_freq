from django.conf.urls import url

from . import views

urlpatterns = [
    url(r"coin/$", views.coin_list, name="coin-list"),
    url(r"coin/add/$", views.coin_add, name="coin-add"),
    url(r"coin/(?P<pk>[0-9]+)/$", views.coin_edit, name="coin-update"),
    url(r"coin/(?P<pk>[0-9]+)/delete/$", views.coin_delete, name="coin-delete"),
]
