
from django.conf import settings
from django.urls import path
from django.conf.urls.static import static
from django.contrib import admin

from forum.attachments.views import upload

app_name = 'attachments'

urlpatterns = [
    path('', upload, name='upload_img'),  
] 
