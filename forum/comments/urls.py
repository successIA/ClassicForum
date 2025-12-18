from django.urls import path

from forum.comments.views import (
    create_comment,
    like_comment,
    reply_comment,
    report_comment,
    update_comment,
)

app_name = 'comments'

urlpatterns = [
    path('<int:pk>/reply/', reply_comment, name='comment_reply'),
    path('<int:pk>/like/', like_comment, name='like'),
    path('<int:pk>/', update_comment, name='comment_update'),
    path('add/', create_comment, name='comment_create'),
    path('<int:pk>/report/', report_comment, name='report'),
]
