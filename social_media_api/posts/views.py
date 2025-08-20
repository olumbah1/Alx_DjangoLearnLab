from rest_framework import generics, permissions, filters, status
from rest_framework.views import APIView
from rest_framework.response import Response
from django_filters.rest_framework import DjangoFilterBackend
from django.shortcuts import get_object_or_404
from django.db.models import Q
from .models import Post, Comment, Like
from .serializers import PostSerializer, CommentSerializer
from notifications.models import Notification

class PostListCreateAPIView(generics.ListCreateAPIView):  # List and create posts
    queryset = Post.objects.all().order_by('-created_at')  # Get all posts ordered by newest
    serializer_class = PostSerializer  # Use PostSerializer to serialize data
    permission_classes = [permissions.IsAuthenticated]  # Only authenticated users can access
    filter_backends = [DjangoFilterBackend, filters.SearchFilter]  # Enable filtering and search
    search_fields = ['title', 'content']  # Allow search by title and content

    def perform_create(self, serializer):
        serializer.save(author=self.request.user)  # Set current user as author

class PostDetailAPIView(generics.RetrieveUpdateDestroyAPIView):  # Retrieve, update, or delete a single post
    queryset = Post.objects.all()  # Get all posts
    serializer_class = PostSerializer  # Use PostSerializer
    permission_classes = [permissions.IsAuthenticated]  # Only authenticated users allowed

class PostLikeView(APIView):  # View to like a post
    permission_classes = [permissions.IsAuthenticated]  # Only authenticated users allowed

    def post(self, request, pk):  # Handle POST request to like a post
        post = get_object_or_404(Post, pk=pk)  # Get the post or return 404
        user = request.user  # Get current user

        if Like.objects.filter(post=post, user=user).exists():
            return Response({'message': 'Already liked'}, status=status.HTTP_400_BAD_REQUEST)  # Prevent duplicate likes
        Like.objects.create(post=post, user=user)  # Create the like

        if post.author != user:
            Notification.objects.create(recipient=post.author,
                                        actor=user, verb='liked your post',
                                        target=post)  # Notify the post author

        return Response({'message': 'Post liked'}, status=status.HTTP_200_OK)  # Return success

class PostUnlikeAPIView(APIView):  # View to unlike a post
    permission_classes = [permissions.IsAuthenticated]  # Only authenticated users allowed

    def post(self, request, pk):  # Handle POST request to unlike a post
        post = get_object_or_404(Post, pk=pk)  # Get the post or return 404
        user = request.user  # Get current user

        like = Like.objects.filter(post=post, user=user).first()  # Find the like
        if not like: return Response({'message': 'You have not liked this post'}, status=status.HTTP_400_BAD_REQUEST)  # Return if like not found

        like.delete()  # Delete the like
        return Response({'message': 'Post unliked'}, status=status.HTTP_200_OK)  # Return success

class FeedAPIView(APIView):  # View to show user's feed
    permission_classes = [permissions.IsAuthenticated]  # Only authenticated users allowed

    def get(self, request):  # Handle GET request
        user = request.user  # Get current user
        following_users = user.following.all()  # Get users this user is following
        queryset = Post.objects.filter(Q(author__in=following_users) | Q(author=user)).distinct().order_by('-created_at')  # Get posts from following or self

        serializer = PostSerializer(queryset, many=True, context={'request': request})  # Serialize posts
        return Response({'message': 
            f'Feed from {user.following_count} users you follow',
            'following_count': user.following_count, 
            'posts_count': queryset.count(), 
            'posts': serializer.data})  # Return feed response

class PersonalFeedAPIView(APIView):  # View to show only followed users' posts
    permission_classes = [permissions.IsAuthenticated]  # Only authenticated users allowed

    def get(self, request):  # Handle GET request
        user = request.user  # Get current user
        following_users = user.following.all()  # Get followed users
        queryset = Post.objects.filter(author__in=following_users).order_by('-created_at')  # Get their posts
        serializer = PostSerializer(queryset, many=True, context={'request': request})  # Serialize posts

        return Response({'message':
            'Posts from users you follow',
            'posts_count': queryset.count(), 
            'posts': serializer.data})  # Return response

class CommentListCreateAPIView(generics.ListCreateAPIView):  # View to list/create comments
    serializer_class = CommentSerializer  # Use CommentSerializer
    permission_classes = [permissions.IsAuthenticated]  # Only authenticated users allowed

    def get_queryset(self):
        return Comment.objects.filter(
            post_id=self.request.query_params.get('post_id')).order_by(
                '-created_at') if self.request.query_params.get(
                    'post_id') else Comment.objects.none()  # Get comments for a post

    def perform_create(self, serializer): 
        serializer.save(author=self.request.user)  # Set current user as comment author
