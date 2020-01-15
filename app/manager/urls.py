from django.conf.urls import include, url

from . import views as core_views
from .knowledge.urls import urlpatterns as knowledge_urls
from .search.urls import urlpatterns as search_urls


urlpatterns = [
    url(r"^$", core_views.index, name="index"),
    url(r"^knowledge/", include(knowledge_urls)),
    url(r"^search/", include(search_urls)),
]
