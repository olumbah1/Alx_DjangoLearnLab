from django.urls import path
from . import views
from .views import (PostListView, 
                    PostDetailView, 
                    PostCreateView,
                    PostUpdateView,
                    PostDeleteView,
                    CommentCreateView,
                    CommentUpdateView,
                    CommentDeleteView,
    
                    )

urlpatterns = [
    # Account Views URL
    path('register/', views.register_view, name='register'),
    path('login/', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),
    path('profile/', views.profile_view, name='profile'),
    path('profile/update/', views.profile_update_view, name='profile-update'),
    
    path('search/', views.search_posts, name='search-posts'),
    path('tags/<str:tag_name>/', views.posts_by_tag, name='posts-by-tag'),

    # Post CRUD Views URL
    path('posts', PostListView.as_view(), name='post-list'),
    path('post/<int:pk>/', PostDetailView.as_view(), name='post-detail'),
    path('post/new/', PostCreateView.as_view(), name='post-create'),
    path('post/<int:pk>/update/', PostUpdateView.as_view(), name='post-update'),
    path('post/<int:pk>/delete/', PostDeleteView.as_view(), name='post-delete'),
    
    # Comment CRUD Views URL.
    path('post/<int:pk>/comments/new/', CommentCreateView.as_view(), name='comment-create'),
    path('comment/<int:pk>/update/', CommentUpdateView.as_view(), name='comment-update'),
    path('comment/<int:pk>/delete/', CommentDeleteView.as_view(), name='comment-delete'),
    
    
]    
