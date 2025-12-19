from django.urls import re_path

from forum.search.views import search

app_name = "search"

urlpatterns = [
    re_path(r"^(?P<page>[\d]*)?/?$", search, name="search"),
]
