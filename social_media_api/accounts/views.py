from rest_framework.authtoken.models import Token
from rest_framework import generics, status
from django.shortcuts import get_object_or_404
from .models import CustomUser
from rest_framework import permissions
from rest_framework.response import Response
from rest_framework.views import APIView
from .serializers import UserRegistrationSerializer, UserLoginSerializer, UserProfileSerializer, UserListSerializer
# Create your views here.

class UserRegistrationView(generics.CreateAPIView):
      queryset = CustomUser.objects.all()
      serializer_class = UserRegistrationSerializer
      permission_classes = [permissions.AllowAny]
      
      def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.save()
        token, created = Token.objects.get_or_create(user=user)
        return Response({
            'user': UserProfileSerializer(user).data,
            'token': token.key
        }, status=status.HTTP_201_CREATED)
      
class UserLoginView(APIView):
    permission_classes = [permissions.AllowAny]
    serializer_class = UserLoginSerializer
    def post(self, request):
        serializer = UserLoginSerializer(data=request.data)
        if serializer.is_valid():
            user = serializer.validated_data['user']
            token, created = Token.objects.get_or_create(user=user)
            return Response({
                'user': UserProfileSerializer(user).data,
                'token': token.key
            })
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
class UserProfileView(generics.RetrieveUpdateAPIView):
    serializer_class = UserProfileSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_object(self):
        return self.request.user
    
class UserDetailView(generics.RetrieveAPIView): #  """View to get any user's profile by username"""
    queryset = CustomUser.objects.all()
    serializer_class = UserProfileSerializer
    permission_classes = [permissions.IsAuthenticated]
    lookup_field = 'username'
    
class FollowUserView(generics.GenericAPIView):
    """Follow a user"""
    permission_classes = [permissions.IsAuthenticated]
    queryset = CustomUser.objects.all()
    lookup_url_kwarg = 'user_id'

    def post(self, request, user_id):
        user_to_follow = get_object_or_404(CustomUser, id=user_id)
        current_user = request.user
        
        # Check if trying to follow self
        if current_user == user_to_follow:
            return Response({
                'error': 'You cannot follow yourself'
            }, status=status.HTTP_400_BAD_REQUEST)
        
        # Check if already following
        if current_user.is_following(user_to_follow):
            return Response({
                'message': 'You are already following this user'
            }, status=status.HTTP_400_BAD_REQUEST)
        
        # Follow the user
        current_user.follow_user(user_to_follow)
        
        return Response({
            'message': f'You are now following {user_to_follow.username}',
            'following_count': current_user.following_count,
            'user_followers_count': user_to_follow.followers_count
        }, status=status.HTTP_200_OK)


class UnfollowUserView(generics.GenericAPIView):  # """Unfollow a user"""
    permission_classes = [permissions.IsAuthenticated]
    queryset = CustomUser.objects.all()
    lookup_url_kwarg = 'user_id'

    def post(self, request, user_id):
        user_to_unfollow = get_object_or_404(CustomUser, id=user_id)
        current_user = request.user
        
        # Check if trying to unfollow self
        if current_user == user_to_unfollow:
            return Response({
                'error': 'You cannot unfollow yourself'
            }, status=status.HTTP_400_BAD_REQUEST)
        
        # Check if not following
        if not current_user.is_following(user_to_unfollow):
            return Response({
                'message': 'You are not following this user'
            }, status=status.HTTP_400_BAD_REQUEST)
        
        current_user.unfollow_user(user_to_unfollow)  # Unfollow the user
        return Response({
            'message': f'You have unfollowed {user_to_unfollow.username}',
            'following_count': current_user.following_count,
            'user_followers_count': user_to_unfollow.followers_count
        }, status=status.HTTP_200_OK)


class UserFollowersView(generics.ListAPIView): # """Get list of user's followers"""
    serializer_class = UserListSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        user = get_object_or_404(CustomUser, id=self.kwargs['user_id'])
        return user.followers.all()

    def list(self, request, *args, **kwargs):
        user = get_object_or_404(CustomUser, id=self.kwargs['user_id'])
        queryset = self.get_queryset()
        serializer = self.get_serializer(queryset, many=True, context={'request': request})
        
        return Response({
            'user': user.username,
            'followers_count': user.followers_count,
            'followers': serializer.data
        })


class UserFollowingView(generics.ListAPIView): # """Get list of users that this user is following"""
    serializer_class = UserListSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        user = get_object_or_404(CustomUser, id=self.kwargs['user_id'])
        return user.following.all()

    def list(self, request, *args, **kwargs):
        user = get_object_or_404(CustomUser, id=self.kwargs['user_id'])
        queryset = self.get_queryset()
        serializer = self.get_serializer(queryset, many=True, context={'request': request})
        
        return Response({
            'user': user.username,
            'following_count': user.following_count,
            'following': serializer.data
        })