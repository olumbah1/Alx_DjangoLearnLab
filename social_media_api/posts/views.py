from rest_framework import generics, permissions, filters, status
from rest_framework.views import APIView
from rest_framework.response import Response
from django_filters.rest_framework import DjangoFilterBackend
from django.shortcuts import get_object_or_404
from django.db.models import Q
from .models import Post, Comment
from .serializers import PostSerializer, CommentSerializer


class PostListCreateAPIView(generics.ListCreateAPIView):
    queryset = Post.objects.all().order_by('-created_at')
    serializer_class = PostSerializer
    permission_classes = [permissions.IsAuthenticated]
    filter_backends = [DjangoFilterBackend, filters.SearchFilter]
    search_fields = ['title', 'content']

    def perform_create(self, serializer):
        serializer.save(author=self.request.user)

class PostDetailAPIView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Post.objects.all()
    serializer_class = PostSerializer
    permission_classes = [permissions.IsAuthenticated]

class PostLikeAPIView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def post(self, request, pk):
        post = get_object_or_404(Post, pk=pk)
        user = request.user

        if post.is_liked_by(user):
            return Response({'message': 'You have already liked this post'}, status=status.HTTP_400_BAD_REQUEST)

        post.likes.add(user)
        return Response({'message': 'Post liked successfully', 'likes_count': post.likes_count})

class PostUnlikeAPIView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def post(self, request, pk):
        post = get_object_or_404(Post, pk=pk)
        user = request.user

        if not post.is_liked_by(user):
            return Response({'message': 'You have not liked this post'}, status=status.HTTP_400_BAD_REQUEST)

        post.likes.remove(user)
        return Response({'message': 'Post unliked successfully', 'likes_count': post.likes_count})

class FeedAPIView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request):
        user = request.user
        following_users = user.following.all()
        queryset = Post.objects.filter(
            Q(author__in=following_users) | Q(author=user)
        ).distinct().order_by('-created_at')

        serializer = PostSerializer(queryset, many=True, context={'request': request})
        return Response({
            'message': f'Feed from {user.following_count} users you follow',
            'following_count': user.following_count,
            'posts_count': queryset.count(),
            'posts': serializer.data
        })

class PersonalFeedAPIView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request):
        user = request.user
        following_users = user.following.all()
        queryset = Post.objects.filter(author__in=following_users).order_by('-created_at')
        serializer = PostSerializer(queryset, many=True, context={'request': request})

        return Response({
            'message': 'Posts from users you follow',
            'posts_count': queryset.count(),
            'posts': serializer.data
        })

class CommentListCreateAPIView(generics.ListCreateAPIView):
    serializer_class = CommentSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        post_id = self.request.query_params.get('post_id')
        return Comment.objects.filter(post_id=post_id).order_by('-created_at') if post_id else Comment.objects.none()

    def perform_create(self, serializer):
        serializer.save(author=self.request.user)


