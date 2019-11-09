
from django.db.models import Max, Min, Count, F, Value, CharField, Prefetch
from django.db import models


class CommentQuerySet(models.query.QuerySet):

    def get_new_for_user(self, user, thread, time):
        if not user.is_authenticated:
            return
        if not time:
            return
        queryset = self.filter(thread=thread, created__gt=time)
        return queryset.exclude(user=user)

    def get_for_thread(self, thread):
        queryset = self.active().get_related().filter(thread=thread)
        return queryset.order_by('created').all()

    def get_user_last_posted(self, user):
        queryset = self.filter(user=user)
        if queryset.count() > 0:
            return queryset.latest('created').created

    def get_user_active_category(self, user):
        if user.comment_set.count() > 0:
            return self.values('thread').filter(
                user=user
            ).annotate(category=F('thread__category__title')).annotate(
                thread_count=Count('thread')
            ).order_by('-thread_count')[0].get('category')

    def get_recent_for_user(self, user, count):
        return self.get_related().filter(
            user=user
        ).exclude(is_starting_comment=True).order_by('-created')[:count]

    def get_user_total_upvotes(self, user):
        queryset = self.filter(user=user).annotate(upvotes=Count('upvoters'))
        total_upvotes = 0
        for model_instance in queryset:
            total_upvotes = total_upvotes + model_instance.upvotes
        return total_upvotes

    def get_related(self):
        return self.select_related(
            'thread', 'user', 'parent'
        ).prefetch_related(
            # # 'attachment_set',
            # 'user__userprofile__attachment_set',
            'revisions',
            'user__userprofile',
            'parent__user',
            'parent__thread',
            'upvoters',
            'downvoters'
        )

    def get_parent(self, pk):
        comment_qs = None
        try:
            comment_qs = self.filter(pk=int(pk))
        except:
            return None
        if comment_qs.exists():
            return comment_qs.first()

    def active(self, *args, **kwargs):
        return self.filter(visible=True)