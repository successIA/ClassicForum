from django.conf import settings
from django.urls import include, path, re_path
from django.conf.urls.static import static
from django.contrib import admin

import debug_toolbar

from forum.threads.views import (
    follow_thread,
    thread_detail,
    thread_list,
    update_thread,
)

urlpatterns = [
    path('__debug__/', include(debug_toolbar.urls)),

    path('', thread_list, name='home'),
    path('categories/', include('forum.categories.urls', namespace='categories')),
    path('threads/', include('forum.threads.urls', namespace='threads')),
    path('accounts/', include('forum.accounts.urls', namespace='accounts')),
    re_path(r'^(?P<thread_slug>[\w-]+)/follow/$', follow_thread, name='thread_follow'),
    re_path(r'^topics/(?P<thread_slug>[\w-]+)/$', thread_detail, name='thread_detail'),
    re_path(r'^topics/(?P<thread_slug>[\w-]+)/edit/$', update_thread, name='thread_update'),
    re_path(r'^topics/(?P<thread_slug>[\w-]+)/comments/', include('forum.comments.urls', namespace='comments')),
    path('upload/', include('forum.attachments.urls', namespace='attachments')),

    path('search/', include('forum.search.urls', namespace='search')),
    path('moderation/', include('forum.moderation.urls', namespace='moderation')),
    re_path(settings.ADMIN_URL, admin.site.urls),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
