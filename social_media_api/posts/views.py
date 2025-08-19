from rest_framework import viewsets, filters, status
from .serializers import PostSerializer, CommentSerializer
from .models import Post, Comment
from rest_framework import permissions
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.decorators import action
from rest_framework.response import Response
from django.db.models import Q



# Create your views here.

class PostViewSet(viewsets.ModelViewSet):
    queryset = Post.objects.all().order_by('-created_at')
    serializer_class = PostSerializer
    permission_classes = [permissions.IsAuthenticated]
    filter_backends = [
        DjangoFilterBackend,
        filters.SearchFilter
    ]
    search_fields = ['title', 'content']  # Enables search by these fields
    
    
    def perform_create(self, serializer):
        serializer.save(author=self.request.user)
        
       # Handles feed generation, personal feed, like and unlike actions for posts.  
    @action(detail=False, methods=['get'], url_path='feed') #  Full feed: Posts from followed users and own posts
    def feed(self, request):
        user = request.user
        following_users = user.following.all()

        queryset = Post.objects.filter(Q(author__in=following_users) | Q(author=user)
        ).distinct().order_by('-created_at')

        serializer = self.get_serializer(queryset, many=True, context={'request': request})
        following_count = user.following_count

        return Response({
            'message': f'Feed from {following_count} users you follow',
            'following_count': following_count,
            'posts_count': queryset.count(),
            'posts': serializer.data
        })

    @action(detail=False, methods=['get'], url_path='personal-feed')
    def personal_feed(self, request):
        """
        Posts only from followed users (excluding own)
        """
        user = request.user
        following_users = user.following.all()

        queryset = Post.objects.filter(author__in=following_users).order_by('-created_at')
        serializer = self.get_serializer(queryset, many=True, context={'request': request})
        return Response({
            'message': 'Posts from users you follow',
            'posts_count': queryset.count(),
            'posts': serializer.data
        })

    @action(detail=True, methods=['post'], url_path='like')
    def like_post(self, request, pk=None):
        """
        Like a specific post
        """
        post = self.get_object()
        user = request.user

        if post.is_liked_by(user):
            return Response({'message': 'You have already liked this post'}, status=status.HTTP_400_BAD_REQUEST)

        post.likes.add(user)
        return Response({'message': 'Post liked successfully', 'likes_count': post.likes_count}, status=status.HTTP_200_OK)

    @action(detail=True, methods=['post'], url_path='unlike')
    def unlike_post(self, request, pk=None):
        """
        Unlike a specific post
        """
        post = self.get_object()
        user = request.user

        if not post.is_liked_by(user):
            return Response({'message': 'You have not liked this post'}, status=status.HTTP_400_BAD_REQUEST)

        post.likes.remove(user)
        return Response({'message': 'Post unliked successfully', 'likes_count': post.likes_count}, status=status.HTTP_200_OK)

    def get_object_by_pk(self, pk):
        """
        Helper method to retrieve a Post instance by pk or raise 404
        """
        from django.shortcuts import get_object_or_404
        return get_object_or_404(Post, pk=pk)


class CommentViewSet(viewsets.ModelViewSet):
    queryset = Comment.objects.all().order_by('-created_at')
    serializer_class = CommentSerializer
    permission_classes = [permissions.IsAuthenticated]
        
    def perform_create(self, serializer):
        serializer.save(author=self.request.user)
        
    def get_queryset(self): 
        queryset = super().get_queryset()
        post_id = self.request.query_params.get('post_id')
        if post_id: queryset = queryset.filter(post_id=post_id) 
        return queryset
    
    