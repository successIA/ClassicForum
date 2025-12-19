from django.urls import path, re_path

from forum.threads.views import create_thread, thread_list

app_name = "threads"

urlpatterns = [
    path("", thread_list, name="thread_list"),
    re_path(
        r"(?P<filter_str>[\w-]+)/(?P<page>[\d]*)?/create/$",
        create_thread,
        name="thread_create",
    ),
    re_path(
        r"(?P<filter_str>[\w-]+)/(?P<page>[\d]*)?/?$",
        thread_list,
        name="thread_list_filter",
    ),
]
