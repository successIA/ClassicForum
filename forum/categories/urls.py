from django.urls import re_path

from forum.categories.views import category_detail
from forum.threads.views import create_thread

app_name = 'categories'

urlpatterns = [
    re_path(r'^(?P<slug>[\w-]+)/$', category_detail, name='category_detail'),

    re_path(
        r'(?P<slug>[\w-]+)/(?P<filter_str>[\w-]+)/(?P<page>[\d]*)?/create-thread/$',
        create_thread,
        name='category_thread_create'
    ),

    re_path(
        r'(?P<slug>[\w-]+)/(?P<filter_str>[\w-]+)/(?P<page>[\d]*)?/?$',
        category_detail,
        name='category_detail_filter'
    ),

]
