from django.contrib import admin
from django.urls import path
from posts.views import *
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
]
