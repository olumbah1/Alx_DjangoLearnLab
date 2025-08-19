from django.urls import path
from .views import (UserRegistrationView,
                    UserLoginView, 
                    UserProfileView, 
                    UserFollowersView, 
                    UserFollowingView, 
                    UserDetailView, 
                    FollowUserView, 
                    UnfollowUserView
                )


urlpatterns = [
    path('register/', UserRegistrationView.as_view(), name='register'),
    path('login/', UserLoginView.as_view(), name='login'),
    path('profile/', UserProfileView.as_view(), name='profile'),
    path('user/<str:username>/', UserDetailView.as_view(), name='user-detail'),
    
     # Follow management endpoints (using user_id as requested)
    path('follow/<int:user_id>/', FollowUserView.as_view(), name='follow-user'),
    path('unfollow/<int:user_id>/', UnfollowUserView.as_view(), name='unfollow-user'),
    
    # Followers/Following lists
    path('users/<int:user_id>/followers/', UserFollowersView.as_view(), name='user-followers'),
    path('users/<int:user_id>/following/', UserFollowingView.as_view(), name='user-following'),
]
