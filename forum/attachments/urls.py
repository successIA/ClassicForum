from django.urls import path

from forum.attachments.views import upload

app_name = "attachments"

urlpatterns = [
    path("", upload, name="upload_img"),
]
