from django.contrib import admin
from django.urls import path
from posts.views import (
    home_view, create_post, single_post_view, delete_single_post,
    edit_post, like_post, like_comment, edit_comment, delete_comment
)
from accounts.views import *

urlpatterns = [
    path("admin/", admin.site.urls),
    path("", home_view, name="list_post"),
    path("create/", create_post, name="create_post"),
    path("signup/", signup_view, name="signup"),
    path("login/", login_view, name="login"),
    path("logout/", logout_view, name="logout"),
    path("profile/", user_profile_view, name="user_details"),
    path("profile/<int:id>/", user_profile_view, name="user_profile"),
    path("edit_profile/", edit_profile_view, name="edit_profile"),
    path("post/<int:post_id>/", single_post_view, name="single_post"),
    path("post/<int:post_id>/delete/", delete_single_post, name="delete_post"),
    path("post/<int:post_id>/edit/", edit_post, name="edit_post"),
    path("post/<int:post_id>/comment/<int:comment_id>/edit/", edit_comment, name="edit_comment"),
    path("post/<int:post_id>/comment/<int:comment_id>/delete/", delete_comment, name="delete_comment"),
    path('posts/<int:post_id>/like/', like_post, name='like_post'),
    path('comments/<int:comment_id>/like/', like_comment, name='like_comment'),
]
