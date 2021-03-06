from django.conf.urls import url

from forum.threads.views import create_thread, thread_list

app_name = 'threads'

urlpatterns = [    
    url(r'^$', thread_list, name='thread_list'),
    url(r'(?P<filter_str>[\w-]+)/(?P<page>[\d]*)?/create/$', create_thread, name='thread_create'),
    url(r'(?P<filter_str>[\w-]+)/(?P<page>[\d]*)?/?$', thread_list, name='thread_list_filter'),
]
