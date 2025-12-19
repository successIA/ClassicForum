from django.contrib.auth import views as auth_views
from django.urls import path, re_path, reverse_lazy

from forum.accounts.forms import UserPasswordChangeForm
from forum.accounts.views import (
    account_activation_sent,
    activate,
    follow_user,
    guest_signup,
    signup,
    user_comment_list,
    user_followers,
    user_following,
    user_mention,
    user_mention_list,
    user_notification_list,
    user_profile_edit,
    user_profile_stats,
    user_thread_list,
)

app_name = "accounts"

urlpatterns = [
    # authentication
    path(
        "account_activation_sent/",
        account_activation_sent,
        name="account_activation_sent",
    ),
    path(
        "activate/<uidb64>/<token>/",
        activate,
        name="activate",
    ),
    path("auth/signup/", signup, name="signup"),
    path("auth/guest-signup/", guest_signup, name="guest_signup"),
    path(
        "auth/login/",
        auth_views.LoginView.as_view(template_name="accounts/login.html"),
        name="login",
    ),
    path("auth/logout/", auth_views.LogoutView.as_view(), name="logout"),
    path(
        "auth/reset/",
        auth_views.PasswordResetView.as_view(
            template_name="accounts/password_reset.html",
            email_template_name="accounts/password_reset_email.html",
            subject_template_name="accounts/password_reset_subject.txt",
            success_url=reverse_lazy("accounts:password_reset_done"),
        ),
        name="password_reset",
    ),
    path(
        "auth/reset/done/",
        auth_views.PasswordResetDoneView.as_view(
            template_name="accounts/password_reset_done.html"
        ),
        name="password_reset_done",
    ),
    re_path(
        r"auth/reset/(?P<uidb64>[0-9A-Za-z_\-]+)/(?P<token>[0-9A-Za-z]{1,13}-[0-9A-Za-z]{1,20})/$",
        auth_views.PasswordResetConfirmView.as_view(
            template_name="accounts/password_reset_confirm.html",
            success_url=reverse_lazy("accounts:password_reset_complete"),
        ),
        name="password_reset_confirm",
    ),
    path(
        "auth/reset/complete/",
        auth_views.PasswordResetCompleteView.as_view(
            template_name="accounts/password_reset_complete.html"
        ),
        name="password_reset_complete",
    ),
    path(
        "auth/settings/password/",
        auth_views.PasswordChangeView.as_view(
            form_class=UserPasswordChangeForm,
            template_name="accounts/password_change.html",
            success_url=reverse_lazy("accounts:password_change_done"),
        ),
        name="password_change",
    ),
    path(
        "auth/settings/password/done/",
        auth_views.PasswordChangeDoneView.as_view(
            template_name="accounts/password_change_done.html"
        ),
        name="password_change_done",
    ),
    # userprofile
    path("users/mention/", user_mention, name="user_mention"),
    path("users/mention-list/", user_mention_list, name="user_mention_list"),
    re_path(
        r"(?P<username>[\w-]+)/(?P<filter_str>new)/(?P<page>[\d]*)?/?$",
        user_thread_list,
        name="thread_new",
    ),
    re_path(
        r"(?P<username>[\w-]+)/(?P<filter_str>following)/(?P<page>[\d]*)?/?$",
        user_thread_list,
        name="thread_following",
    ),
    re_path(
        r"(?P<username>[\w-]+)/(?P<filter_str>me)/(?P<page>[\d]*)?/?$",
        user_thread_list,
        name="thread_user",
    ),
    re_path(r"(?P<username>[\w-]+)/info/$", user_profile_edit, name="user_edit"),
    re_path(r"(?P<username>[\w-]+)/follow/$", follow_user, name="user_follow"),
    re_path(
        r"(?P<username>[\w-]+)/user-following/$", user_following, name="user_following"
    ),
    re_path(
        r"(?P<username>[\w-]+)/user-followers/$", user_followers, name="user_followers"
    ),
    re_path(
        r"(?P<username>[\w-]+)/comments/$", user_comment_list, name="user_comments"
    ),
    re_path(
        r"(?P<username>[\w-]+)/notifications/$",
        user_notification_list,
        name="user_notifs",
    ),
    re_path(r"(?P<username>[\w-]+)/$", user_profile_stats, name="user_stats"),
]
