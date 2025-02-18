# social_app/api_urls.py

from django.urls import path
from . import views

urlpatterns = [
    path('posts/', views.PostListAPIView.as_view(), name='post-list-api'),
    path('posts/<int:pk>/', views.PostDetailAPIView.as_view(), name='post-detail-api'),

    path('comments/', views.CommentListAPIView.as_view(), name='comment-list-api'),
    path('comments/<int:pk>/', views.CommentDetailAPIView.as_view(), name='comment-detail-api'),

    path('forums/', views.ForumListAPIView.as_view(), name='forum-list-api'),
    path('forums/<int:pk>/', views.ForumDetailAPIView.as_view(), name='forum-detail-api'),

    path('forum-posts/', views.ForumPostListAPIView.as_view(), name='forum-post-list-api'),
    path('forum-posts/<int:pk>/', views.ForumPostDetailAPIView.as_view(), name='forum-post-detail-api'),

    path('media/', views.MediaListAPIView.as_view(), name='media-list-api'),
    path('media/<int:pk>/', views.MediaDetailAPIView.as_view(), name='media-detail-api'),
]