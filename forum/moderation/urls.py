from django.urls import path

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
    path("<slug:username>/detail/", moderator_detail, name="moderator_detail"),
    path("<slug:username>/edit/", update_moderator, name="moderator_update"),
    path("<slug:username>/delete/", delete_moderator, name="moderator_delete"),
    path("list/", moderator_list, name="moderator_list"),
    path("topics/<slug:slug>/hide/", hide_thread, name="thread_hide"),
    path("topics/<slug:slug>/unhide/", unhide_thread, name="thread_unhide"),
    path(
        "topics/<slug:thread_slug>/<int:comment_pk>/hide/",
        hide_comment,
        name="comment_hide",
    ),
    path(
        "topics/<slug:thread_slug>/<int:comment_pk>/unhide/",
        unhide_comment,
        name="comment_unhide",
    ),
]
