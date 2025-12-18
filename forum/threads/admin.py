from django.contrib import admin
from django.contrib.contenttypes.admin import GenericTabularInline

from forum.comments.models import Comment
from forum.threads.models import Thread, ThreadFollowership, ThreadRevision


class ThreadRevisionInline(admin.TabularInline):
    model = ThreadRevision


class CommentInline(admin.TabularInline):
    model = Comment


@admin.register(Thread)
class ThreadAdmin(admin.ModelAdmin):
    inlines = [
        CommentInline
    ]


admin.site.register(ThreadRevision)
admin.site.register(ThreadFollowership)
