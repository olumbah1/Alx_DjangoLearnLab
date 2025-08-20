from rest_framework.authtoken.models import Token
from rest_framework import generics, status
from django.shortcuts import get_object_or_404
from .models import CustomUser
from rest_framework import permissions
from rest_framework.response import Response
from rest_framework.views import APIView
from .serializers import UserRegistrationSerializer, UserLoginSerializer, UserProfileSerializer, UserListSerializer
# Create your views here.

class UserRegistrationView(generics.CreateAPIView):  # View to register a new user
    queryset = CustomUser.objects.all()  # Define queryset for the view
    serializer_class = UserRegistrationSerializer  # Use serializer to handle user data
    permission_classes = [permissions.AllowAny]  # Allow any user (even unauthenticated) to register

    def create(self, request, *args, **kwargs):  # Handle POST request for user registration
        serializer = self.get_serializer(data=request.data)  # Deserialize incoming data
        serializer.is_valid(raise_exception=True)  # Validate data, raise error if invalid
        user = serializer.save()  # Save the new user
        token, created = Token.objects.get_or_create(user=user)  # Create or get auth token
        return Response({  # Return user data and token
            'user': UserProfileSerializer(user).data,
            'token': token.key
        }, status=status.HTTP_201_CREATED)

class UserLoginView(APIView):  # View to handle user login
    permission_classes = [permissions.AllowAny]  # Anyone can attempt login
    serializer_class = UserLoginSerializer  # Use this serializer for login data

    def post(self, request):  # Handle POST request to log user in
        serializer = UserLoginSerializer(data=request.data)  # Deserialize login data
        if serializer.is_valid():  # If credentials are valid
            user = serializer.validated_data['user']  # Extract user from validated data
            token, created = Token.objects.get_or_create(user=user)  # Get or create token
            return Response({  # Return user data and token
                'user': UserProfileSerializer(user).data,
                'token': token.key
            })
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)  # Return errors if invalid

class UserProfileView(generics.RetrieveUpdateAPIView):  # View to get or update own profile
    serializer_class = UserProfileSerializer  # Use this serializer for profile
    permission_classes = [permissions.IsAuthenticated]  # Only authenticated users can access

    def get_object(self): return self.request.user  # Return the current user

class UserDetailView(generics.RetrieveAPIView):  # View to get any user's profile by username
    queryset = CustomUser.objects.all()  # All users are queryable
    serializer_class = UserProfileSerializer  # Use profile serializer
    permission_classes = [permissions.IsAuthenticated]  # Only authenticated users can access
    lookup_field = 'username'  # Lookup by username instead of ID

class FollowUserView(generics.GenericAPIView):  # View to follow a user
    permission_classes = [permissions.IsAuthenticated]  # Only logged-in users can follow
    queryset = CustomUser.objects.all()  # All users are followable
    lookup_url_kwarg = 'user_id'  # URL will contain user_id to follow

    def post(self, request, user_id):  # Handle POST request to follow a user
        user_to_follow = get_object_or_404(CustomUser, id=user_id)  # Get target user
        current_user = request.user  # Get current user

        if current_user == user_to_follow:  # Prevent following self
            return Response({'error': 'You cannot follow yourself'}, status=status.HTTP_400_BAD_REQUEST)

        if current_user.is_following(user_to_follow):  # Check if already following
            return Response({'message': 'You are already following this user'}, status=status.HTTP_400_BAD_REQUEST)

        current_user.follow_user(user_to_follow)  # Perform the follow action

        return Response({  # Return success with counts
            'message': f'You are now following {user_to_follow.username}',
            'following_count': current_user.following_count,
            'user_followers_count': user_to_follow.followers_count
        }, status=status.HTTP_200_OK)

class UnfollowUserView(generics.GenericAPIView):  # View to unfollow a user
    permission_classes = [permissions.IsAuthenticated]  # Only logged-in users can unfollow
    queryset = CustomUser.objects.all()  # All users can be unfollowed
    lookup_url_kwarg = 'user_id'  # URL will contain user_id to unfollow

    def post(self, request, user_id):  # Handle POST request to unfollow a user
        user_to_unfollow = get_object_or_404(CustomUser, id=user_id)  # Get target user
        current_user = request.user  # Get current user

        if current_user == user_to_unfollow:  # Prevent unfollowing self
            return Response({'error': 'You cannot unfollow yourself'}, status=status.HTTP_400_BAD_REQUEST)

        if not current_user.is_following(user_to_unfollow):  # Check if not following
            return Response({'message': 'You are not following this user'}, status=status.HTTP_400_BAD_REQUEST)

        current_user.unfollow_user(user_to_unfollow)  # Perform the unfollow action

        return Response({  # Return success with updated counts
            'message': f'You have unfollowed {user_to_unfollow.username}',
            'following_count': current_user.following_count,
            'user_followers_count': user_to_unfollow.followers_count
        }, status=status.HTTP_200_OK)

class UserFollowersView(generics.ListAPIView):  # View to get list of a user's followers
    serializer_class = UserListSerializer  # Use this serializer for user list
    permission_classes = [permissions.IsAuthenticated]  # Only authenticated users

    def get_queryset(self):  # Define queryset of followers
        user = get_object_or_404(CustomUser, id=self.kwargs['user_id'])  # Get target user
        return user.followers.all()  # Return all followers

    def list(self, request, *args, **kwargs):  # Customize list response
        user = get_object_or_404(CustomUser, id=self.kwargs['user_id'])  # Get target user again
        queryset = self.get_queryset()  # Get followers queryset
        serializer = self.get_serializer(queryset, many=True, context={'request': request})  # Serialize data
        return Response({  # Return formatted follower list
            'user': user.username,
            'followers_count': user.followers_count,
            'followers': serializer.data
        })

class UserFollowingView(generics.ListAPIView):  # View to get users that a user is following
    serializer_class = UserListSerializer  # Use serializer for listing
    permission_classes = [permissions.IsAuthenticated]  # Only authenticated users

    def get_queryset(self):  # Define queryset of followings
        user = get_object_or_404(CustomUser, id=self.kwargs['user_id'])  # Get target user
        return user.following.all()  # Return all followed users

    def list(self, request, *args, **kwargs):  # Customize list response
        user = get_object_or_404(CustomUser, id=self.kwargs['user_id'])  # Get target user again
        queryset = self.get_queryset()  # Get followings queryset
        serializer = self.get_serializer(queryset, many=True, context={'request': request})  # Serialize data
        return Response({  # Return formatted following list
            'user': user.username,
            'following_count': user.following_count,
            'following': serializer.data
        })
