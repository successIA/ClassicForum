from django.contrib import admin

from forum.comments.models import Comment, CommentRevision


class CommentInline(admin.TabularInline):
    model = CommentRevision


@admin.register(Comment)
class CommentAdmin(admin.ModelAdmin):
    inlines = [
        CommentInline,
    ]
