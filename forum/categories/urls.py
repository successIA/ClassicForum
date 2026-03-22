from django.urls import path, re_path

from forum.categories.views import category_detail

app_name = "categories"

urlpatterns = [
    path("<slug:slug>/", category_detail, name="category_detail"),
    re_path(
        r"(?P<slug>[\w-]+)/(?P<filter_str>[\w-]+)/(?P<page>[\d]*)?/?$",
        category_detail,
        name="category_detail_filter",
    ),
]
