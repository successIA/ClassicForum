from django.urls import path, re_path

from .views import (
    create_moderator,
    delete_moderator,
    hide_comment,
    hide_thread,
    moderator_detail,
    moderator_list,
    unhide_comment,
    unhide_thread,
    update_moderator,
)

app_name = "moderation"

urlpatterns = [
    path("add/", create_moderator, name="moderator_create"),
    re_path(
        r"^(?P<username>[\w-]+)/detail/$", moderator_detail, name="moderator_detail"
    ),
    re_path(r"^(?P<username>[\w-]+)/edit/$", update_moderator, name="moderator_update"),
    re_path(
        r"^(?P<username>[\w-]+)/delete/$", delete_moderator, name="moderator_delete"
    ),
    path("list/", moderator_list, name="moderator_list"),
    re_path(r"^topics/(?P<slug>[\w-]+)/hide/$", hide_thread, name="thread_hide"),
    re_path(r"^topics/(?P<slug>[\w-]+)/unhide/$", unhide_thread, name="thread_unhide"),
    re_path(
        r"^topics/(?P<thread_slug>[\w-]+)/(?P<comment_pk>[\w-]+)/hide/$",
        hide_comment,
        name="comment_hide",
    ),
    re_path(
        r"^topics/(?P<thread_slug>[\w-]+)/(?P<comment_pk>[\w-]+)/unhide/$",
        unhide_comment,
        name="comment_unhide",
    ),
]
