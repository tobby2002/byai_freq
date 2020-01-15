from django.conf.urls import url

from . import views

urlpatterns = [
    url(r"^$", views.knowledge_list, name="knowledge-list"),
    url(r"^add/$", views.knowledge_add, name="knowledge-add"),
    # url(r"^(?P<pk>[a-z0-9-_]+)/$", views.knowledge_edit, name="knowledge-update"),
    # url(r"^<slug>/$", views.knowledge_edit, name="knowledge-update"),
    # url(r"^(?P<slug>[a-zA-Z0-9-_]+?)/edit$", views.knowledge_edit, name="knowledge-update"),
    url(r"^(?P<slug>.+)/edit/$", views.knowledge_edit, name="knowledge-update"),
    # url(r"^(?P<pk>[a-z0-9-_]+?)/", views.knowledge_edit, name="knowledge-update"),
    # url(r"^edit/", views.knowledge_edit, name="knowledge-update"),
    url(r"^(?P<pk>[0-9]+)/delete/$", views.knowledge_delete, name="knowledge-delete"),
]
