from django.urls import path
from . import views

urlpatterns = [
    path('posts/<int:post_id>/like/', views.like_post, name='like_post'),
    path('comments/<int:comment_id>/like/', views.like_comment, name='like_comment'),
]