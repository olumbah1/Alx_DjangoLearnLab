from django.urls import path
from .views import (
    PostListCreateAPIView,
    PostDetailAPIView,
    PostLikeAPIView,
    PostUnlikeAPIView,
    FeedAPIView,
    PersonalFeedAPIView,
    CommentListCreateAPIView
)

urlpatterns = [
    path('posts/', PostListCreateAPIView.as_view(), name='post-list-create'),
    path('posts/<int:pk>/', PostDetailAPIView.as_view(), name='post-detail'),
    path('posts/<int:pk>/like/', PostLikeAPIView.as_view(), name='post-like'),
    path('posts/<int:pk>/unlike/', PostUnlikeAPIView.as_view(), name='post-unlike'),
    path('posts/feed/', FeedAPIView.as_view(), name='post-feed'),
    path('posts/personal-feed/', PersonalFeedAPIView.as_view(), name='personal-feed'),
    
    path('comments/', CommentListCreateAPIView.as_view(), name='comment-list-create'),
]

