from django.conf import settings
from django.contrib.contenttypes.fields import GenericRelation
from django.urls import reverse
from django.db import models
from django.db.models import CharField, Count, F, Max, Min, Prefetch, Value
from django.utils.html import mark_safe
from django.utils.text import slugify

from hitcount.models import HitCount, HitCountMixin

from forum.accounts.utils import get_user_list_without_creator
from forum.categories.models import Category
from forum.core.bbcode_quote import bbcode_quote
from forum.core.constants import COMMENT_PER_PAGE
from forum.core.models import TimeStampedModel
from forum.notifications.models import Notification
from forum.threads.managers import ThreadQuerySet


class Thread(TimeStampedModel, HitCountMixin):
    title = models.CharField(max_length=150)
    slug = models.SlugField(blank=True, max_length=255)
    body = models.TextField(max_length=4000)
    category = models.ForeignKey(
        'categories.Category', on_delete=models.CASCADE
    )
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL, on_delete=models.CASCADE
    )
    likes = models.PositiveIntegerField(default=0)
    hit_counts  =  GenericRelation(
        HitCount, 
        object_id_field='object_pk',
        related_query_name='threads'
    )
    visible = models.BooleanField(default=True)
    followers = models.ManyToManyField(
        settings.AUTH_USER_MODEL,
        through='ThreadFollowership', 
        related_name='thread_following'
    )
    starting_comment = models.ForeignKey(
        'comments.Comment', on_delete=models.SET_NULL,
        blank=True, null=True, related_name='starting_thread'
    )
    final_comment_user = models.ForeignKey(
        settings.AUTH_USER_MODEL, on_delete=models.SET_NULL,
        blank=True, null=True, related_name='final_thread'
    )
    final_comment_time = models.DateTimeField(null=True, blank=True)
    comment_count = models.PositiveIntegerField(default=0)
    objects = ThreadQuerySet.as_manager()

    def __str__(self):
        return self.title

    def save(self, *args, **kwargs):
        if not self.pk:
            self.slug = self.__class__.objects.generate_slug(self)
        super(Thread, self).save(*args, **kwargs)

    def synchronise(self, comment, added=True):
        if comment:
            self.final_comment_user=comment.user
            self.final_comment_time=comment.created            
            if added:
                self.comment_count=F('comment_count') + 1
            else:
                self.comment_count=F('comment_count') - 1
        else:
            self.final_comment_user=None
            self.final_comment_time=self.starting_comment.created
            self.comment_count=0
        self.save(update_fields=[
            'final_comment_user', 'final_comment_time', 'comment_count'
        ])

    def set_starting_comment(self, comment):
        self.starting_comment=comment
        self.final_comment_time=comment.created
        self.save(update_fields=[
            'starting_comment', 'final_comment_time'
        ])

    def is_owner(self, user):
        return self.user == user

    def get_absolute_url(self):
        return reverse(
            'thread_detail', kwargs={'thread_slug': self.slug}
        )

    @staticmethod
    def get_precise_url(filter_str, page):
        return reverse(
            "threads:thread_list_filter",
            kwargs={'filter_str': filter_str, 'page': page}
        )
    
    def get_update_url(self):
        return reverse('thread_update', kwargs={'thread_slug': self.slug})

    def get_thread_update_form_action(self):
        return self.get_update_url()

    def get_comment_create_form_action(self, page_num):
        return '%s?page=%s#post-form' % (
            reverse(
                'comments:comment_create',
                kwargs={'thread_slug': self.slug}
            ),
            page_num
        )
      
    def get_thread_follow_url(self):
        return reverse('thread_follow', kwargs={'thread_slug': self.slug})
    
    def get_follow_url(self):
        return reverse('thread_follow', kwargs={'thread_slug': self.slug})


class ThreadFollowershipQuerySet(models.query.QuerySet):
    def get_instance_and_count(self, thread, user=None):
        qs = self.filter(thread=thread)
        instance = None
        count = 0
        if user:
            qs_user = qs.select_related('user', 'first_new_comment')
            for qs_item in qs_user:
                count += 1
                if user == qs_item.user:
                    instance = qs_item
            return instance, count
        else:
            return instance, qs.count()

    def toggle(self, user, thread):
        queryset = self.filter(user=user, thread=thread)
        if queryset:
            queryset[0].delete()
        else:
            self.create(user=user, thread=thread)
    
    def synchronise(self, thread, comment):
        qs = self.filter(thread=thread).select_related('user').all()
        user_list = [instance.user for instance in qs]
        if comment.user not in user_list:
            self.create(user=comment.user, thread=thread)
        if comment.user in user_list:
            user_list.remove(comment.user)
        self.filter(
            user__in=user_list, thread=thread,
        ).update(
            new_comment_count=F('new_comment_count') + 1
        )
        self.filter(
            user__in=user_list, thread=thread,
            first_new_comment__isnull=True
        ).update(
            first_new_comment=comment
        )


class ThreadFollowership(TimeStampedModel):
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL, on_delete=models.CASCADE
    )
    thread = models.ForeignKey('threads.Thread', on_delete=models.CASCADE)
    first_new_comment = models.ForeignKey(
        'comments.Comment', on_delete=models.CASCADE, blank=True, null=True
    )
    new_comment_count = models.PositiveIntegerField(default=0)
    objects = ThreadFollowershipQuerySet.as_manager()

    class Meta:
        verbose_name = "Thread Followership"
		
    def __str__(self):
        return f'{self.thread.title} - {self.user.username}'

    def update_comment_fields(self, comments):
        if not self.first_new_comment:
            return
        next_comment = self._get_next_first_new_comment(comments)
        count = self._get_next_new_comment_count(next_comment)
        self.__class__.objects.filter(
            user=self.user, thread=self.thread,
        ).update(first_new_comment=next_comment, new_comment_count=count)

    def _get_next_first_new_comment(self, comments):
        from forum.comments.models import Comment

        if comments.has_next():
            comment_qs = Comment.objects.filter(
                thread=self.thread,
                created__gt=self.first_new_comment.created
            ).exclude(is_starting_comment=True)[:COMMENT_PER_PAGE]
            if comment_qs:
                position = self._get_position_of_comment_in_page(comments)
                next_first_new_comment = comment_qs[COMMENT_PER_PAGE - position]
                return next_first_new_comment
            else:
                return None
        else:
            return None

    def _get_position_of_comment_in_page(self, comments):
        position = 0
        for comment in comments:
            position += 1
            if self.first_new_comment.pk == comment.pk:
                break
        return position

    def _get_next_new_comment_count(self, first_new_comment):
        if first_new_comment:
            index = first_new_comment.position + first_new_comment.offset
            next_new_comment_count = self.thread.comment_count - index + 1
            return next_new_comment_count
        else:
            return 0


class ThreadRevision(models.Model):
    thread = models.ForeignKey(
        Thread, on_delete=models.CASCADE, related_name="revisions"
    )
    starting_comment = models.ForeignKey(
        'comments.Comment', on_delete=models.SET_NULL,
        blank=True, null=True, related_name='starting_thread_revision'
    )
    title = models.TextField()
    message = models.TextField()
    marked_message = models.TextField(blank=True)
    created = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = "Thread Revision"

    def __str__(self):
        return 'Thread History-%s' % (self.created)
